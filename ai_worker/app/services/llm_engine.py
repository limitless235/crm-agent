from llama_cpp import Llama
from app.core.config import settings
import json
import re

class LLMEngine:
    def __init__(self):
        # We assume the model exists at settings.LLM_MODEL_PATH
        # In a real setup, we might download it if missing
        self.llm = None
        try:
            self.llm = Llama(
                model_path=settings.LLM_MODEL_PATH,
                n_ctx=4096,
                n_threads=4,
                verbose=False
            )
        except Exception as e:
            print(f"Warning: Failed to load local LLM: {e}. Worker will start but generation will fail until model is provided.")

    def generate_response(self, prompt: str, schema: dict = None, max_retries: int = 3) -> dict:
        if not self.llm:
            return self._deterministic_fallback()

        # Enhance prompt for JSON output if schema is provided
        if schema:
            prompt += f"\n\nReturn your response as a JSON object strictly following this schema: {json.dumps(schema)}"

        for attempt in range(max_retries):
            try:
                response = self.llm(
                    prompt,
                    max_tokens=500,
                    stop=["<|endoftext|>", "}"], 
                    echo=False
                )

                text = response['choices'][0]['text']
                if schema and not text.strip().endswith("}"):
                    text += "}"

                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                
                # If no JSON found but schema was requested, retry
                if schema:
                    continue
                
                return {"response": text}
            except Exception as e:
                print(f"LLM Error (Attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return self._deterministic_fallback()
        
        return self._deterministic_fallback()

    def _deterministic_fallback(self) -> dict:
        return {
            "response": "I apologize, but I am currently unable to generate a detailed response. A support agent will review your request shortly.",
            "confidence": 0.0,
            "fallback": True
        }

llm_engine = LLMEngine()
