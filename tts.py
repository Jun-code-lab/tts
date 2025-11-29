import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class AzureTTS:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not self.speech_key or not self.service_region:
            raise ValueError("❌ .env 파일 확인 필요!")

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
        )

    def generate_audio(self, text, params, output_filename):
        """
        하이퍼파라미터(params)를 받아 오디오를 생성하는 함수
        """
        # 1. 파라미터 언패킹 (기본값 설정)
        voice = params.get("voice", "ko-KR-SunHiNeural")
        style = params.get("style", "cheerful")
        degree = params.get("style_degree", 1.0)
        pitch = params.get("pitch", 0)   # 숫자만 입력 (예: 20 -> "+20%")
        rate = params.get("rate", 0)     # 숫자만 입력 (예: 10 -> "+10%")
        
        # 2. 동적 SSML 생성 (여기가 핵심!)
        # f-string을 써서 변수를 쏙쏙 집어넣습니다.
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
               xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ko-KR">
          <voice name="{voice}">
            <mstts:express-as style="{style}" styledegree="{degree}">
              <prosody pitch="{pitch:+d}%" rate="{rate:+d}%">
                {text}
              </prosody>
            </mstts:express-as>
          </voice>
        </speak>
        """

        # 3. 저장 설정 및 실행
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)

        print(f"🎛️ 생성 중... [설정: {style}({degree}), P:{pitch}%, R:{rate}%]")
        result = synthesizer.speak_ssml_async(ssml).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✅ 저장 완료: {output_filename}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            print(f"❌ 실패: {result.cancellation_details.error_details}")

# ==========================================================
# 🧪 하이퍼파라미터 실험실 (여기서 값만 바꾸세요!)
# ==========================================================
if __name__ == "__main__":
    tts = AzureTTS()

    # 1️⃣ Chipi (애기/식물 캐릭터) 설정값
    chipi_params = {
        "voice": "ko-KR-SeoHyeonNeural",  #
        "style": "cheerful",           # 감정: 쾌활함
        "style_degree": 1.0,           # 감정 강도: 0.01(최소)-2.0(최대)
        "pitch": 20,                   # 피치: -50% ~ +50%
        "rate": 20                     # 속도: -50~200
    }


    # === 테스트 실행 ===
    
    # Chipi 목소리 생성
    tts.generate_audio(
        text="안녕 고양이바질꾼! 난 치피야, 네가 키우는 작은 식물 친구야. 오늘 기분 어때?",
        params=chipi_params,
        output_filename="voice_chipi.mp3"
    )