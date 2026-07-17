# Save screenshot of http://127.0.0.1:8000/ to docs/assets/
# Uses Selenium-based approach or simple PIL screenshot

import subprocess, os, time

# Launch browser maximized
url = "http://127.0.0.1:8000/"

# Use Windows Snipping Tool alternative: 
# We'll use a simple Python approach with PIL to capture the screen
# First, ensure the page is open and visible

print("Opening browser...")
os.system(f'start msedge "{url}"')

time.sleep(3)  # Wait for page to load

# Try to use PIL to capture screen
try:
    from PIL import Image, ImageGrab
    screenshot = ImageGrab.grab()
    output_path = r"D:\ai\RuyiDailyAnalysis\RuyiDailyStockAnalysis\docs\assets\readme_workspace_tour_20260717.png"
    screenshot.save(output_path)
    print(f"Screenshot saved to: {output_path}")
    print(f"Size: {screenshot.size}")
except ImportError:
    print("PIL ImageGrab not available on this platform")
except Exception as e:
    print(f"Failed: {e}")
