#!/bin/bash

echo "--- FPSプロジェクト 整合性チェック開始 ---"

# 1. ディレクトリ構成の確認
echo "[1/4] ディレクトリ確認..."
for dir in core data assets/sounds; do
    if [ -d "$dir" ]; then
        echo "  OK: $dir が存在します。"
    else
        echo "  NG: $dir が見つかりません！"
    fi
done

# 2. ファイルの存在確認
echo -e "\n[2/4] ファイル存在確認..."
FILES=("core/engine.py" "core/raycaster.py" "core/weapon.py" "core/enemy.py" "core/player.py" "core/map.py")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  OK: $file が存在します。"
    else
        echo "  NG: $file が欠落しています！"
    fi
done

# 3. インポートと引数の整合性チェック（簡易静的解析）
echo -e "\n[3/4] コードの整合性チェック..."

# Enemyのインポートがあるか
if grep -q "from core.enemy import Enemy" core/engine.py; then
    echo "  OK: engine.py で Enemy がインポートされています。"
else
    echo "  NG: engine.py で Enemy のインポートが漏れています！"
fi

# Raycaster.castの引数が3つ（player, enemies, bullets）あるか
CAST_ARGS=$(grep "def cast" core/raycaster.py)
if [[ $CAST_ARGS == *"player"* && $CAST_ARGS == *"enemies"* && $CAST_ARGS == *"bullets"* ]]; then
    echo "  OK: raycaster.py の cast メソッドは最新です。"
else
    echo "  NG: raycaster.py の cast の引数が古いです！: $CAST_ARGS"
fi

# engine.pyからの呼び出し側も3つか
CALL_ARGS=$(grep "self.renderer.cast" core/engine.py)
if [[ $CALL_ARGS == *"self.player"* && $CALL_ARGS == *"self.enemies"* && $CALL_ARGS == *"self.bullets"* ]]; then
    echo "  OK: engine.py からの呼び出し引数は最新です。"
else
    echo "  NG: engine.py からの呼び出し引数が古いです！: $CALL_ARGS"
fi

# 4. 実行テスト
echo -e "\n[4/4] Python実行テスト..."
python3 -c "import pygame; import numpy; print('  OK: pygame と numpy はインストールされています。')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  NG: pygame か numpy が入っていません。'pip install pygame numpy' を試してください。"
fi

echo -e "\n--- チェック完了 ---"
