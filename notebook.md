# Custom Fine‑Tuned LLM (Notebook Guide)

This is a **complete, teach‑by‑example guide** for training a custom LLM that
follows Adriana James’ brand tone. It references the exact code in `notebook.py`
so you can understand *what each part does* and *why it matters*.

The training script uses **LoRA** (parameter‑efficient fine‑tuning) on a small
base model so you can run it in Colab with a single GPU.

---

## 1) Goal and Mental Model (Why We Fine‑Tune)

Prompting alone is good, but fine‑tuning makes the model **internalize style**:
- it learns the tone and rhythm from examples
- outputs are more consistent with the brand
- fewer “generic AI” completions

In this project, RAG + Cohere embeddings still retrieve relevant examples,
but the generator itself becomes brand‑aware.

---

## 2) What You Need Before Training

### A) GPU runtime
Use Google Colab (T4/V100/A100) or local GPU.

### B) Training data
You said you **don’t have data**, so here are good sources:

**Recommended (permissive license)**
- **UpMails (CC0)** – subject lines, email sequences, A/B tests  
  https://upmails.eu

**Research datasets (check license if commercial)**
- **AESLC (CC BY‑NC‑SA)** – Enron subject line corpus  
  https://github.com/ryanzhumich/AESLC

> If you plan commercial usage, prefer CC0 or fully commercial‑friendly sources.

---

## 3) Data Formats We Support

### A) JSONL (prompt/completion)
Each line is a JSON object:

```
{"prompt": "Write a welcome email for new subscribers", "completion": "Subject: Welcome..."}
{"prompt": "Write a social post about a new product launch", "completion": "We just launched..."}
```

Put files here:
```
data/train.jsonl
data/valid.jsonl  # optional; auto‑split if missing
```

### B) AESLC `.subject` format (your screenshot)
The AESLC dataset uses this layout:

```
AESLC/enron_subject_line/
  train/
  dev/
  test/
```

Each `.subject` file looks like:
```
subject
Bishops Corner

@ann0
draw file bishops corneer
@ann1
draw file for bishops corner
@ann2
draw file you created for bishops corner
```

The script handles this automatically by turning:
- **subject** → completion  
- **body / @ann** → prompt  

To enable AESLC in `notebook.py`:
```
USE_AESLC = True
AESLC_ROOT = "AESLC/enron_subject_line"
```

**Code reference (AESLC parsing and dataset building):**
```104:201:notebook.py
def _read_non_empty(lines: List[str], start_idx: int) -> Tuple[str, int]:
    # ...

def parse_aeslc_subject_file(path: str) -> Tuple[str, List[str]]:
    # ...

def build_aeslc_rows(root: str, split: str) -> List[Dict]:
    # ...

def build_dataset(train_path: str, valid_path: str) -> Tuple[Dataset, Dataset]:
    # ...
```

---

## 4) Colab Setup (Step‑by‑Step)

```bash
# 1) Install dependencies
pip install -q transformers datasets peft accelerate bitsandbytes

# 2) (Optional) Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

Copy `notebook.py` into Colab, then run:
```bash
python notebook.py
```

---

## 5) How the Training Script Works (Explain the Code)

### Step 1 — Configuration
This block sets the base model, data paths, and training hyperparameters.
It’s where you switch between JSONL and AESLC.

```32:56:notebook.py
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TRAIN_DATA_PATH = "data/train.jsonl"
VALID_DATA_PATH = "data/valid.jsonl"
USE_AESLC = False
AESLC_ROOT = "AESLC/enron_subject_line"
```

### Step 2 — Format training examples
We create a consistent instruction format:
`system` → brand voice  
`user` → prompt  
`assistant` → expected output  

```70:97:notebook.py
class Example:
    prompt: str
    completion: str

SYSTEM_PROMPT = (...)

def format_example(example: Example) -> str:
    return (
        f"<s>[SYSTEM]...[/SYSTEM]"
        f"[USER]...[/USER]"
        f"[ASSISTANT]...[/ASSISTANT]"
    )
