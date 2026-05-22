"""Main entry point for the Twerkflow."""

import argparse
from src.services.hydration_runner import run_watcher_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twerkflow Hydration Watcher")
    parser.add_argument("--iterations", type=int, default=0, help="Number of iterations to run (0 for infinite)")
    args = parser.parse_args()

    # Test: Run hydration (should find tagged issues)
    print(f"--- Starting Hydration Watcher (iterations: {args.iterations or 'infinite'}) ---")
    run_watcher_app(iterations=args.iterations)
