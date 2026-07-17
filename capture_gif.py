"""Capture DSA Web frames with visible changes for a proper GIF."""
import time, os
from pathlib import Path

try:
    from PIL import Image, ImageGrab
except ImportError:
    print("Pillow required")
    exit(1)

output_dir = Path(r"D:\ai\RuyiDailyAnalysis\RuyiDailyStockAnalysis\docs\assets")
output_dir.mkdir(parents=True, exist_ok=True)

# First open the page
url = "http://127.0.0.1:8000/"
os.system(f'start msedge "{url}"')
time.sleep(4)

# Take screenshots at different timings to capture potential animations/ui changes
frames = []
print("Capturing 8 frames over 20 seconds...")

for i in range(8):
    try:
        screenshot = ImageGrab.grab()
        screenshot = screenshot.resize((1280, 800), Image.LANCZOS)
        frames.append(screenshot)
        print(f"  Frame {i+1}/8")
    except Exception as e:
        print(f"  Frame {i+1} failed: {e}")
    time.sleep(1.5)

if len(frames) >= 2:
    gif_path = output_dir / "readme_workspace_tour_20260717.gif"
    frames[0].save(
        str(gif_path),
        save_all=True,
        append_images=frames[1:],
        duration=1200,
        loop=0,
        optimize=False,
    )
    size_kb = gif_path.stat().st_size / 1024
    print(f"\n✅ GIF: {gif_path} ({size_kb:.0f} KB, {len(frames)} frames)")
else:
    print("Not enough frames!")
