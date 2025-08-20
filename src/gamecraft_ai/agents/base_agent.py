"""Base agent architecture for GameCraft AI agents"""

import time
from abc import ABC, abstractmethod
from typing import Any

from ..utils.logging import get_logger


class BaseAgent(ABC):
    """Base class for all GameCraft AI agents"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = get_logger(f"agents.{agent_name}")

    @abstractmethod
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process the state and return updated state

        Args:
            state: Current workflow state

        Returns:
            Updated state dictionary
        """
        pass

    def _log_start(self, operation: str) -> None:
        """Log the start of an operation"""
        self.logger.info(f"{self.agent_name} starting {operation}")

    def _log_success(self, operation: str, duration: float) -> None:
        """Log successful completion of an operation"""
        self.logger.info(f"{self.agent_name} completed {operation} in {duration:.2f}s")

    def _log_error(self, operation: str, error: Exception, duration: float) -> None:
        """Log an error during operation"""
        self.logger.error(
            f"{self.agent_name} failed {operation} after {duration:.2f}s: {str(error)}"
        )

    def _execute_with_logging(self, operation_name: str, operation_func, *args, **kwargs) -> Any:
        """Execute an operation with standardized logging

        Args:
            operation_name: Name of the operation for logging
            operation_func: Function to execute
            *args: Arguments to pass to operation_func
            **kwargs: Keyword arguments to pass to operation_func

        Returns:
            Result of operation_func

        Raises:
            Exception: Re-raises any exception from operation_func
        """
        start_time = time.time()
        self._log_start(operation_name)

        try:
            result = operation_func(*args, **kwargs)
            duration = time.time() - start_time
            self._log_success(operation_name, duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            self._log_error(operation_name, e, duration)
            raise

    def _add_error(self, state: dict[str, Any], error_message: str) -> dict[str, Any]:
        """Add an error to the state"""
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(f"{self.agent_name}: {error_message}")
        return state

    def _add_warning(self, state: dict[str, Any], warning_message: str) -> dict[str, Any]:
        """Add a warning to the state"""
        if "warnings" not in state:
            state["warnings"] = []
        state["warnings"].append(f"{self.agent_name}: {warning_message}")
        return state

    def _update_processing_step(self, state: dict[str, Any], step_name: str) -> dict[str, Any]:
        """Update the current processing step in state"""
        state["current_step"] = step_name
        if "completed_steps" not in state:
            state["completed_steps"] = []
        if step_name not in state["completed_steps"]:
            state["completed_steps"].append(step_name)
        return state


class QueryClassifierAgent(BaseAgent):
    """Enhanced query classifier agent with base agent architecture"""

    def __init__(self, llm_service, model: str = "gpt-4o-mini"):
        super().__init__("QueryClassifier")
        from ..services.llm import LLMService

        self.llm = llm_service or LLMService(model=model)

    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process query classification"""
        return self._execute_with_logging(
            "query_classification", self._classify_query_internal, state
        )

    def _classify_query_internal(self, state: dict[str, Any]) -> dict[str, Any]:
        """Internal query classification logic"""
        from ..agents.classifier import ClassifierAgent, RelevanceError

        # Use existing classifier logic
        classifier = ClassifierAgent(self.llm)

        try:
            # Update processing step
            state = self._update_processing_step(state, "classify")

            # Perform classification
            classified_state = classifier.classify_query(state)

            self.logger.info(
                f"Query classified as {classified_state['query'].query_type.value} "
                f"in {classified_state['query'].language.value}"
            )

            return classified_state

        except RelevanceError as e:
            error_msg = f"Query relevance check failed: {str(e)}"
            self.logger.warning(error_msg)
            return self._add_error(state, error_msg)
        except Exception as e:
            error_msg = f"Classification failed: {str(e)}"
            self.logger.error(error_msg)
            return self._add_error(state, error_msg)


class ResearchAgentBase(BaseAgent):
    """Base class for research agents"""

    def __init__(self, agent_name: str, igdb_service, youtube_service, cache_service):
        super().__init__(agent_name)
        self.igdb_service = igdb_service
        self.youtube_service = youtube_service
        self.cache_service = cache_service

    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process research request"""
        return self._execute_with_logging("research", self._conduct_research_internal, state)

    @abstractmethod
    def _conduct_research_internal(self, state: dict[str, Any]) -> dict[str, Any]:
        """Internal research logic - must be implemented by subclasses"""
        pass


class ScriptWriterAgentBase(BaseAgent):
    """Base class for script writing agents"""

    def __init__(self, agent_name: str, llm_service):
        super().__init__(agent_name)
        self.llm_service = llm_service

    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process script writing request"""
        return self._execute_with_logging("script_writing", self._write_script_internal, state)

    @abstractmethod
    def _write_script_internal(self, state: dict[str, Any]) -> dict[str, Any]:
        """Internal script writing logic - must be implemented by subclasses"""
        pass


class YouTubeCoachAgentBase(BaseAgent):
    """Base class for YouTube coaching agents"""

    def __init__(self, agent_name: str, llm_service):
        super().__init__(agent_name)
        self.llm_service = llm_service

    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process YouTube coaching request"""
        return self._execute_with_logging(
            "youtube_coaching", self._generate_strategies_internal, state
        )

    @abstractmethod
    def _generate_strategies_internal(self, state: dict[str, Any]) -> dict[str, Any]:
        """Internal YouTube coaching logic - must be implemented by subclasses"""
        pass
