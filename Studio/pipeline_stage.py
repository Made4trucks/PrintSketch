from abc import ABC, abstractmethod

from project_context import ProjectContext


class PipelineStage(ABC):
    """Base class for every PrintSketch pipeline stage."""

    name: str = "Unnamed stage"

    def __init__(self, context: ProjectContext) -> None:
        self.context = context

    @abstractmethod
    def is_ready(self) -> bool:
        """Return True when this stage has already been completed."""

    @abstractmethod
    def run(self) -> None:
        """Execute this pipeline stage."""

    def print_start(self) -> None:
        print()
        print("-" * 60)
        print(f"Starting stage: {self.name}")
        print("-" * 60)

    def print_skip(self) -> None:
        print(f"Skipping stage: {self.name} — already completed.")

    def print_complete(self) -> None:
        print(f"Stage completed: {self.name}")