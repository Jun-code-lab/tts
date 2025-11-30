import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SUPERTON_API_KEY")
voice_id = os.getenv("SUPERTON_VOICE_ID")

print(f"API Key: {api_key[:30]}...")
print(f"Voice ID: {voice_id}\n")


# 2. 텍스트-음성 변환 (현재 voice_id 사용)
print("=" * 60)
print(f"[2] 텍스트-음성 변환 (Voice ID: {voice_id})")
print("=" * 60)

url = f"https://supertoneapi.com/v1/text-to-speech/{voice_id}"

payload = {
    "text": "안녕하세요, 수퍼톤 API입니다.",
    "language": "ko",
    "style": "neutral",
    "model": "sona_speech_1"
}

headers = {
    "x-sup-api-key": api_key,
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"상태: {response.status_code}")

    if response.status_code == 200:
        print("✅ 성공!")
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print(f"파일 저장됨: output.mp3 ({len(response.content)} bytes)")
    else:
        print(f"❌ 오류: {response.text}")

except Exception as e:
    print(f"❌ 요청 오류: {e}")
