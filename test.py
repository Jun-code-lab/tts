import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

def test_speaker():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    # 1. 기본 설정
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "ko-KR-SeoHyeonNeural" # 서현이 목소리

    # 2. 스피커 출력 설정
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    print("🔊 스피커 테스트 중... (소리가 들려야 합니다)")
    
    # 3. SSML 없이 단순 텍스트로 테스트
    result = synthesizer.speak_text_async("아아, 마이크 테스트. 제 목소리 들리시나요?").get()

    # 4. 결과 확인
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ 재생 성공 (프로그램상으로는 소리를 보냈습니다)")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print(f"❌ 오류 발생: {result.cancellation_details.error_details}")

if __name__ == "__main__":
    test_speaker()