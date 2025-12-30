from llama_cpp import Llama
from worker.settings import settings
import json
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        self.llm = None
        model_path = settings.LLM_MODEL_PATH
        
        # Deep Diagnostic
        import os
        logger.info(f"DEBUG: Checking model path: {model_path}")
        logger.info(f"DEBUG: /data exists: {os.path.exists('/data')}")
        if os.path.exists('/data'):
            logger.info(f"DEBUG: /data contents: {os.listdir('/data')}")
            if os.path.exists('/data/models'):
                logger.info(f"DEBUG: /data/models contents: {os.listdir('/data/models')}")
        
        # Auto-discovery if configured path fails
        if not os.path.exists(model_path):
            models_dir = "/data/models"
            if os.path.exists(models_dir):
                gguf_files = [f for f in os.listdir(models_dir) if f.endswith(".gguf")]
                if gguf_files:
                    model_path = os.path.join(models_dir, gguf_files[0])
                    logger.info(f"INFO: Configured model not found. Auto-discovered: {model_path}")

        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=settings.LLM_CONTEXT_WINDOW,
                n_threads=4,
                n_batch=128,          # Lower batch size saves memory
                n_gpu_layers=0,       # Force CPU if not explicitly configured
                verbose=False
            )
            logger.info(f"SUCCESS: LLM Loaded from {model_path}")
        except Exception as e:
            logger.warning(f"Warning: Failed to load local LLM: {e}.")

    def generate_response(self, prompt: str, schema: dict = None, max_retries: int = 2) -> dict:
        if not self.llm:
            return self._deterministic_fallback("LLM not loaded")

        original_prompt = prompt
        if schema:
            # Mistral 7B performs better with concrete examples than complex JSON schemas
            prompt += "\n\nProvide the analysis in the following JSON format ONLY. Do not use placeholders.\n"
            prompt += "JSON: {\"response\": \"...\", \"sentiment\": \"...\", \"summary\": \"...\", \"history_summary\": \"...\", \"draft_response\": \"...\", \"extracted_fields\": {\"product\": \"...\", \"serial\": \"...\"}, \"predicted_csat\": 4, \"confidence\": 0.9}"
            prompt += "\n\nJSON: {"

        for attempt in range(max_retries):
            try:
                # Note: No native timeout in llama-cpp-python __call__
                # We rely on the container/worker level timeout management if needed
                response = self.llm(
                    prompt,
                    max_tokens=settings.LLM_MAX_TOKENS,
                    stop=["<|endoftext|>", "\n\n"], # Stop on double newline or end
                    echo=False
                )

                text = response['choices'][0]['text']
                # If we prepended "{", we add it back to the text
                full_text = "{" + text if schema else text
                logger.info(f"DEBUG: RAW LLM OUTPUT: {full_text}")

                json_match = re.search(r'\{.*\}', full_text, re.DOTALL)
                if json_match:
                    try:
                        parsed = json.loads(json_match.group())
                        logger.info("DEBUG: Successfully parsed JSON")
                        return parsed
                    except json.JSONDecodeError as je:
                        logger.error(f"DEBUG: JSON Parse Error: {je} for text: {json_match.group()}")
                
                if not schema:
                    return {"response": text, "confidence": 0.5}
                
            except Exception as e:
                logger.error(f"DEBUG: LLM Generation Exception: {e}")
                continue
        
        return self._deterministic_fallback("Max retries or generation error")

    def _deterministic_fallback(self, reason: str = "unknown") -> dict:
        return {
            "response": "I apologize, but I am currently unable to generate a detailed response. A support agent will review your request shortly.",
            "confidence": 0.0,
            "fallback": True,
            "fallback_reason": reason
        }

llm_engine = LLMEngine()
