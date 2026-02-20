import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class PipelineMonitor:
    """Tracks pipeline performance, LLM calls, and costs."""

    def __init__(self):
        self.traces = []
        self.start_time = None
        logger.info("Pipeline monitor initialized")

    def start_trace(self, document_id):
        """Start tracking a pipeline run."""
        self.start_time = time.time()
        self.current_trace = {
            "document_id": document_id,
            "started_at": datetime.now().isoformat(),
            "steps": [],
            "llm_calls": [],
            "total_tokens": 0,
            "total_cost": 0.0
        }
        logger.info(f"Trace started for {document_id}")

    def log_step(self, step_name, duration_ms, status="success"):
        """Log a pipeline step."""
        step = {
            "step": step_name,
            "duration_ms": round(duration_ms, 2),
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.current_trace["steps"].append(step)
        logger.info(f"MONITOR | {step_name}: {duration_ms:.0f}ms ({status})")

    def log_llm_call(self, model, input_tokens, output_tokens):
        """Track LLM API call and cost."""
        # GPT-4 pricing (approximate)
        costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "claude": {"input": 0.015, "output": 0.075},
            "mock": {"input": 0.0, "output": 0.0}
        }

        model_cost = costs.get(model, costs["mock"])
        call_cost = (input_tokens / 1000 * model_cost["input"]) + \
                    (output_tokens / 1000 * model_cost["output"])

        llm_call = {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": round(call_cost, 6),
            "timestamp": datetime.now().isoformat()
        }
        self.current_trace["llm_calls"].append(llm_call)
        self.current_trace["total_tokens"] += input_tokens + output_tokens
        self.current_trace["total_cost"] += call_cost
        logger.info(f"MONITOR | LLM call: {model} | tokens: {input_tokens}+{output_tokens} | cost: ${call_cost:.4f}")

    def end_trace(self):
        """End tracking and return summary."""
        duration = time.time() - self.start_time
        self.current_trace["total_duration_ms"] = round(duration * 1000, 2)
        self.current_trace["ended_at"] = datetime.now().isoformat()
        self.traces.append(self.current_trace)

        logger.info(f"MONITOR | Pipeline complete: {duration*1000:.0f}ms | "
                     f"tokens: {self.current_trace['total_tokens']} | "
                     f"cost: ${self.current_trace['total_cost']:.4f}")
        return self.current_trace
