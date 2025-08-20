"""
Tests for the main application module
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.main import main, run_gradio_app  # noqa: E402


def test_main_function_exists():
    """Test that main function exists and can be imported"""
    assert callable(main)
    assert callable(run_gradio_app)


def test_main_with_default_args():
    """Test main function with default arguments"""
    with patch("src.gamecraft_ai.main.run_gradio_app") as mock_run:
        with patch("sys.argv", ["main.py"]):
            try:
                main()
            except SystemExit:
                pass  # Expected when app tries to launch
        mock_run.assert_called_once()


def test_main_with_custom_args():
    """Test main function with custom arguments"""
    with patch("src.gamecraft_ai.main.run_gradio_app") as mock_run:
        with patch("sys.argv", ["main.py", "--host", "0.0.0.0", "--port", "8080", "--debug"]):
            try:
                main()
            except SystemExit:
                pass  # Expected when app tries to launch
        mock_run.assert_called_once()


@patch("src.gamecraft_ai.main.create_gradio_app")
def test_run_gradio_app_success(mock_create_app):
    """Test successful Gradio app launch"""
    mock_app = Mock()
    mock_create_app.return_value = mock_app

    with patch("src.gamecraft_ai.main.settings") as mock_settings:
        mock_settings.host = "127.0.0.1"
        mock_settings.port = 7860
        mock_settings.debug = False

        try:
            run_gradio_app()
        except SystemExit:
            pass  # Expected when mock app launches

        mock_app.launch.assert_called_once()


@patch("src.gamecraft_ai.main.create_gradio_app")
def test_run_gradio_app_failure(mock_create_app):
    """Test Gradio app launch failure"""
    mock_create_app.side_effect = Exception("Test error")

    with patch("sys.exit") as mock_exit:
        run_gradio_app()
        mock_exit.assert_called_once_with(1)
