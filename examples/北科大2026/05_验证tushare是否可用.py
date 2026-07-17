"""
验证 Tushare API Key 是否可用
==============================
读取 key.txt 中的 Tushare Token，验证连接和基本接口可用性。

用法:
  .venv\Scripts\python.exe examples\北科大2026\05_验证tushare是否可用.py

依赖:
  pip install tushare
"""

import sys
from pathlib import Path

# 定位项目根目录
ROOT = Path(__file__).resolve().parent.parent.parent
KEY_FILE = ROOT / "key.txt"


def _read_tushare_token() -> str:
    """从 key.txt 中读取 Tushare token。"""
    if not KEY_FILE.exists():
        print(f"❌ key.txt 不存在: {KEY_FILE}")
        sys.exit(1)

    content = KEY_FILE.read_text(encoding="utf-8")
    # key.txt 格式：每行一对 "标识\nkey"
    # 查找 "tushare" 标记后的下一行
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    for i, line in enumerate(lines):
        if line.lower() == "tushare" and i + 1 < len(lines):
            return lines[i + 1]

    print("❌ key.txt 中未找到 tushare token，请确认格式为：")
    print("   tushare")
    print("   你的token")
    sys.exit(1)


def main():
    import tushare as ts

    token = _read_tushare_token()
    print(f"🔍 读取到 Tushare Token: {token[:6]}...{token[-4:]}")
    print()

    # ── 测试 1：设置 token（Pro 版鉴权） ──
    print("=" * 50)
    print("测试 1: Pro API 鉴权")
    print("=" * 50)
    try:
        pro = ts.pro_api(token)
        # 用最轻量的接口测试 token 有效性
        # 注意：不同积分等级可用的接口不同，此处仅测试鉴权是否通过
        try:
            df = pro.query("trade_cal", exchange="SSE",
                           start_date="20260701", end_date="20260716")
            print(f"  ✅ Pro API 连接成功（trade_cal）: {len(df)} 条")
        except Exception as e:
            msg = str(e)
            if "没有接口" in msg or "无权限" in msg:
                print(f"  ⚠️  Pro API 鉴权通过，但当前 Token 积分不足，无法调用高级接口")
                print(f"     提示: {msg.split('。')[0]}。")
            else:
                print(f"  ❌ Pro API 调用失败: {e}")

    except Exception as e:
        print(f"  ❌ Pro API 初始化失败: {e}")

    print()

    # ── 测试 2：旧版实时行情（免费，无需积分） ──
    print("=" * 50)
    print("测试 2: 旧版实时行情接口")
    print("=" * 50)
    try:
        df = ts.get_realtime_quotes("000001")
        if df is not None and not df.empty:
            code = df.iloc[0].get("code", "N/A")
            name = df.iloc[0].get("name", "N/A")
            price = df.iloc[0].get("price", "N/A")
            high = df.iloc[0].get("high", "N/A")
            low = df.iloc[0].get("low", "N/A")
            volume = df.iloc[0].get("volume", "N/A")
            print(f"  ✅ 平安银行(000001) 实时行情获取成功:")
            print(f"     名称: {name}")
            print(f"     最新价: {price}")
            print(f"     最高: {high}  最低: {low}")
            print(f"     成交量: {volume}")
        else:
            print(f"  ❌ 返回数据为空")
    except Exception as e:
        print(f"  ❌ 实时行情接口调用失败: {e}")

    print()

    # ── 测试 3：设置到项目 .env ──
    print("=" * 50)
    print("测试 3: .env 配置检查")
    print("=" * 50)
    env_path = ROOT / ".env"
    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
        if "TUSHARE_TOKEN" in content:
            print(f"  ✅ .env 中已包含 TUSHARE_TOKEN 配置项")
        else:
            print(f"  ⚠️  .env 中未配置 TUSHARE_TOKEN")
            print(f"     如需使用，可添加: TUSHARE_TOKEN={token[:6]}...{token[-4:]}")
    else:
        print(f"  ⚠️  .env 文件不存在")

    print()
    print("=" * 50)
    print("✅ Tushare Token 验证完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
