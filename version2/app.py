import openai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#ファイルの読み込み
file = st.file_uploader("m4aファイルをアップロードしてください", type=["m4a"])

# ファイルがアップロードされた場合にのみ処理を実行する
if file is not None:
    # ファイル名を取得する
    filename = file.name
    
    # ファイルの内容を読み込む
    file_content = file.read()
    
    # 読み込んだ内容をそのまま別のファイルに書き出す
    with open("output.m4a", "wb") as f:
        f.write(file_content)

#ファイルがない状態で読み込まれるとエラーとなる
if os.path.exists("output.m4a"):
    with open("output.m4a", "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
        transcript = response["text"]
    print("書き起こし")
    print(response["text"])
    st.write("書き起こし")
    st.write(response["text"])

    res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=1000,
    temperature=0.8,
    top_p=1,
    n = 1,
    stream=False,
    presence_penalty=0,
    frequency_penalty=0,
    logit_bias=logit_bias,
        messages=[
            {
                "role": "system",
                "content": "日本語で700文字程度で要約してください。"
            },
            {
                "role": "user",
                "content": response["text"]
            },
        ],
        
    )
    print("要約")
    print(res)
    st.write("要約")
    st.write(res["choices"][0]["message"]["content"])
    print(res["choices"][0]["message"]["content"])
else:
    st.warning("ファイルが存在しません")