"""
Notebook-style training script for a custom fine-tuned LLM.

This is designed to run in Google Colab or a GPU notebook.
It keeps everything in one file for easy copy/paste execution.
"""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
import inspect
import warnings
from typing import Dict, List, Tuple

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)


# =============================================================================
# Configuration
# =============================================================================

# Base model to fine-tune (small, fast, decent for style tuning).
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Where your dataset lives (JSONL or CSV).
TRAIN_DATA_PATH = "data/train.jsonl"
VALID_DATA_PATH = "data/valid.jsonl"

# AESLC dataset root (set this if you want to train from AESLC format)
# Example: "AESLC/enron_subject_line"
USE_AESLC = False
AESLC_ROOT = "AESLC/enron_subject_line"

# Output directory for the LoRA adapter or full model.
OUTPUT_DIR = "finetuned-adapter"

# Training parameters
MAX_LENGTH = 512
TRAIN_BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 8
LEARNING_RATE = 2e-4
NUM_EPOCHS = 2
WARMUP_RATIO = 0.05

# Set to True to enable 4-bit loading (requires bitsandbytes).
# If running on CPU or TPU/XLA, this will be disabled automatically.
USE_4BIT = True


# =============================================================================
# Data Format
# =============================================================================
# Each JSONL row should be a dict with either:
# 1) {"prompt": "...", "completion": "..."}
# OR
# 2) {"input": "...", "output": "..."}
#
# The script normalizes both into a single training string.


@dataclass
class Example:
    prompt: str
    completion: str


SYSTEM_PROMPT = (
    "You are a marketing copywriter who writes in Adriana James' voice. "
    "Tone: warm, empowering, clear, concise, action-oriented. "
    "Avoid hype and fake urgency. Use confident, supportive language."
)


def normalize_example(row: Dict) -> Example:
    if "prompt" in row and "completion" in row:
        return Example(prompt=row["prompt"], completion=row["completion"])
    if "input" in row and "output" in row:
        return Example(prompt=row["input"], completion=row["output"])
    raise ValueError("Each row must contain prompt/completion or input/output.")


def format_example(example: Example) -> str:
    # Simple instruction format suitable for causal LM fine-tuning.
    return (
        f"<s>[SYSTEM]\n{SYSTEM_PROMPT}\n[/SYSTEM]\n"
        f"[USER]\n{example.prompt}\n[/USER]\n"
        f"[ASSISTANT]\n{example.completion}\n</s>"
    )


def load_jsonl(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]

def _read_non_empty(lines: List[str], start_idx: int) -> Tuple[str, int]:
    idx = start_idx
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return (lines[idx].strip() if idx < len(lines) else ""), idx


def parse_aeslc_subject_file(path: str) -> Tuple[str, List[str], str]:
    """
    Parse AESLC .subject files that look like:
    subject
    <subject line>
    @ann0
    <annotation text>
    @ann1
    <annotation text>
    ...
    """
    with open(path, "r", encoding="utf-8") as file:
        lines = [line.rstrip("\n") for line in file]

    subject = ""
    annotations: List[str] = []
    body_lines: List[str] = []

    subject_idx = None
    for idx, raw in enumerate(lines):
        lower = raw.strip().lower()
        if lower.startswith("subject") or lower.startswith("@subject"):
            subject_idx = idx
            break

    if subject_idx is not None:
        body_lines = lines[:subject_idx]
        idx = subject_idx
    else:
        idx = 0

    while idx < len(lines):
        line = lines[idx].strip()
        lower = line.lower()
        if lower.startswith("subject") or lower.startswith("@subject"):
            token = "@subject" if lower.startswith("@subject") else "subject"
            remainder = line[len(token):].lstrip(" :")
            if remainder:
                subject = remainder.strip()
            else:
                subject, idx = _read_non_empty(lines, idx + 1)
        elif line.startswith("@ann"):
            ann_text, idx = _read_non_empty(lines, idx + 1)
            if ann_text:
                annotations.append(ann_text)
        idx += 1

    if not subject:
        # Fallback: first non-empty line that isn't an annotation marker
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("@ann"):
                subject = stripped
                break
    body_text = "\n".join([line for line in body_lines if line.strip()]).strip()
    return subject, annotations, body_text


def build_aeslc_rows(root: str, split: str) -> List[Dict]:
    split_dir = os.path.join(root, split)
    rows: List[Dict] = []
    if not os.path.isdir(split_dir):
        print(f"[AESLC] Missing split dir: {split_dir}")
        return rows

    subject_files = [
        filename for filename in os.listdir(split_dir) if filename.endswith(".subject")
    ]
    print(f"[AESLC] {split} subject files: {len(subject_files)}")

    for filename in subject_files:
        subject_path = os.path.join(split_dir, filename)
        subject, annotations, inline_body = parse_aeslc_subject_file(subject_path)
        if not subject:
            continue

        base = subject_path[: -len(".subject")]
        body_path = base + ".body"

        prompts: List[str] = []
        if os.path.exists(body_path):
            with open(body_path, "r", encoding="utf-8") as file:
                body = file.read().strip()
            if body:
                prompts.append(
                    "Write a concise email subject line for this email:\n"
                    f"{body}"
                )
        elif inline_body:
            prompts.append(
                "Write a concise email subject line for this email:\n"
                f"{inline_body}"
            )
        else:
            for ann in annotations:
                prompts.append(
                    "Write a concise email subject line for this summary:\n"
                    f"{ann}"
                )

        for prompt in prompts:
            rows.append({"prompt": prompt, "completion": subject})

    return rows


