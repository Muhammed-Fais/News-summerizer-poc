from langchain.llms.base import LLM
import google.generativeai as genai
from src.config import MODEL_CONFIG
from typing import Optional, List, Any

class GeminiLLM(LLM):

    model_name: str = MODEL_CONFIG["model_name"]
    temperature: float = MODEL_CONFIG["temperature"]
    max_tokens: int = MODEL_CONFIG["max_tokens"]

    def __init__(self):
        super().__init__()

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens
            )
        )
        return response.text

    @property
    def _llm_type(self) -> str:
        return "gemini"