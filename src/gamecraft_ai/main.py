#!/usr/bin/env python3
"""
GameCraft AI - Main Application Entry Point

This module provides the main entry point for the GameCraft AI Gradio web interface.
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .config import settings  # noqa: E402
from .ui.app import create_gradio_app  # noqa: E402
from .utils.logging import get_logger, setup_logging  # noqa: E402


def run_gradio_app():
    """Run the Gradio web interface"""
    logger = get_logger(__name__)
    logger.info("Starting GameCraft AI Gradio interface...")

    try:
        app = create_gradio_app()
        app.launch(
            server_name=settings.host,
            server_port=settings.port,
            share=False,
            debug=settings.debug,
            show_error=settings.debug,
        )
    except Exception as e:
        logger.error(f"Failed to start Gradio app: {e}")
        sys.exit(1)


def main():
    """Main entry point with command line argument parsing"""
    parser = argparse.ArgumentParser(description="GameCraft AI - Gaming Content Script Generator")
    parser.add_argument(
        "--host", default=settings.host, help=f"Host to bind to (default: {settings.host})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port to bind to (default: {settings.port})",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Update settings from CLI args
    settings.host = args.host
    settings.port = args.port
    settings.debug = args.debug

    # Setup logging
    setup_logging(
        level="DEBUG" if settings.debug else settings.log_level, log_file=settings.log_file
    )

    logger = get_logger(__name__)
    logger.info("Starting GameCraft AI Gradio interface")
    logger.info(f"Server: {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")

    # Run Gradio app
    run_gradio_app()


if __name__ == "__main__":
    main()
