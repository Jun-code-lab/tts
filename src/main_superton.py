import os
import sys

# 경로 설정 (src 폴더에서 실행되므로 상위 폴더 추가)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.core.chipi_brain import ChipiBrain
from src.tts.superton_tts import SupertonTTS


# 한글 출력 깨짐 방지
sys.stdout.reconfigure(encoding='utf-8')

def main():
    load_dotenv('config/.env')

    device_serial = os.environ.get("DEVICE_SERIAL")
    if not device_serial:
        print("⚠️ DEVICE_SERIAL 없음")

    print("\n============== ⚡ 치피(Chipi) SuperTone TTS 모드 시작 ==============\n")

    try:
        print("🧠 두뇌(LLM) 연결 중...", end=" ", flush=True)
        brain = ChipiBrain()
        print("✅ 완료")

        print("🎤 음성(SuperTone TTS) 연결 중...", end=" ", flush=True)
        tts = SupertonTTS()
        print("✅ 완료\n")

        # 시작 인사
        tts.speak("준비됐어! 말 걸어줘!", language="ko", style="neutral")

        # 슬픈 톤을 사용할 키워드 목록
        sad_keywords = ["죽고", "자살", "끝내고", "절망", "극도로 힘들", "살기싫", "뛰어내리"]

        while True:
            # 1. 마이크로 입력 받기
            user_text = tts.listen()

            if not user_text:
                continue

            # 종료 체크
            if any(word in user_text for word in ["종료", "그만", "꺼져"]):
                tts.speak("안녕!", language="ko", style="neutral")
                break

            # 슬픈 톤 키워드 감지 (공백/문장부호 무관)
            is_sad_topic = any(keyword in user_text for keyword in sad_keywords)
            print(f"🔍 슬픈 토픽 감지: {is_sad_topic}", flush=True)

            # 2. 생각하기
            print("🧠 생각하는 중...", end=" ", flush=True)
            brain.add_msg(user_text)
            ai_response = brain.wait_run(ai_name='chipi', device_serial=device_serial)
            print("✅ 완료", flush=True)

            if not ai_response:
                response_style = "sad" if is_sad_topic else "neutral"
                pitch_shift = -10 if is_sad_topic else 0
                tts.speak("미안, 다시 말해줄래?", language="ko", style=response_style, pitch_shift=pitch_shift)
                continue

            # 3. 답변 출력 및 음성 재생
            print(f"🤖 치피: {ai_response}")

            # 슬픈 키워드가 있으면 슬픈 톤으로, 없으면 중립 톤으로 재생
            response_style = "sad" if is_sad_topic else "neutral"
            # 슬픈 톤일 때는 피치를 낮춤 (-20: 최저)
            pitch_shift = -10 if is_sad_topic else 0
            print(f"🎤 응답 톤: {response_style}, 피치: {pitch_shift}", flush=True)
            tts.speak(ai_response, language="ko", style=response_style, pitch_shift=pitch_shift)

    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        input("종료하려면 엔터...")

if __name__ == "__main__":
    main()
