import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env 読み込み
load_dotenv(override=True)

# Foundry接続
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")

# SDK用URL
base_url = endpoint.removesuffix("/responses") + "/"

client = OpenAI(
    base_url=base_url,
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")

# -----------------------
# 画面
# -----------------------

st.set_page_config(
    page_title="価値観ナビゲーター",
    page_icon="🌱"
)

st.title("🌱 価値観ナビゲーター")

st.info(
    """
好きなことや疲れることから、
今のあなたが大切にしている価値観を整理します。
"""
)

# -----------------------
# 入力
# -----------------------

happy_text = st.text_area(
    "① 最近ちょっと嬉しかったことを3つ教えてください",
    height=120,
    placeholder="""
例：
・AIの勉強が進んだ
・友人と楽しく話した
・散歩で気分転換できた
"""
)

tired_text = st.text_area(
    "② 逆に『これは疲れるな』と感じることを3つ教えてください",
    height=120,
    placeholder="""
例：
・意味の見えない作業
・急な予定変更
・細かく管理されること
"""
)

# -----------------------
# 分析ボタン
# -----------------------

if st.button("🔍 価値観を分析する"):

    if not happy_text.strip() or not tired_text.strip():

        st.warning("両方入力してください。")

    else:

        prompt = f"""
以下の内容から価値観を整理してください。

【嬉しかったこと】
{happy_text}

【疲れること】
{tired_text}

次の形式で回答してください。

【見えてきたあなたが大切にしていること】

【自己決定理論からの考察】

・自律性
・有能感
・関係性

【おすすめの小さな一歩】

分析は決めつけず、
「〜かもしれません」
「〜という可能性があります」
という表現を使ってください。

やさしく、前向きな文章にしてください。
"""

        try:

            with st.spinner("価値観を整理しています..."):

                response = client.responses.create(
                    model=model,
                    input=prompt,
                    max_output_tokens=4000,
                    reasoning={
                        "effort": "low"
                    }
                )

                answer = response.output_text

            st.success("分析が完了しました")

            st.markdown(answer)

        except Exception as e:

            st.error(f"APIエラー: {e}")