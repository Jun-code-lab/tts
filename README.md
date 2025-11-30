# Chipi TTS (Text-to-Speech) 애플리케이션

음성 합성과 음성 인식을 통한 대화형 AI 시스템

## 🎙️ TTS 엔진 지원

### 1. Azure TTS (`tts_engine.py`, `main.py`)
- **공급자**: Microsoft Azure Cognitive Services
- **특징**: 음성 인식 + 음성 합성 통합
- **홈페이지**: https://azure.microsoft.com/ko-kr/services/cognitive-services/speech-services/
- **모델**: Ko-KR-SeoHyeonNeural (여성 음성)

### 2. SuperTone TTS (`superton_tts.py`, `main_superton.py`)
- **공급자**: SuperTone AI
- **홈페이지**: https://www.supertone.ai/
- **API 문서**: https://supertoneapi.com/
- **모델**: sona_speech_1

## 🚀 설치 및 실행

### 필수 라이브러리
```bash
pip install azure-cognitiveservices-speech python-dotenv requests pygame
```

### 환경 설정 (.env)
```
# Azure Speech
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=eastus

# SuperTone TTS
SUPERTON_API_KEY=your_key
SUPERTON_VOICE_ID=your_voice_id
```

### 실행
```bash
# Azure TTS 사용
python main.py

# SuperTone TTS 사용
python main_superton.py
```

## 📚 Credits & Attribution

- **Azure Speech Services**: Microsoft Azure Cognitive Services
- **SuperTone TTS**: SuperTone AI - https://www.supertone.ai/

## 📜 License

### Project License
This project is provided as-is for educational and personal use.

### Third-Party Licenses

#### Azure Speech Services
- **Provider**: Microsoft Corporation
- **License**: Microsoft Software License Terms
- **URL**: https://azure.microsoft.com/en-us/support/legal/
- **Note**: Requires valid Azure subscription for API usage

#### SuperTone TTS
- **Provider**: SuperTone AI
- **License**: SuperTone API Terms of Service
- **URL**: https://www.supertone.ai/
- **Note**: Requires valid API key and may have usage restrictions

### Dependencies Licenses
- **pygame**: LGPL License
- **requests**: Apache 2.0 License
- **python-dotenv**: BSD License
- **azure-cognitiveservices-speech**: Microsoft Software License Terms

**Important**: When using this project, ensure you comply with the terms and conditions of:
1. Azure Speech Services (if using Azure TTS)
2. SuperTone API (if using SuperTone TTS)
3. All third-party libraries and their respective licenses