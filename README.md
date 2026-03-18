# 🏯 Snow Monkey Inbound Strategy Analysis Platform

地獄谷野猿公苑（Snow Monkey Park）におけるインバウンド需要を可視化・分析するためのデータパイプラインです。
YouTube APIによるデータ収集から、Gemini APIを用いた構造化分析、Streamlitによるダッシュボード表示までを自動化しています。

## 🚀 システム概要

本プロジェクトは、観光地に対する海外ユーザーの生の声を収集し、感情分析のみではなく、具体的な施策立案を支援することを目的としています。


### 🏗️ テクニカルスタック
- **Language:** Python 3.9+
- **Data Collection:** YouTube Data API v3
- **AI / NLP:** Google Gemini 2.0 Flash (Generative AI)
- **Data Visualization:** Streamlit, Matplotlib, Seaborn
- **Infrastructure / Automation:** Bash Shell Script, Git, GitHub

## 🛠️ パイプラインの構成

本プラットフォームは以下の3つのコンポーネントで構成されています。

1.  **データ収集層 (`analysis.py`)**
    - YouTubeから特定のキーワードで動画を検索し、コメントおよびエンゲージメント統計（再生数、高評価数）を取得。
    - 各コメントに対し、AIが「感情（Sentiment）」「観光要素（Elements）」「来訪意図（Intent）」をリアルタイムでメタデータ化。
2.  **分析・集計層 (`ai_analysis.py`)**
    - 収集したデータを構造化（JSON化）し、言語セグメント別のインサイトを生成。
    - 経営判断に直結する3つの具体的なビジネス示唆をAIが立案。
3.  **可視化層 (`app.py`)**
    - 抽出されたインサイトと統計データをダッシュボードで表示。
    - フィルター機能により、特定の国や感情に絞った深掘り分析が可能。

## 🔒 セキュリティとコンプライアンス

- **データ保護:** YouTube APIの利用規約およびプライバシー保護の観点から、コメント生データを含むCSVファイルはリポジトリに含めず、`.gitignore` により除外しています。
- **成果物の管理:** AIによって生成された二次的な分析結果（`analysis_report.json`）のみをGitHub上で構成管理の対象としています。

## 🏃‍♂️ セットアップと実行
```
chmod +x run_analysis.sh

# データ取得・分析
./run_analysis.sh

#　ダッシュボードの起動
streamlit run app.py
```

### 環境変数の設定
`.env` ファイルを作成し、以下のキーを設定してください。
```env
YOUTUBE_API_KEY=あなたのYouTube_APIキー
GEMINI_API_KEY=あなたのGemini_APIキー
```

### 更新履歴
- **2026/03/18 README.md更新**