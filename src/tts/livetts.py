import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import pygame

load_dotenv()

class AzureTTS:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not self.speech_key or not self.service_region:
            print("❌ 오류: .env 파일이 없거나 키가 설정되지 않았습니다.")
            raise ValueError(".env 파일 확인 필요")

        # Pygame 초기화 (오디오 재생용)
        pygame.mixer.init()

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        # 고음질 설정 (48kHz)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
        )

    def speak(self, text, params):
        # 1. 사용자 설정값 가져오기
        voice = params.get("voice", "ko-KR-SeoHyeonNeural")
        style = params.get("style", "cheerful")
        degree = params.get("style_degree", 1.0)
        pitch = params.get("pitch", 0)
        rate = params.get("rate", 0)

        # 2. SSML 포맷팅 (+ 부호 붙이기)
        fmt_pitch = f"+{pitch}%" if pitch >= 0 else f"{pitch}%"
        fmt_rate = f"+{rate}%" if rate >= 0 else f"{rate}%"

        # 3. SSML 생성 (사용자 설정 적용)
        ssml_string = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ko-KR">'
            f'<voice name="{voice}">'
            f'<mstts:express-as style="{style}" styledegree="{degree}">'
            f'<prosody pitch="{fmt_pitch}" rate="{fmt_rate}">'
            f'{text}'
            f'</prosody></mstts:express-as></voice></speak>'
        )

        # 절대 경로로 파일명 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_filename = os.path.join(current_dir, "temp_output.mp3")

        # 4. Azure 합성기 생성 (스피커 사용 X -> 데이터만 받음)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

        print(f"🔊 치피 생성 중... (Pitch:{fmt_pitch}, Rate:{fmt_rate})")
        
        # 5. 실행
        result = synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # 6. 받은 데이터를 직접 파일로 저장 (오류 원천 차단)
            audio_data = result.audio_data
            with open(temp_filename, "wb") as f:
                f.write(audio_data)
            
            # 7. Pygame으로 재생
            try:
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
            except Exception as e:
                print(f"❌ 재생 오류: {e}")

            # 파일 정리
            try:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
            except:
                pass

        elif result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            print(f"❌ [Azure 오류] {details.error_details}")

        del synthesizer

# =========================================================
# 2. 듣기 담당 (STT)
# =========================================================
def listen_to_user():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "ko-KR" 
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print("\n🎤 듣고 있어요... (말씀해 보세요)")
    result = recognizer.recognize_once_async().get()
    
    # 리소스 해제
    del recognizer
    del audio_config
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"📝 인식: {result.text}")
        return result.text
    return None

# =========================================================
# 3. LLM 로직 (가짜)
# =========================================================
def get_ai_response(user_text):
    if "안녕" in user_text: return "안녕 고양이바질꾼! 반가워! 오늘도 바질 보러 왔어?"
    elif "상태" in user_text: return "음... 바질 잎이 조금 시무룩해 보여. 물을 좀 주면 어때?"
    elif "종료" in user_text: return "exit"
    return f"네가 방금 '{user_text}'라고 말했지? 내가 똑같이 말해줄게!"

# =========================================================
# 4. 실행
# =========================================================
if __name__ == "__main__":
    try:
        tts = AzureTTS()
        
        # ✨ [사용자님 설정값 적용 완료]
        chipi_params = {
            "voice": "ko-KR-SeoHyeonNeural",  # 서현이
            "style": "cheerful",              # 쾌활함
            "style_degree": 1.0,              # 강도 1.0
            "pitch": 20,                      # 피치 +20% (높음)
            "rate": 20                        # 속도 +20% (빠름)
        }
        
        print("============== 치피 음성 비서 시작 ==============")
        tts.speak("치피가 깨어났어! 나랑 대화하자!", chipi_params)

        while True:
            text = listen_to_user()
            if not text: continue
            
            response = get_ai_response(text)
            if response == "exit": 
                tts.speak("알겠어! 나중에 또 봐! 안녕!", chipi_params)
                break
            
            print(f"🤖 치피 생각: {response}")
            tts.speak(response, chipi_params)
            
    except Exception as e:
        print(f"Error: {e}")