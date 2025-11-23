from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional

class BaseLLMService(ABC):
    @abstractmethod
    def get_llm(self) -> Any:
        """Return the underlying LLM object."""
        pass

class BaseVectorStore(ABC):
    @abstractmethod
    def ingest_text(self, text: str, source: str) -> int:
        """Ingest text into the vector store."""
        pass

    @abstractmethod
    def get_retriever(self) -> Any:
        """Return the retriever object."""
        pass

class BaseAgent(ABC):
    @abstractmethod
    def process_message(self, message: str, history: List[Dict[str, str]]) -> str:
        """Process a user message and return a response."""
        pass
