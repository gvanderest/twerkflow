"""Main entry point for the Twerkflow."""

import argparse
from src.core.driver_factory import DriverFactory
from src.workflows.hydration_flow import app
from src.services.hydration_watcher import HydrationWatcher, HydrationWatcherConfig


def run_watcher_app(iterations: int = 0, watcher_class=HydrationWatcher):
    """Executes the hydration watcher."""
    factory = DriverFactory()
    config = HydrationWatcherConfig(factory=factory, app=app)
    watcher = watcher_class(config)
    watcher.run_watcher(iterations=iterations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twerkflow Hydration Watcher")
    parser.add_argument("--iterations", type=int, default=0, help="Number of iterations to run (0 for infinite)")
    args = parser.parse_args()

    # Test: Run hydration (should find tagged issues)
    print(f"--- Starting Hydration Watcher (iterations: {args.iterations or 'infinite'}) ---")
    run_watcher_app(iterations=args.iterations)
