import os
import sys
from dotenv import load_dotenv
from chipi_brain import ChipiBrain
from superton_tts import SupertonTTS


# 한글 출력 깨짐 방지
sys.stdout.reconfigure(encoding='utf-8')

def main():
    load_dotenv()

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

        while True:
            # 1. 마이크로 입력 받기
            user_text = tts.listen()

            if not user_text:
                continue

            # 종료 체크
            if any(word in user_text for word in ["종료", "그만", "꺼져"]):
                tts.speak("안녕!", language="ko", style="neutral")
                break

            # 2. 생각하기
            print("🧠 생각하는 중...", end=" ", flush=True)
            brain.add_msg(user_text)
            ai_response = brain.wait_run(ai_name='chipi', device_serial=device_serial)
            print("✅ 완료", flush=True)

            if not ai_response:
                tts.speak("미안, 다시 말해줄래?", language="ko", style="neutral")
                continue

            # 3. 답변 출력 및 음성 재생
            print(f"🤖 치피: {ai_response}")
            tts.speak(ai_response, language="ko", style="neutral")

    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        input("종료하려면 엔터...")

if __name__ == "__main__":
    main()
