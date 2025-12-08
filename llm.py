from abc import ABC, abstractmethod


class LLMAnalyzer(ABC):

    @abstractmethod
    def analyze(self, prompt):
        pass

    @abstractmethod
    def get_name(self):
        pass
