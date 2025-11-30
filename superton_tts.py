import os
import requests
import pygame
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()


class SupertonTTS:
    """SuperTone API를 사용한 TTS 클래스"""

    def __init__(self, voice_id=None, api_key=None):
        """
        초기화

        Args:
            voice_id: 음성 ID (기본값: env의 SUPERTON_VOICE_ID)
            api_key: API 키 (기본값: env의 SUPERTON_API_KEY)
        """
        self.api_key = api_key or os.getenv("SUPERTON_API_KEY")
        self.voice_id = voice_id or os.getenv("SUPERTON_VOICE_ID")

        if not self.api_key:
            raise ValueError("❌ SUPERTON_API_KEY가 설정되지 않았습니다.")

        pygame.mixer.init()

        # Azure Speech 설정 (음성 인식용)
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SPEECH_REGION")

        if self.speech_key and self.service_region:
            self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
            self.speech_config.speech_recognition_language = "ko-KR"
        else:
            self.speech_config = None

    def generate(self, text, language="ko", style="neutral", output_format="wav",
                 pitch_shift=0, speed=1, pitch_variance=1):
        """
        SuperTone API를 사용하여 음성 생성

        Args:
            text: 텍스트
            language: 언어 (기본값: "ko")
            style: 스타일 (기본값: "neutral")
            output_format: 출력 형식 - "wav" 또는 "mp3" (기본값: "wav")
            pitch_shift: 음높이 조정 (-20 ~ 20, 기본값: 0)
            speed: 재생 속도 (0.5 ~ 2, 기본값: 1)
            pitch_variance: 음높이 변동성 (0 ~ 2, 기본값: 1)

        Returns:
            음성 바이트 데이터 또는 None
        """
        url = f"https://supertoneapi.com/v1/text-to-speech/{self.voice_id}"

        headers = {
            "x-sup-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "language": language,
            "style": style,
            "model": "sona_speech_1",
            "output_format": output_format,
            "voice_settings": {
                "pitch_shift": pitch_shift,
                "pitch_variance": pitch_variance,
                "speed": speed
            }
        }

        try:
            print(f"🔊 음성 생성 중: {text[:20]}...", end=" ", flush=True)

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                print("✅ 완료", flush=True)
                return response.content
            else:
                print(f"❌ 오류 (상태: {response.status_code})", flush=True)
                print(f"응답: {response.text}")
                return None

        except requests.exceptions.Timeout:
            print(f"❌ 요청 시간 초과 (30초)", flush=True)
            return None
        except Exception as e:
            print(f"❌ 오류: {e}", flush=True)
            return None

    def speak(self, text, language="ko", style="neutral", pitch_shift=0, speed=1, pitch_variance=1):
        """
        텍스트를 음성으로 변환하고 재생

        Args:
            text: 말할 텍스트
            language: 언어 (기본값: "ko")
            style: 스타일 (기본값: "neutral")
            pitch_shift: 음높이 조정 (-20 ~ 20, 기본값: 0)
            speed: 재생 속도 (0.5 ~ 2, 기본값: 1)
            pitch_variance: 음높이 변동성 (0 ~ 2, 기본값: 1)
        """
        audio_data = self.generate(text, language, style, output_format="wav",
                                   pitch_shift=pitch_shift, speed=speed,
                                   pitch_variance=pitch_variance)

        if audio_data:
            try:
                # 임시 파일로 저장 후 재생
                current_dir = os.path.dirname(os.path.abspath(__file__))
                temp_file = os.path.join(current_dir, "temp_superton.wav")

                with open(temp_file, "wb") as f:
                    f.write(audio_data)

                print("▶️  재생 중...", end=" ", flush=True)
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(30)

                pygame.mixer.music.unload()
                print("✅ 완료", flush=True)

                # 임시 파일 삭제
                try:
                    os.remove(temp_file)
                except:
                    pass

            except Exception as e:
                print(f"❌ 재생 오류: {e}", flush=True)

    def save(self, text, filename="output.wav", language="ko", style="neutral", output_format="wav",
             pitch_shift=0, speed=1, pitch_variance=1):
        """
        텍스트를 음성 파일로 저장

        Args:
            text: 말할 텍스트
            filename: 저장할 파일명 (기본값: "output.wav")
            language: 언어 (기본값: "ko")
            style: 스타일 (기본값: "neutral")
            output_format: 출력 형식 - "wav" 또는 "mp3" (기본값: "wav")
            pitch_shift: 음높이 조정 (-20 ~ 20, 기본값: 0)
            speed: 재생 속도 (0.5 ~ 2, 기본값: 1)
            pitch_variance: 음높이 변동성 (0 ~ 2, 기본값: 1)

        Returns:
            저장된 파일 경로 또는 None
        """
        audio_data = self.generate(text, language, style, output_format,
                                   pitch_shift=pitch_shift, speed=speed,
                                   pitch_variance=pitch_variance)

        if audio_data:
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(current_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(audio_data)

                print(f"💾 저장 완료: {filepath}")
                return filepath

            except Exception as e:
                print(f"❌ 파일 저장 오류: {e}", flush=True)
                return None

        return None

    def listen(self):
        """
        마이크에서 음성 입력받아 텍스트로 변환

        Returns:
            인식된 텍스트 또는 None
        """
        if not self.speech_config:
            print("❌ Azure Speech 설정이 없습니다.")
            return None

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # 침묵 감지 시간 단축
        recognizer.properties.set_property_by_name("SpeechServiceConnection_InitialSilenceTimeoutMs", "3000")
        recognizer.properties.set_property_by_name("Speech_SegmentationSilenceTimeoutMs", "1000")

        print("\n👂 듣는 중...", end=" ", flush=True)

        result = recognizer.recognize_once_async().get()

        # 리소스 즉시 해제
        del recognizer
        del audio_config

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"✅ 인식됨: \"{result.text}\"", flush=True)
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("🔕 (침묵)", flush=True)
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("❌ (취소/오류)", flush=True)
            return None

    def list_voices(self):
        """
        사용 가능한 모든 음성 목록 조회

        Returns:
            음성 목록 또는 None
        """
        url = "https://supertoneapi.com/v1/voices"

        headers = {
            "x-sup-api-key": self.api_key
        }

        try:
            print("🎤 음성 목록 조회 중...", end=" ", flush=True)

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                print("✅ 완료", flush=True)
                return response.json()
            else:
                print(f"❌ 오류 (상태: {response.status_code})", flush=True)
                return None

        except Exception as e:
            print(f"❌ 오류: {e}", flush=True)
            return None