def build_dataset(train_path: str, valid_path: str) -> Tuple[Dataset, Dataset]:
    if USE_AESLC:
        train_rows = build_aeslc_rows(AESLC_ROOT, "train")
        valid_rows = build_aeslc_rows(AESLC_ROOT, "dev")
    else:
        train_rows = load_jsonl(train_path)
        valid_rows = load_jsonl(valid_path) if os.path.exists(valid_path) else []

    if not train_rows:
        if USE_AESLC:
            raise ValueError(
                "No training rows found. Check AESLC_ROOT and ensure it contains "
                "train/ with .subject files (and optional .body files)."
            )
        raise ValueError(
            f"No training rows found in {train_path}. "
            "Create data/train.jsonl or enable USE_AESLC."
        )

    if not valid_rows:
        random.shuffle(train_rows)
        split_idx = max(1, int(len(train_rows) * 0.9))
        valid_rows = train_rows[split_idx:]
        train_rows = train_rows[:split_idx]

    def to_text(row: Dict) -> Dict:
        ex = normalize_example(row)
        return {"text": format_example(ex)}

    train_ds = Dataset.from_list([to_text(r) for r in train_rows])
    valid_ds = Dataset.from_list([to_text(r) for r in valid_rows])
    return train_ds, valid_ds


# =============================================================================
# Tokenization
# =============================================================================


def tokenize_dataset(tokenizer, dataset: Dataset) -> Dataset:
    def tokenize_fn(batch: Dict) -> Dict:
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            padding=False,
        )

    return dataset.map(tokenize_fn, batched=True, remove_columns=["text"])


# =============================================================================
# Model Setup
# =============================================================================


def _get_lora_targets(model) -> List[str]:
    model_type = getattr(model.config, "model_type", "").lower()
    if model_type in {"gpt2"}:
        return ["c_attn", "c_proj", "c_fc"]
    return [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ]


def load_model_and_tokenizer() -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs = {"device_map": "auto"}
    use_4bit = USE_4BIT and torch.cuda.is_available()
    if USE_4BIT and not torch.cuda.is_available():
        warnings.warn("CUDA not available; disabling 4-bit loading.")

    if use_4bit:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model_kwargs["quantization_config"] = quant_config
    else:
        model_kwargs["torch_dtype"] = torch.float16

    try:
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, **model_kwargs)
    except RuntimeError as exc:
        if use_4bit and "Params4bit" in str(exc):
            warnings.warn(
                "4-bit loading failed (Params4bit error). Falling back to "
                "non-quantized weights. You can also set USE_4BIT=False."
            )
            model_kwargs.pop("quantization_config", None)
            model_kwargs["torch_dtype"] = torch.float16
            model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, **model_kwargs)
        else:
            raise

    if use_4bit:
        model = prepare_model_for_kbit_training(model)

    target_modules = _get_lora_targets(model)
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=target_modules,
    )
    model = get_peft_model(model, lora_config)
    return model, tokenizer


# =============================================================================
# Training
# =============================================================================


def train():
    train_ds, valid_ds = build_dataset(TRAIN_DATA_PATH, VALID_DATA_PATH)
    model, tokenizer = load_model_and_tokenizer()

    tokenized_train = tokenize_dataset(tokenizer, train_ds)
    tokenized_valid = tokenize_dataset(tokenizer, valid_ds)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False
    )

    args_kwargs = dict(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=TRAIN_BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        learning_rate=LEARNING_RATE,
        warmup_ratio=WARMUP_RATIO,
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=100,
        save_steps=100,
        save_total_limit=2,
        optim="adamw_torch",
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    sig = inspect.signature(TrainingArguments.__init__).parameters
    if "evaluation_strategy" not in sig and "eval_strategy" in sig:
        args_kwargs["eval_strategy"] = args_kwargs.pop("evaluation_strategy")

    filtered_args = {k: v for k, v in args_kwargs.items() if k in sig}
    args = TrainingArguments(**filtered_args)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_valid,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print(f"Saved adapter/model to: {OUTPUT_DIR}")


# =============================================================================
# Quick Evaluation
# =============================================================================


def generate_sample(prompt: str):
    model, tokenizer = load_model_and_tokenizer()
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    if hasattr(tokenizer, "apply_chat_template"):
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        text = format_example(Example(prompt=prompt, completion=""))

    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    print(decoded)


if __name__ == "__main__":
    # Step 1: Train
    train()

    # Step 2: Quick sanity check
    generate_sample("Write a short welcome email for new subscribers.")
