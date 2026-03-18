import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tourism Insight Dashboard", layout="wide")

# ------------------------
# データ読み込み
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("tourism_advanced.csv")
    with open("analysis_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
    return df, report

df, report = load_data()

# ------------------------
# タイトル
# ------------------------
st.title("🌏 観光インサイトダッシュボード（Snow Monkey分析）")

# ------------------------
# KPI表示
# ------------------------
st.subheader("📊 KPIサマリー")

col1, col2, col3, col4 = st.columns(4)

col1.metric("コメント数", len(df))
col2.metric("平均ER", f"{df['EngagementRate'].mean():.4f}")
col3.metric("動画数", df['VideoID'].nunique())
col4.metric("国数", df['Lang'].nunique())

# ------------------------
# フィルター
# ------------------------
st.sidebar.header("🔍 フィルター")

selected_lang = st.sidebar.multiselect(
    "言語選択",
    options=df['Lang'].unique(),
    default=df['Lang'].unique()
)

selected_sentiment = st.sidebar.multiselect(
    "感情選択",
    options=df['Sentiment'].unique(),
    default=df['Sentiment'].unique()
)

filtered_df = df[
    (df['Lang'].isin(selected_lang)) &
    (df['Sentiment'].isin(selected_sentiment))
]

# ------------------------
# 感情分布
# ------------------------
st.subheader("😊 感情分布")

sentiment_counts = filtered_df['Sentiment'].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
st.pyplot(fig1)

# ------------------------
# 要素ランキング
# ------------------------
st.subheader("🔥 人気要素ランキング")

elements_series = (
    filtered_df['Elements']
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)

top_elements = elements_series.value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_elements.index[::-1], top_elements.values[::-1])
st.pyplot(fig2)

# ------------------------
# 意図ファネル
# ------------------------
st.subheader("🎯 来訪意図ファネル")

intent_counts = filtered_df['Intent'].value_counts()

fig3, ax3 = plt.subplots()
ax3.bar(intent_counts.index, intent_counts.values)
st.pyplot(fig3)

# ------------------------
# 国別分析
# ------------------------
st.subheader("🌍 国別感情分析")

lang_sentiment = pd.crosstab(filtered_df['Lang'], filtered_df['Sentiment'])

st.dataframe(lang_sentiment)

# ------------------------
# 動画パフォーマンス
# ------------------------
st.subheader("🎥 動画パフォーマンス")

video_perf = (
    filtered_df
    .groupby('Title')[['ViewCount', 'LikeCount', 'EngagementRate']]
    .mean()
    .sort_values(by='EngagementRate', ascending=False)
    .head(10)
)

st.dataframe(video_perf)

# ------------------------
# AIインサイト
# ------------------------
st.subheader("🧠 AIインサイト（全体）")

st.write(report["overall_insight"])

# ------------------------
# セグメントインサイト
# ------------------------
st.subheader("🌐 国別インサイト")

for lang, data in report["segment_insight"].items():
    with st.expander(f"{lang} の戦略"):
        st.write("📊 サマリー")
        st.json(data["summary"])
        st.write("💡 インサイト")
        st.write(data["insight"])

# ------------------------
# コメント表示
# ------------------------
st.subheader("💬 コメント分析（サンプル）")

st.dataframe(filtered_df[['Comment', 'Sentiment', 'Elements', 'Intent', 'Lang']].head(50))
