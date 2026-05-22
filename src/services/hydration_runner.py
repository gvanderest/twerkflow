"""Runner for hydration watcher service."""

from src.core.driver_factory import DriverFactory
from src.workflows.hydration_flow import app
from src.services.hydration_watcher import HydrationWatcher, HydrationWatcherConfig


def run_watcher_app(iterations: int = 0, watcher_class=HydrationWatcher):
    """Executes the hydration watcher."""
    factory = DriverFactory()
    config = HydrationWatcherConfig(factory=factory, app=app)
    watcher = watcher_class(config)
    watcher.run_watcher(iterations=iterations)
