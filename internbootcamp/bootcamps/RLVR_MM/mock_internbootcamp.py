from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseInstructionGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def case_generator(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def prompt_func(self, identity: Dict[str, Any]) -> str:
        pass

class BaseRewardCalculator(ABC):
    @staticmethod
    @abstractmethod
    def extract_output(output_str: str):
        pass

    @classmethod
    @abstractmethod
    def _verify_correction(cls, extract_solution, identity: dict, **kwargs) -> float:
        pass
