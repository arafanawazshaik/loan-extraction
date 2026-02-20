import logging

logger = logging.getLogger(__name__)


class ConsensusChecker:
    """Compares rule-based and LLM extractions for higher accuracy."""

    def check(self, rule_result, llm_result):
        """Compare P1 and P2 results, pick the best."""
        final = {}

        fields = ["borrower_name", "loan_amount", "interest_rate", "loan_term", "monthly_payment"]

        for field in fields:
            rule_data = rule_result.get(field, {})
            llm_data = llm_result.get(field, {})

            rule_value = rule_data.get("value") if isinstance(rule_data, dict) else None
            llm_value = llm_data.get("value") if isinstance(llm_data, dict) else None
            rule_conf = rule_data.get("confidence", 0) if isinstance(rule_data, dict) else 0
            llm_conf = llm_data.get("confidence", 0) if isinstance(llm_data, dict) else 0

            if rule_value == llm_value:
                final[field] = {"value": llm_value, "confidence": max(rule_conf, llm_conf), "method": "consensus"}
                logger.info(f"{field}: Both agree → {llm_value} (high confidence)")
            elif llm_conf > rule_conf:
                final[field] = {"value": llm_value, "confidence": llm_conf, "method": "llm_preferred"}
                logger.info(f"{field}: LLM preferred → {llm_value} ({llm_conf:.2f} vs {rule_conf:.2f})")
            else:
                final[field] = {"value": rule_value, "confidence": rule_conf, "method": "rule_preferred"}
                logger.info(f"{field}: Rule preferred → {rule_value} ({rule_conf:.2f} vs {llm_conf:.2f})")

        final["loan_type"] = llm_result.get("loan_type", rule_result.get("loan_type"))
        logger.info(f"Consensus complete: {len(final)} fields resolved")
        return final
