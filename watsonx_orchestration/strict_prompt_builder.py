import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StrictPromptBuilder")

class StrictPromptBuilder:
    """
    Constructs isolated prompt sandboxes for watsonx.ai foundational models,
    forcing absolute data grounding and preventing model hallucination vectors.
    """
    def __init__(self, model_id: str = "ibm/granite-13b-instruct-v2"):
        self.model_id = model_id

    def build_grounded_prompt(self, user_query: str, audited_contexts: List[str]) -> str:
        """Injects strict system directives around verified context blocks to anchor outputs."""
        logger.info(f"Assembling isolated prompt boundary for target model: {self.model_id}")
        
        system_mandate = (
            "=========================================================================\n"
            "VANE-GUARD SOVEREIGN ARCHITECTURE MANDATE: GROUNDING PROTECTION ACTIVE\n"
            "CRITICAL: Formulate your answer based ONLY on the verified context blocks\n"
            "provided below. Do not assume, elaborate, or reference external knowledge.\n"
            "If the context blocks do not contain explicit proof to answer, reply with:\n"
            "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]\n"
            "========================================================================="
        )
        
        # Flatten our validated data streams (IMS, SevOne, etc.) into the truth block
        truth_context = "\n".join([f"[VERIFIED_DATA_BLOCK_{i}]: {block}" for i, block in enumerate(audited_contexts)])
        
        full_prompt = (
            f"{system_mandate}\n\n"
            f"--- BEGIN TRUTH CONTEXT BASELINE ---\n{truth_context}\n--- END TRUTH CONTEXT BASELINE ---\n\n"
            f"USER INPUT QUERY: {user_query}\n"
            f"DETERMINISTIC MODEL RESPONSE:"
        )
        return full_prompt

if __name__ == "__main__":
    # Component sanity self-test
    builder = StrictPromptBuilder()
    
    query = "Check system status of server 01."
    contexts = ["[SEVONE_TELEMETRY_LOG_ENTRY] Device ID: FIN-PROD-SERVER-01 | CPU Load: 42.8% | Status: SECURE"]
    
    secure_prompt = builder.build_grounded_prompt(query, contexts)
    print(f"Generated secure watsonx prompt baseline:\n\n{secure_prompt}")
