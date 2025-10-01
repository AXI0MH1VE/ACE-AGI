"""
Local LLM Inference using Hugging Face Transformers
Phi-3-mini-4k-instruct model for sovereign AI operations
Sovereign Core Cycle 20 - No API dependencies
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import time
from typing import Optional, List, Dict, Any
import json

class LocalLLMInference:
    """
    Self-contained local LLM inference using Phi-3
    No API keys or external dependencies required
    """

    _instance: Optional['LocalLLMInference'] = None
    LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialize()

    def _initialize(self):
        """Initialize the local LLM model"""
        print("🚀 Initializing Phi-3 Local LLM...")
        print(f"   Model: {self.LLM_MODEL_NAME}")

        # Detect device
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"   Device: {'CUDA' if self.device == 0 else 'CPU'}")

        # Load tokenizer
        print("   Loading tokenizer...")
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.LLM_MODEL_NAME,
            trust_remote_code=True
        )
        self._tokenizer.pad_token = self._tokenizer.eos_token

        # Load model
        print("   Loading model (this may take ~25s on CPU)...")
        start_time = time.time()

        self._model = AutoModelForCausalLM.from_pretrained(
            self.LLM_MODEL_NAME,
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == 0 else torch.float32,
            low_cpu_mem_usage=True,
        )

        if self.device == 0:
            self._model.to(f'cuda:{self.device}')

        self._model.eval()

        # Create pipeline
        self._pipeline = pipeline(
            "text-generation",
            model=self._model,
            tokenizer=self._tokenizer,
            device=self.device,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=self._tokenizer.eos_token_id,
            pad_token_id=self._tokenizer.eos_token_id,
        )

        load_time = time.time() - start_time
        print(f"✅ Phi-3 initialized in {load_time:.2f}s")
        print(f"   Max tokens: {self._tokenizer.model_max_length}")
        print(f"   Vocab size: {len(self._tokenizer)}")

        self._initialized = True

    def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.7) -> str:
        """
        Generate text using local Phi-3 model

        Args:
            prompt: Input prompt
            max_new_tokens: Maximum new tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        if not hasattr(self, '_pipeline') or self._pipeline is None:
            raise RuntimeError("Local LLM not initialized. Call _initialize() first.")

        try:
            # Format prompt for Phi-3
            formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>"

            generated = self._pipeline(
                formatted_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                return_full_text=False,
            )

            full_text = generated[0]['generated_text']
            return full_text.strip()

        except Exception as e:
            return f"Local LLM generation error: {str(e)}"

    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured output using local LLM

        Args:
            prompt: Input prompt
            schema: Expected JSON schema

        Returns:
            Parsed JSON response
        """
        schema_str = json.dumps(schema, indent=2)
        structured_prompt = f"""Generate a JSON response that matches this schema:

Schema: {schema_str}

User Query: {prompt}

Respond with valid JSON only, no additional text:"""

        response = self.generate(structured_prompt, temperature=0.3)

        try:
            # Try to parse JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass

            # Return error structure
            return {
                "error": "Failed to parse structured response",
                "raw_response": response,
                "schema": schema
            }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": self.LLM_MODEL_NAME,
            "device": "CUDA" if self.device == 0 else "CPU",
            "max_length": self._tokenizer.model_max_length,
            "vocab_size": len(self._tokenizer),
            "initialized": hasattr(self, '_initialized') and self._initialized
        }

# Test function
def test_local_llm():
    """Test the local LLM functionality"""
    print("🧪 Testing Local Phi-3 LLM...")

    llm = LocalLLMInference()

    # Test basic generation
    test_prompt = "What is viral engagement in the context of social media?"
    print(f"Prompt: {test_prompt}")

    response = llm.generate(test_prompt)
    print(f"Response: {response}")

    # Test structured generation
    schema = {
        "type": "object",
        "properties": {
            "definition": {"type": "string"},
            "strategies": {"type": "array", "items": {"type": "string"}},
            "metrics": {"type": "array", "items": {"type": "string"}}
        }
    }

    structured = llm.generate_structured(
        "Explain viral engagement and provide strategies and metrics",
        schema
    )

    print(f"Structured response: {json.dumps(structured, indent=2)}")

    return True

if __name__ == "__main__":
    test_local_llm()