```

### Step 3 — Build datasets
We normalize either JSONL or AESLC into a single list of examples.
If there is no validation file, we auto‑split 90/10.

```181:201:notebook.py
def build_dataset(train_path: str, valid_path: str) -> Tuple[Dataset, Dataset]:
    if USE_AESLC:
        train_rows = build_aeslc_rows(...)
        valid_rows = build_aeslc_rows(...)
    else:
        train_rows = load_jsonl(...)
        valid_rows = load_jsonl(...) if exists else []
```

### Step 4 — Tokenization
We convert text into token IDs. This sets the maximum length.

```209:218:notebook.py
def tokenize_dataset(tokenizer, dataset: Dataset) -> Dataset:
    return dataset.map(tokenize_fn, batched=True, remove_columns=["text"])
```

### Step 5 — Load model + LoRA
We load the base model and add LoRA adapters for efficient fine‑tuning.
`USE_4BIT` reduces memory usage.

```226:263:notebook.py
def load_model_and_tokenizer() -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    tokenizer = AutoTokenizer.from_pretrained(...)
    if USE_4BIT:
        load_in_4bit=True
    model = AutoModelForCausalLM.from_pretrained(...)
    model = get_peft_model(model, lora_config)
```

### Step 6 — Train
Hugging Face `Trainer` handles the training loop.
We save the adapter and tokenizer at the end.

```271:311:notebook.py
def train():
    train_ds, valid_ds = build_dataset(...)
    trainer = Trainer(...)
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
```

### Step 7 — Quick sanity generation
We generate one sample after training to confirm it works.

```319:336:notebook.py
def generate_sample(prompt: str):
    model, tokenizer = load_model_and_tokenizer()
    output = model.generate(...)
```

---

## 6) Why LoRA (Simple Explanation)

Full fine‑tuning updates all model weights. That is **expensive**.
LoRA updates a tiny set of adapter weights:
- lower GPU memory
- faster training
- still captures style and tone

This is why it’s the best option for Colab‑scale training.

---

## 7) After Training — Use the Model

Your training run saves a **LoRA adapter** and tokenizer to:
```
finetuned-adapter/
```

You have two options for using this in the backend:

### Option A — Merge adapter into a full model (recommended)

1. In Colab, load the base model and adapter, merge, and save:
   ```python
   from transformers import AutoModelForCausalLM, AutoTokenizer
   from peft import PeftModel
   import torch

   BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
   ADAPTER_DIR = "finetuned-adapter"
   MERGED_DIR = "finetuned-merged"

   tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
   dtype = torch.float16 if torch.cuda.is_available() else torch.float32
   base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=dtype, device_map="auto")

   model = PeftModel.from_pretrained(base, ADAPTER_DIR)
   model = model.merge_and_unload()

   model.save_pretrained(MERGED_DIR)
   tokenizer.save_pretrained(MERGED_DIR)
   ```

2. Download `finetuned-merged/` and place it in your project under:
   ```
   backend/models/finetuned-merged/
   ```

3. Update `.env`:
   ```env
   HUGGINGFACE_MODEL=./backend/models/finetuned-merged
   ```

4. Restart the API server.

This makes the fine‑tuned model look like a normal Hugging Face model folder, so
`backend/services/llm_service.py` can load it without any PEFT changes.

### Option B — Use the adapter directly (advanced)

Alternatively, you can keep `finetuned-adapter/` and modify the backend to load
the base model plus adapter with `PeftModel.from_pretrained(...)`. This gives
smaller disk size but requires code changes, so Option A is usually simpler.

---

## 8) Best Practices (Make Results Better)

- Use **real brand copy** if available.
- Mix multiple content types (email, social, ads).
- Remove noisy or irrelevant text.
- Ensure licensing is compatible with your use case.

---

## 9) Troubleshooting

**`FileNotFoundError: data/train.jsonl`**  
You’re still in JSONL mode. Either:
- add `data/train.jsonl`, or
- set `USE_AESLC = True` and set `AESLC_ROOT`

**CUDA out of memory**  
Reduce `MAX_LENGTH`, reduce `TRAIN_BATCH_SIZE`, or keep `USE_4BIT = True`.

---

## 10) Want It Customized?

Tell me:
- base model size (1B, 2B, 7B)
- target language
- commercial or non‑commercial

I can tailor the training setup for you.
