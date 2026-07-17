"""Generate an animated GIF illustration of the DSA Web interface using Pillow drawing."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1280, 720
FRAMES = 12

# Colors
BG_DARK = (15, 23, 42)
CARD_BG = (30, 41, 59, 200)
SIDEBAR_BG = (30, 41, 59, 230)
ACCENT = (56, 189, 248)
GOLD = (251, 191, 36)
TEXT = (226, 232, 240)
TEXT_MUTED = (100, 116, 139)
GREEN = (52, 211, 153)
RED = (248, 113, 113)

def draw_frame(t):
    """Draw one frame at time t (0..1)."""
    img = Image.new("RGBA", (W, H), BG_DARK + (255,))
    draw = ImageDraw.Draw(img)

    # === Sidebar ===
    draw.rectangle([0, 0, 220, H], fill=SIDEBAR_BG)
    # Logo circle
    cx, cy = 110, 60
    r = 20
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=ACCENT)
    draw.text((cx-6, cy-7), "R", fill=TEXT)
    draw.text((40, 90), "如意金股", fill=TEXT)
    draw.text((40, 108), "RuyiDailyStockAnalysis", fill=TEXT_MUTED)
    draw.text((40, 122), "柯冰妍", fill=(TEXT_MUTED[0], TEXT_MUTED[1], TEXT_MUTED[2], 100))

    # Nav items
    nav_items = ["🏠 首页", "💬 策略问股", "📊 选股", "💼 持仓", "📈 信号", "🔄 回测", "🔔 告警", "📊 用量", "⚙ 设置"]
    for i, item in enumerate(nav_items):
        y = 160 + i * 36
        if i == 0:
            draw.rectangle([10, y-4, 210, y+24], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 30))
        draw.text((30, y), item, fill=TEXT if i == 0 else TEXT_MUTED)

    # === Header (search bar) ===
    header_h = 56
    draw.rectangle([220, 0, W, header_h], fill=(CARD_BG[0], CARD_BG[1], CARD_BG[2], 180))
    # Search input
    draw.rectangle([240, 12, 500, 44], fill=(15, 23, 42, 200), outline=(ACCENT[0], ACCENT[1], ACCENT[2], 100))
    draw.text((250, 22), "🔍 600519  贵州茅台", fill=TEXT_MUTED)
    # Buttons
    draw.rectangle([520, 12, 600, 44], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 200))
    draw.text((530, 22), "📋 分析", fill=TEXT)
    draw.rectangle([620, 12, 700, 44], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 100))
    draw.text((630, 22), "🌐 大盘", fill=TEXT)
    # Theme toggle
    draw.ellipse([W-50, 14, W-20, 42], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 100))
    draw.text((W-40, 22), "🌙", fill=TEXT)

    # === Main content area ===
    content_x = 240
    content_y = 72
    content_w = W - 260

    # === Report Overview ===
    # Stock header card
    draw.rounded_rectangle([content_x, content_y, content_x + content_w, content_y + 110], 
                           radius=12, fill=CARD_BG)
    # Stock name + price
    draw.text((content_x + 20, content_y + 16), "贵州茅台 600519", fill=TEXT, font=None)
    draw.text((content_x + 20, content_y + 44), "1,253.00", fill=GREEN, font=None)
    draw.text((content_x + 130, content_y + 48), "-0.48%", fill=RED, font=None)
    draw.text((content_x + 20, content_y + 74), "2026-07-17 · A股 · 盘后", fill=TEXT_MUTED)

    # Score gauge on the right
    gauge_x = content_x + content_w - 160
    draw.ellipse([gauge_x, content_y + 20, gauge_x + 80, content_y + 100], 
                 outline=ACCENT, width=3)
    draw.text((gauge_x + 24, content_y + 50), "65", fill=ACCENT, font=None)

    # === Action Advice + Trend ===
    adv_y = content_y + 130
    card_w = (content_w - 20) // 2
    
    # Buy card
    draw.rounded_rectangle([content_x, adv_y, content_x + card_w, adv_y + 70],
                           radius=12, fill=CARD_BG)
    draw.text((content_x + 16, adv_y + 12), "📋 操作建议", fill=GREEN)
    draw.text((content_x + 16, adv_y + 36), "多头排列延续，建议观望", fill=TEXT)
    
    # Trend card
    draw.rounded_rectangle([content_x + card_w + 20, adv_y, content_x + content_w, adv_y + 70],
                           radius=12, fill=CARD_BG)
    draw.text((content_x + card_w + 36, adv_y + 12), "📈 趋势预测", fill=GOLD)
    draw.text((content_x + card_w + 36, adv_y + 36), "看多 · 评分 65", fill=TEXT)

    # === Technical indicators (k-line bars) ===
    tech_y = adv_y + 90
    draw.rounded_rectangle([content_x, tech_y, content_x + content_w, tech_y + 130],
                           radius=12, fill=CARD_BG)
    draw.text((content_x + 16, tech_y + 10), "📊 技术指标", fill=TEXT)
    
    # Animated K-line bars
    bar_base_x = content_x + 40
    bar_base_y = tech_y + 80
    for i in range(20):
        bx = bar_base_x + i * 28
        # Bar height animates slightly
        bh = int(20 + 30 * abs(t - i/20) + 15 * (i % 3))
        bar_color = GREEN if i % 3 != 1 else RED
        draw.rectangle([bx, bar_base_y - bh, bx + 8, bar_base_y], fill=bar_color)
        # Wick
        draw.line([(bx+4, bar_base_y - bh - 6), (bx+4, bar_base_y)], fill=bar_color, width=2)

    # MA lines (animated)
    for j in range(3):
        pts = []
        for i in range(20):
            x = bar_base_x + i * 28 + 4
            y = bar_base_y - 15 - int(20 * (0.3 + 0.3 * (i/20) + 0.1 * t + 0.05 * j))
            pts.append((x, y))
        draw.line(pts, fill=ACCENT if j == 0 else (GOLD if j == 1 else TEXT_MUTED), width=2)

    # === Right rail - Sentiment ===
    rail_x = content_x + content_w + 15
    if rail_x < W - 15:
        draw.rounded_rectangle([rail_x, content_y, W - 15, content_y + 250],
                               radius=12, fill=CARD_BG)
        draw.text((rail_x + 10, content_y + 12), "📊 市场情绪", fill=TEXT)
        draw.ellipse([rail_x + 25, content_y + 50, rail_x + 105, content_y + 130],
                     outline=ACCENT, width=3)
        draw.text((rail_x + 50, content_y + 80), "65", fill=ACCENT)
        draw.text((rail_x + 10, content_y + 145), "评分 看多", fill=GREEN)
        draw.text((rail_x + 10, content_y + 165), "MA5 1237.78", fill=TEXT_MUTED)
        draw.text((rail_x + 10, content_y + 185), "MA10 1217.11", fill=TEXT_MUTED)
        draw.text((rail_x + 10, content_y + 205), "MA20 1204.11", fill=TEXT_MUTED)
        draw.rounded_rectangle([rail_x + 10, content_y + 290, rail_x + 130, content_y + 320],
                               radius=8, fill=GOLD)
        draw.text((rail_x + 30, content_y + 298), "⭐ 加入自选", fill=BG_DARK)

    return img

frames = []
print("Generating animation frames...")
for i in range(FRAMES):
    t = i / FRAMES
    frame = draw_frame(t)
    frames.append(frame)
    print(f"  Frame {i+1}/{FRAMES}")

output = r"D:\ai\RuyiDailyAnalysis\RuyiDailyStockAnalysis\docs\assets\readme_workspace_tour_20260717.gif"
frames[0].save(output, save_all=True, append_images=frames[1:], 
               duration=150, loop=0, optimize=True, disposal=2)
print(f"\n✅ GIF saved: {output} ({os.path.getsize(output)/1024:.0f} KB)")
