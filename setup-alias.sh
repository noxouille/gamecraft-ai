#!/usr/bin/env bash
# Setup convenient shell alias for GameCraft AI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up GameCraft AI alias..."

# Add to .bashrc if it exists and doesn't already have the alias
if [[ -f "$HOME/.bashrc" ]] && ! grep -q "alias gamecraft=" "$HOME/.bashrc"; then
    echo "alias gamecraft='$SCRIPT_DIR/gamecraft'" >> "$HOME/.bashrc"
    echo "✅ Added alias to ~/.bashrc"
fi

# Add to .zshrc if it exists and doesn't already have the alias
if [[ -f "$HOME/.zshrc" ]] && ! grep -q "alias gamecraft=" "$HOME/.zshrc"; then
    echo "alias gamecraft='$SCRIPT_DIR/gamecraft'" >> "$HOME/.zshrc"
    echo "✅ Added alias to ~/.zshrc"
fi

echo ""
echo "🎮 GameCraft AI is now set up with uv!"
echo ""
echo "Usage:"
echo "  gamecraft              # Start the application"
echo "  gamecraft --port 7860  # Start on custom port"
echo "  gamecraft --debug      # Start with debug mode"
echo ""
echo "Or use uv directly:"
echo "  uv run python -m src.gamecraft_ai.main"
echo ""
echo "Restart your shell or run 'source ~/.bashrc' to use the alias."
