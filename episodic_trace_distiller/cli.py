"""CLI for Episodic Trace Distiller."""
import argparse
import json
from .core import EpisodicTraceDistiller


def main():
    parser = argparse.ArgumentParser(description="Episodic Trace Distiller CLI")
    parser.add_argument("--demo", action="store_true", help="Distill a sample agent trace")
    args = parser.parse_args()

    distiller = EpisodicTraceDistiller()
    trace = [
        {"tool": "run_build", "status": "error", "error": "ENOENT config.json"},
        {"tool": "write_file", "status": "ok", "args": {"path": "config.json"}},
        {"tool": "run_build", "status": "ok"},
    ]
    print(json.dumps(distiller.distill(trace), indent=2))


if __name__ == "__main__":
    main()
