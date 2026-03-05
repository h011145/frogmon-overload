import os
import subprocess

def generate_readme():
    content = """# 🐸 Frogmon Overload: System Overload Edition

![Language](https://img.shields.io/badge/language-python-blue.svg)
![Library](https://img.shields.io/badge/library-pygame-green.svg)

AIとターミナルだけで構築された、ハイテンポなレイキャスティングFPS。

## 🚀 特徴
- **爆速BGM**: "System Overload.mp3" をバックグラウンドに採用。
- **動的パーティクル**: 敵命中時に火花が散るエフェクトシステム。
- **シンセSE**: NumPyを使用して波形から直接生成されたマシンガン発射音。
- **進化する難易度**: 撃破数に応じてカエル男の移動速度が上昇。

## 🕹 遊び方
1. `pip install pygame numpy`
2. `python3 index.py`
3. マウスで狙って左クリックで射撃！

---
*Created by Hiroshi with AI Coordinator*
"""
    with open("README.md", "w") as f:
        f.write(content)
    print("✓ README.md has been generated.")

def deploy_to_github():
    try:
        # READMEを追加してコミット・プッシュ
        subprocess.run(["git", "add", "README.md", "coordinator.py"], check=True)
        subprocess.run(["git", "commit", "-m", "docs: update README and add coordinator script"], check=True)
        # origin master へプッシュ
        subprocess.run(["git", "push", "origin", "master"], check=True)
        print("✓ Successfully pushed to GitHub!")
    except Exception as e:
        print(f"Error during deployment: {e}")

if __name__ == "__main__":
    generate_readme()
    deploy_to_github()
