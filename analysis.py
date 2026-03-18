import os
import pandas as pd
from googleapiclient.discovery import build
from google import genai
from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

# API初期化
youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ------------------------
# AI系関数
# ------------------------

def safe_gemini(prompt):
    try:
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except:
        return ""

# 感情分析
def get_sentiment(text):
    result = safe_gemini(f"""
    以下のコメントの感情を1単語で分類：
    Positive / Negative / Neutral
    
    コメント：
    {text}
    """)
    return result if result in ['Positive', 'Negative', 'Neutral'] else 'Neutral'

# 要素抽出（最重要）
def extract_elements(text):
    result = safe_gemini(f"""
    以下のコメントから観光的要素を最大3つ抽出し、
    英語の単語でカンマ区切りで出力：
    
    例：
    monkey, snow, onsen
    
    コメント：
    {text}
    """)
    return result

# 来訪意図分析
def classify_intent(text):
    result = safe_gemini(f"""
    このコメントの旅行意図を分類：
    
    Desire（行きたい）
    Plan（行く予定）
    Visit（行った）
    None
    
    1単語のみで回答
    
    コメント：
    {text}
    """)
    return result if result in ['Desire', 'Plan', 'Visit', 'None'] else 'None'

# 言語判定
def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"

# ------------------------
# メイン処理
# ------------------------

def main():

    # ①動画検索
    search_response = youtube.search().list(
        q='Snow Monkey Park Jigokudani',
        part='id',
        maxResults=3, ##5→3に変更
        type='video'
    ).execute()

    all_data = []

    for item in search_response['items']:
        video_id = item['id']['videoId']

        # ②動画情報取得
        video_res = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        stats = video_res['items'][0]['statistics']
        snippet = video_res['items'][0]['snippet']

        view = int(stats.get('viewCount', 0))
        like = int(stats.get('likeCount', 0))
        comment_count = int(stats.get('commentCount', 0))
        title = snippet.get('title', '')

        # ③コメント取得
        comments_res = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=20  ## 50→20に変更
        ).execute()

        for c in comments_res['items']:
            comment = c['snippet']['topLevelComment']['snippet']['textDisplay']

            all_data.append({
                'VideoID': video_id,
                'Title': title,
                'ViewCount': view,
                'LikeCount': like,
                'CommentCount': comment_count,
                'Comment': comment
            })

    # DataFrame化
    df = pd.DataFrame(all_data)

    print("🤖 AI分析開始...（お待ちください）")

    # ④AI分析
    df['Sentiment'] = df['Comment'].apply(get_sentiment)
    df['Elements'] = df['Comment'].apply(extract_elements)
    df['Intent'] = df['Comment'].apply(classify_intent)
    df['Lang'] = df['Comment'].apply(detect_lang)

    # ⑤エンゲージメント率
    df['EngagementRate'] = (df['LikeCount'] / df['ViewCount']).fillna(0)

    # 保存
    df.to_csv('tourism_advanced.csv', index=False)

    print("✅ 完了：tourism_advanced.csv")

# 実行
if __name__ == "__main__":
    main()