import streamlit as st
import time
import azure.cognitiveservices.speech as speechsdk
import openai
from dotenv import load_dotenv
import os


# dotenvを使って.envファイルを読み込む
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")
openai.api_key = os.getenv("OPENAI_API_KEY")

#ファイルの読み込み
file = st.file_uploader("m4aファイルをアップロードしてください")

# ファイルがアップロードされた場合にのみ処理を実行する
if file is not None:
    # ファイル名を取得する
    filename = file.name
    
    # ファイルの内容を読み込む
    file_content = file.read()
    
    # 読み込んだ内容をそのまま別のファイルに書き出す
    with open("output.wav", "wb") as f:
        f.write(file_content)

def recognize_audio(output, speech_key, service_region, filename, recognize_time=100):
    """
    wav形式のデータから文字を起こす関数
    ---------------------------
    Parameters
    output: str
        音声から起こしたテキスト（再帰的に取得する）
    speech_key: str
        Azure Speech SDKのキー
    service_region: str
         Azure Speech SDKのリージョン名
    filename: str
        音声ファイルのパス
    recognize_time: int
        音声認識にかける時間（秒）
    """
    # Speech to Text 設定周り
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="ja-JP")

    # 認識器の設定
    audio_input = speechsdk.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    def recognized(evt):
        nonlocal output
        output += evt.result.text
        
    # 音声認識の実行
    # recognize_timeの時間、継続して文字起こしを行う
    # ユーザーが認識結果を受け取るにはEventSignalに接続する必要がある
    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.start_continuous_recognition()
    time.sleep(recognize_time)

    return output


filename = "output.m4a"
output = ""

output = recognize_audio(output, speech_key, service_region, filename, recognize_time=200)

def summarize(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"次の文章を700字で要約してください:\n\n{text}",
        max_tokens=700,
        temperature=0
    )
    return response["choices"][0]["text"]

if output:
    summarize_text = summarize(output)
print("recognize")
print(output)
print("openai")
print(summarize_text)

st.write(summarize_text)