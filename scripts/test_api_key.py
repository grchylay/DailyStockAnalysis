#!/usr/bin/env python
"""
测试 API Key 是否可用
======================
支持测试 DeepSeek、硅基流动、OpenAI 兼容接口。

用法:
  .venv\Scripts\python.exe scripts\test_api_key.py            # 用 key.txt 测全部
  .venv\Scripts\python.exe scripts\test_api_key.py deepseek   # 只测 DeepSeek
  .venv\Scripts\python.exe scripts\test_api_key.py silicon    # 只测硅基流动
  .venv\Scripts\python.exe scripts\test_api_key.py all        # 测全部
"""

import sys
from pathlib import Path

import openai

ROOT = Path(__file__).resolve().parent.parent
KEY_FILE = ROOT / "key.txt"


def load_key() -> str:
    if not KEY_FILE.exists():
        print(f"❌ key.txt 不存在: {KEY_FILE}")
        sys.exit(1)
    return KEY_FILE.read_text().strip()


def test_provider(name: str, base_url: str, model: str, api_key: str) -> bool:
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=10,
        )
        tokens = resp.usage.total_tokens
        print(f"  ✅ {name:<12} model={resp.model}  tokens={tokens}")
        return True
    except openai.AuthenticationError:
        print(f"  ❌ {name:<12} 401 Unauthorized — Key 无效或无权访问该模型")
        return False
    except openai.APIConnectionError as e:
        print(f"  ❌ {name:<12} 连接失败 — {e.__cause__ or e}")
        return False
    except Exception as e:
        print(f"  ❌ {name:<12} {type(e).__name__}: {e}")
        return False


def main():
    api_key = load_key()
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    providers = {
        "deepseek": ("https://api.deepseek.com", "deepseek-v4-flash"),
        "silicon": ("https://api.siliconflow.cn/v1", "deepseek-v4-flash"),
    }

    run_all = "all" in targets
    results = {}

    for name, (base_url, model) in providers.items():
        if run_all or name in targets:
            print(f"🔍 测试 {name} ...")
            ok = test_provider(name, base_url, model, api_key)
            results[name] = ok

    print()
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    if total == 0:
        print("⚠️  未指定要测试的 provider。可用参数: deepseek, silicon, all")
        return
    print(f"📊 结果: {passed}/{total} 通过")
    for name, ok in results.items():
        print(f"   {'✅' if ok else '❌'} {name}")


if __name__ == "__main__":
    main()
