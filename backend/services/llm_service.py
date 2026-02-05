# =============================================================================
# Marketing Assistant AI - LLM Service (Hugging Face Version)
# =============================================================================
# LLM-powered marketing copy generation using Hugging Face Transformers.
# LLM runs locally; Cohere is used elsewhere for embeddings/rerank.
# =============================================================================

import logging
from typing import List, Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from backend.config import settings
from backend.models.schemas import (
    GenerationRequest,
    GenerationResponse,
    RetrievedContent,
    ContentType
)

# Import brand voice components
from backend.data.brand.voice import get_brand_voice_prompt
from backend.data.brand.tone_guidelines import format_guidelines_for_prompt
from backend.data.brand.vocabulary import format_vocabulary_for_prompt

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for generating marketing copy using Hugging Face Transformers.
    
    RUNS LOCALLY - NO API KEY REQUIRED!
    
    Uses the professionally structured brand voice from backend.data.brand.
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the LLM service."""
        self.model_name = model_name or settings.huggingface_model
        self.max_tokens = settings.max_generation_tokens
        self.temperature = settings.generation_temperature
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing LLM: {self.model_name} on {self.device}")
        
        # Lazy loading
        self._model = None
        self._tokenizer = None
        self._pipe = None
    
    def _load_model(self):
        """Lazy load the model."""
        if self._pipe is not None:
            return
        
        logger.info(f"Loading model {self.model_name}...")
        
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            model_kwargs = {
                "trust_remote_code": True,
                "low_cpu_mem_usage": True,
            }
            
            if self.device == "cuda":
                model_kwargs["torch_dtype"] = torch.float16
            
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            self._model.to(self.device)
            
            self._pipe = pipeline(
                "text-generation",
                model=self._model,
                tokenizer=self._tokenizer,
                device=0 if self.device == "cuda" else -1,
            )
            
            logger.info(f"Model loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Failed to load model: {e}")
    
    async def generate(
        self,
        request: GenerationRequest,
        retrieved_content: Optional[List[RetrievedContent]] = None
    ) -> GenerationResponse:
        """Generate marketing copy based on the request."""
        self._load_model()
        
        # Build prompt using brand voice components
        full_prompt = self._build_prompt(request, retrieved_content)
        
        try:
            logger.debug(f"Generating {request.content_type.value} content...")
            
            outputs = self._pipe(
                full_prompt,
                max_new_tokens=min(self.max_tokens, 1024),
                temperature=self.temperature,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
            )
            
            generated_text = outputs[0]["generated_text"]
            cleaned = self._clean_output(generated_text, full_prompt)
            
            response = GenerationResponse(
                generated_content=cleaned,
                content_type=request.content_type,
                prompt_used=request.prompt,
                similar_content_used=[
                    r.content.title for r in (retrieved_content or [])
                ],
                generation_metadata={
                    "model": self.model_name,
                    "device": self.device,
                    "temperature": self.temperature
                }
            )
            
            return response
        
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise RuntimeError(f"Failed to generate content: {e}")
    
    async def refine_content(
        self,
        original_content: str,
        feedback: str,
        content_type: ContentType
    ) -> str:
        """Refine existing content based on feedback."""
        self._load_model()
        
        prompt = self._build_refine_prompt(original_content, feedback, content_type)
        
        try:
            outputs = self._pipe(
                prompt,
                max_new_tokens=min(self.max_tokens, 1024),
                temperature=self.temperature,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
            )
            
            generated_text = outputs[0]["generated_text"]
            cleaned = self._clean_output(generated_text, prompt)
            return cleaned
        
        except Exception as e:
            logger.error(f"Refinement failed: {e}")
            raise RuntimeError(f"Failed to refine content: {e}")
    
    def _build_prompt(
        self,
        request: GenerationRequest,
        retrieved_content: Optional[List[RetrievedContent]] = None
    ) -> str:
        """Build the full prompt for generation."""
        brand_voice = get_brand_voice_prompt()
        guidelines = format_guidelines_for_prompt(request.content_type.value)
        vocabulary = format_vocabulary_for_prompt()
        
        prompt_parts = [
            brand_voice,
            "",
            guidelines,
            "",
            vocabulary,
            "",
            f"CONTENT TYPE: {request.content_type.value}",
            f"PROMPT: {request.prompt}",
        ]
        
        if request.target_audience:
            prompt_parts.append(f"TARGET AUDIENCE: {request.target_audience}")
        
        if request.key_points:
            prompt_parts.append("KEY POINTS:")
            prompt_parts.extend([f"- {p}" for p in request.key_points])
        
        if request.tone_override:
            prompt_parts.append(f"TONE OVERRIDE: {request.tone_override}")
        
        if retrieved_content:
            prompt_parts.append("\nSIMILAR CONTENT EXAMPLES:")
            for i, item in enumerate(retrieved_content, 1):
                prompt_parts.append(
                    f"\nExample {i} ({item.content.content_type.value}):\n"
                    f"Title: {item.content.title}\n"
                    f"Content:\n{item.content.content}"
                )
        
        prompt_parts.append("\nOUTPUT:")
        
        return "\n".join(prompt_parts)
    
    def _build_refine_prompt(
        self,
        original_content: str,
        feedback: str,
        content_type: ContentType
    ) -> str:
        """Build prompt for refinement."""
        guidelines = format_guidelines_for_prompt(content_type.value)
        
        prompt = (
            f"{get_brand_voice_prompt()}\n\n"
            f"{guidelines}\n\n"
            f"ORIGINAL CONTENT:\n{original_content}\n\n"
            f"FEEDBACK:\n{feedback}\n\n"
            f"REFINED OUTPUT:"
        )
        
        return prompt
    
    def _clean_output(self, generated_text: str, prompt: str) -> str:
        """Clean generated output by removing prompt and extra tokens."""
        if generated_text.startswith(prompt):
            cleaned = generated_text[len(prompt):].strip()
        else:
            cleaned = generated_text.strip()
        
        for marker in ["OUTPUT:", "REFINED OUTPUT:"]:
            if cleaned.startswith(marker):
                cleaned = cleaned[len(marker):].strip()
        
        return cleaned


# =============================================================================
# Module-level singleton
# =============================================================================

_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create singleton LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