# 🧪 하이퍼파라미터 실험실 (여기서 값만 바꾸세요!)
# ==========================================================
if __name__ == "__main__":
    tts = SupertonTTS()

    # 1️⃣ Chipi (애기/식물 캐릭터) 설정값
    chipi_params = {
        "language": "ko",              # 언어: "ko"(한국어), "en"(영어) 등
        "style": "happy",            # 감정: "neutral", "happy", "sad", "angry" 등
        "pitch_shift": 10,              # 음높이: -20 ~ 20 (음수=낮음, 양수=높음)
        "speed": 1,                    # 속도: 0.5 ~ 2 (0.5=느림, 2=빠름)
        "pitch_variance": 1            # 음높이 변동성: 0 ~ 2 (0=일정함, 2=변동 큼)
    }

    print("=== SuperTone TTS 테스트 ===\n")
    print(f"📋 현재 설정:")
    for key, value in chipi_params.items():
        print(f"   {key}: {value}")
    print()

    try:
        # 1. 음성 재생 (기본값)
        print("[1] 음성 재생 (chipi_params 적용):")
        tts.speak("안녕하세요, 슈퍼톤입니다!", **chipi_params)

        # 2. 음성 저장
        print("\n[2] WAV 파일 생성:")
        filepath = tts.save("반갑습니다!", filename="test_superton.wav", **chipi_params)

        if filepath:
            print(f"✅ 파일 저장됨: {filepath}\n")

        print("\n✅ 테스트 완료!")

    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()
