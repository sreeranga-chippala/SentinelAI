"""
agents/base_agent.py

Abstract Base Class for all SentinelAI agents.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, logger=None):

        self.logger = logger

    # ----------------------------------------------------------

    @property
    def name(self):

        return self.__class__.__name__

    # ----------------------------------------------------------

    def log(self, message: str):

        if self.logger:

            self.logger.log(
                f"[{self.name}] {message}"
            )

        else:

            print(
                f"[{self.name}] {message}"
            )

    # ----------------------------------------------------------

    def before_run(self):

        self.log("Started")

    # ----------------------------------------------------------

    def after_run(self):

        self.log("Completed")

    # ----------------------------------------------------------

    @abstractmethod
    def run(self):

        """
        Execute the agent.

        Returns
        -------
        object
            Agent-specific result.
        """
        pass