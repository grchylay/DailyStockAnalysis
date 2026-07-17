"""Capture DSA Web page frames and save as GIF using PIL ImageGrab."""
import time, os
from pathlib import Path

try:
    from PIL import Image, ImageGrab
except ImportError:
    print("Pillow required")
    exit(1)

url = "http://127.0.0.1:8000/"
os.system(f'start msedge "{url}"')
time.sleep(3)

output_dir = Path(r"D:\ai\RuyiDailyAnalysis\RuyiDailyStockAnalysis\docs\assets")
output_dir.mkdir(parents=True, exist_ok=True)

frames = []
print("Capturing frames (will take ~12s)...")

for i in range(6):
    try:
        screenshot = ImageGrab.grab()
        screenshot = screenshot.resize((1280, 800), Image.LANCZOS)
        frames.append(screenshot)
        print(f"  Frame {i+1}/6")
    except Exception as e:
        print(f"  Frame {i+1} failed: {e}")
    time.sleep(1.2)

if frames:
    gif_path = output_dir / "readme_workspace_tour_20260717.gif"
    frames[0].save(
        str(gif_path),
        save_all=True,
        append_images=frames[1:],
        duration=1000,
        loop=0,
        optimize=True,
    )
    size_kb = gif_path.stat().st_size / 1024
    print(f"\n✅ GIF saved: {gif_path} ({size_kb:.0f} KB, {len(frames)} frames)")
else:
    print("No frames captured!")
