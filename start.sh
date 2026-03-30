

# Se placer dans le répertoire du script
cd "$(dirname "$0")"


xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" /home/emilien/.local/bin/uv run python main.py
