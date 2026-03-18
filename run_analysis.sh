#!/bin/bash

# エラー時に即時停止
set -e

# Pythonの警告を非表示にする（クリーンなログのため）
export PYTHONWARNINGS="ignore"

echo "------------------------------------------"
echo "🚀 Snow Monkey Analysis Pipeline Start"
echo "------------------------------------------"

# 1. データ収集 & AIメタデータ付与
echo "📥 [1/3] YouTubeデータ取得 & 感情・意図分析を実行中..."
# stderrを捨てることでライブラリの警告を隠す
python3 analysis.py 2>/dev/null

# 2. 構造化サマリー & インサイト生成
echo "🧠 [2/3] データを集計し、AI戦略レポート(JSON)を生成中..."
python3 ai_analysis.py 2>/dev/null

# 3. GitHubへの同期（成果物の選別）
echo "📤 [3/3] GitHubへソースコードと分析レポートを同期中..."

# すべてのコード修正をadd（.gitignoreによりCSVは自動除外される）
git add .

# AIが生成したレポート(JSON)は成果物として見せたいので、確実に含める
if [ -f "analysis_report.json" ]; then
    git add -f analysis_report.json
fi

# コミットとプッシュ（変更がある場合のみ）
current_time=$(date "+%Y-%m-%d %H:%M:%S")
if git commit -m "Update: Analysis Pipeline Results at ${current_time}"; then
    # リモートとの競合を防ぐためにrebaseしてからpush
    git pull origin main --rebase -X ours || (git rebase --abort && git pull origin main)
    git push origin main
    echo "✅ GitHubへの同期が完了しました。"
else
    echo "⚠️ 変更がなかったため、プッシュをスキップしました。"
fi

echo "------------------------------------------"
echo "✨ 全工程が終了しました！"
echo "Streamlitを起動してダッシュボードを確認してください。"
echo "------------------------------------------"