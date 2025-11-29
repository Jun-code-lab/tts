import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import pygame

load_dotenv()

class AzureTTS:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not self.speech_key or not self.service_region:
            raise ValueError("❌ .env 파일 확인 필요")

        pygame.mixer.init()

        # Speech Config는 한 번만 로드해서 재사용 (속도 향상)
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
        )
        self.speech_config.speech_recognition_language = "ko-KR"

    def speak(self, text, params):
        print(f"🔊 [TTS] 음성 생성 시작: {text[:15]}...", end=" ", flush=True)
        
        voice = params.get("voice", "ko-KR-SeoHyeonNeural")
        style = params.get("style", "cheerful")
        degree = params.get("style_degree", 2.0)
        pitch = params.get("pitch", 0)
        rate = params.get("rate", 0)

        ssml_string = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ko-KR">'
            f'<voice name="{voice}">'
            f'<mstts:express-as style="{style}" styledegree="{degree}">'
            f'<prosody pitch="{pitch:+d}%" rate="{rate:+d}%">'
            f'{text}'
            f'</prosody></mstts:express-as></voice></speak>'
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_filename = os.path.join(current_dir, "temp_output.mp3")

        # 파일 저장용 합성기 생성
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        
        # 비동기 실행 (생성)
        result = synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ 생성 완료 -> 재생 중", flush=True)
            
            # 파일 쓰기
            with open(temp_filename, "wb") as f:
                f.write(result.audio_data)
            
            # 재생
            try:
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(30) # 체크 주기를 10->30으로 높여 반응성 향상
                pygame.mixer.music.unload()
            except Exception as e:
                print(f"\n❌ 재생 오류: {e}")

            # 파일 삭제 (빠른 정리를 위해 try-except 최소화)
            try: os.remove(temp_filename)
            except: pass

        elif result.reason == speechsdk.ResultReason.Canceled:
            print(f"\n❌ [TTS 실패] {result.cancellation_details.error_details}")

        del synthesizer

    def listen(self):
        # 듣기 전용 설정
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # [중요] 침묵 감지 시간 단축 (말 끝나면 더 빨리 인식하도록)
        # 기본값보다 짧게 설정하여 반응 속도를 높임
        # InitialSilenceTimeout: 말 시작 전 대기 시간
        # EndSilenceTimeout: 말 끝난 후 대기 시간 (이걸 줄여야 빨리 넘어감)
        recognizer.properties.set_property_by_name("SpeechServiceConnection_InitialSilenceTimeoutMs", "3000")
        recognizer.properties.set_property_by_name("Speech_SegmentationSilenceTimeoutMs", "1000")

        print("\n👂 듣는 중...", end=" ", flush=True)
        
        result = recognizer.recognize_once_async().get()

        # 리소스 즉시 해제 (충돌 방지)
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