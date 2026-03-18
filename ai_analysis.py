import pandas as pd
import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ------------------------
# Gemini 初期化
# ------------------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def safe_gemini(prompt):
    try:
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("Gemini Error:", e)
        return ""

# ------------------------
# データ読み込み
# ------------------------
def load_data():
    try:
        df = pd.read_csv("tourism_advanced.csv")
        print("✅ データ読み込み成功")
        return df
    except Exception as e:
        print("❌ CSV読み込み失敗:", e)
        return None

# ------------------------
# 構造化サマリー作成（超重要）
# ------------------------
def create_summary(df):

    summary = {}

    # 感情分布
    summary["sentiment_counts"] = df['Sentiment'].value_counts().to_dict()

    # 要素（Top10）
    summary["top_elements"] = (
        df['Elements']
        .dropna()
        .value_counts()
        .head(10)
        .to_dict()
    )

    # 意図分布
    summary["intent_counts"] = df['Intent'].value_counts().to_dict()

    # 言語分布
    summary["lang_counts"] = df['Lang'].value_counts().to_dict()

    # エンゲージメント平均
    summary["avg_engagement_rate"] = float(df['EngagementRate'].mean())

    return summary

# ------------------------
# インサイト生成（AIの正しい使い方）
# ------------------------
def generate_insight(summary):

    prompt = f"""
    あなたは観光マーケティングの専門家です。

    以下のデータをもとに、ビジネスに使える重要な示唆を3つ出してください。

    【条件】
    ・抽象論は禁止
    ・具体的な施策レベルで書く
    ・日本語で簡潔に

    【データ】
    {summary}

    【出力形式】
    ・示唆1：
    ・示唆2：
    ・示唆3：
    """

    return safe_gemini(prompt)

# ------------------------
# セグメント別分析（強い）
# ------------------------
def generate_segment_insight(df):

    results = {}

    for lang in df['Lang'].unique():

        segment_df = df[df['Lang'] == lang]

        if len(segment_df) < 10:
            continue

        segment_summary = {
            "sentiment": segment_df['Sentiment'].value_counts().to_dict(),
            "elements": segment_df['Elements'].value_counts().head(5).to_dict(),
            "intent": segment_df['Intent'].value_counts().to_dict()
        }

        insight = safe_gemini(f"""
        以下は特定の国・言語ユーザーの分析データです。

        このユーザー層に刺さる観光戦略を1つ提案してください。

        データ：
        {segment_summary}

        簡潔に日本語で答えてください。
        """)

        results[lang] = {
            "summary": segment_summary,
            "insight": insight
        }

    return results

# ------------------------
# メイン処理
# ------------------------
def main():

    df = load_data()

    if df is None:
        return

    print("📊 サマリー作成中...")
    summary = create_summary(df)

    print("🤖 全体インサイト生成中...")
    insight = generate_insight(summary)

    print("🌍 セグメント分析中...")
    segment_insight = generate_segment_insight(df)

    # 最終出力
    result = {
        "summary": summary,
        "overall_insight": insight,
        "segment_insight": segment_insight
    }

    # JSON保存
    with open("analysis_report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ 完了：analysis_report.json 出力")

# 実行
if __name__ == "__main__":
    main()