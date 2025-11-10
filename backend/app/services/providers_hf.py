from app.services.provider_interface import BaseLLMProvider
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from app.services.token_utils import count_tokens
import os

from typing import List, Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
except Exception:
    _TIKTOKEN_AVAILABLE = False

load_dotenv()  # Load API token from .env file

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
DEFAULT_MODEL = os.getenv("HF_MODEL_NAME", "google/flan-t5-base")  # good free text model
DEFAULT_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DEFAULT_TIMEOUT = int(os.getenv("LLM_REQUEST_TIMEOUT", "20"))

# “If the decorated function fails with any Exception,
# retry up to 3 times, waiting 1s, 2s, 4s between tries (up to max 8s),
# and if it still fails, re-raise the final error.”
_retry = retry(
    reraise=True,
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)



# adapted from https://huggingface.co/docs/huggingface_hub/main/en/inference#text-generation
# adapter for HuggingFace Inference API
# this class implements the BaseLLMProvider interface
class HuggingFaceProvider(BaseLLMProvider):
    
    def __init__(self):
        self.model = os.getenv("HF_MODEL_NAME", "google/flan-t5-base")
        self.embedding_model = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        # Don’t wait forever for a response — stop waiting after X seconds.
        self.timeout = int(os.getenv("LLM_REQUEST_TIMEOUT", "20"))
        self.client = InferenceClient(model=self.model, token=os.getenv("HF_API_TOKEN"),timeout=self.timeout)
        self.embed_client = InferenceClient(model=self.embedding_model, token=os.getenv("HF_API_TOKEN"),timeout=self.timeout)

    @_retry
    def generate_response(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7, **kwargs) -> str:
        token_count = count_tokens(prompt)
        if token_count + max_tokens > 4096:
            max_tokens = 4000-token_count
            # raise ValueError(f"Prompt too long: {token_count} tokens + {max_tokens} max_tokens exceeds 4096 limit.")
        return self.client.text_generation(prompt, max_new_tokens=max_tokens, temperature=temperature)
    
    def generate_plan(self, prompt: str) -> dict:
        text = self.generate_response(prompt)
        return {"title": f"Plan for: {prompt}", "raw_plan": text}
    @_retry
    def generate_chat(self, messages: list[dict], max_tokens: int = 256, temperature: float = 0.7) -> dict:
        full_prompt = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
        reply = self.generate_response(full_prompt, max_tokens=max_tokens, temperature=temperature)
        return {"content": reply}
    @_retry
    def embed_text(self, text: str) -> list[float]:
        result = self.embed_client.feature_extraction(text)
        if isinstance(result, list) and isinstance(result[0], list):
            return result[0]
        return result
    
    # def token_count(self, text: str) -> int:
    #     try:
    #         import tiktoken
    #         enc = tiktoken.encoding_for_model("gpt2")
    #         return len(enc.encode(text))
    #     except Exception:
    #         return len(text)//4