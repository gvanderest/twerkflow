"""Runner for hydration watcher service."""
from typing import Any
from src.core.driver_factory import DriverFactory
from src.workflows.hydration_flow import app
from src.services.hydration_watcher import HydrationWatcher, HydrationWatcherConfig


def run_watcher_app(iterations: int = 0, watcher_class: Any = HydrationWatcher) -> None:
    """Executes the hydration watcher."""
    factory = DriverFactory()
    config = HydrationWatcherConfig(factory=factory, app=app)
    watcher = watcher_class(config)
    watcher.run_watcher(iterations=iterations)
