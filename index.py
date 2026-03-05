#!/usr/bin/env python3
import os, sys, json
import pygame

# 実行環境の固定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

from core.engine import GameEngine

def main():
    # 1. データの読み込み
    try:
        with open('data/config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json が見つかりません。")
        sys.exit(1)

    # 2. エンジンの起動
    engine = GameEngine(config)
    engine.run()

if __name__ == "__main__":
    main()
