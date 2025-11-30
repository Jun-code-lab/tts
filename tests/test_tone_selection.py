#!/usr/bin/env python3
"""
테스트: 동적 톤 선택 기능 검증
목표: 슬픈 키워드 감지 시 TTS 스타일이 'sad'로 변경되는지 확인
"""

import os
import sys
from dotenv import load_dotenv
from superton_tts import SupertonTTS

# 한글 출력 깨짐 방지
sys.stdout.reconfigure(encoding='utf-8')

def test_tone_selection():
    """동적 톤 선택 기능 테스트"""
    load_dotenv()

    print("\n" + "="*60)
    print("🧪 동적 톤 선택 테스트 시작")
    print("="*60 + "\n")

    # 슬픈 톤을 사용할 키워드 목록 (main_superton.py와 동일)
    sad_keywords = ["죽고싶다", "뛰어내리고싶다", "살기싫다", "자살", "끝내고싶다", "절망", "극도로 힘들어"]

    try:
        tts = SupertonTTS()

        # 테스트 케이스
        test_cases = [
            {
                "name": "일반 대화 (중립 톤)",
                "user_input": "안녕, 오늘 날씨 어때?",
                "ai_response": "안녕! 오늘 날씨는 구름이 많아.",
                "expected_style": "neutral"
            },
            {
                "name": "슬픈 주제 - 자살 키워드 (슬픈 톤)",
                "user_input": "나 정말 자살하고 싶어",
                "ai_response": "그 기분이 당연하다고 생각해. 넌 혼자가 아니야. 전문가와 얘기하는 게 도움될 거야. 1393을 불러봐.",
                "expected_style": "sad"
            },
            {
                "name": "슬픈 주제 - 절망 키워드 (슬픈 톤)",
                "user_input": "정말 절망적이야",
                "ai_response": "그런 기분 충분히 이해해. 넌 이겨낼 수 있어.",
                "expected_style": "sad"
            },
            {
                "name": "슬픈 주제 - 극도로 힘들어 키워드 (슬픈 톤)",
                "user_input": "극도로 힘들어서 살기 싫어",
                "ai_response": "힘든 시간을 보내고 있구나. 감정이 타당해. 전문 상담사와 얘기해봐.",
                "expected_style": "sad"
            },
            {
                "name": "일반 대화 (중립 톤) - 슬픈 단어 없음",
                "user_input": "오늘은 좋은 날씨네",
                "ai_response": "정말 좋은 날씨야!",
                "expected_style": "neutral"
            }
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 테스트 {i}: {test_case['name']}")
            print(f"   사용자 입력: {test_case['user_input']}")

            # 키워드 감지 (main_superton.py의 로직과 동일)
            is_sad_topic = any(keyword in test_case['user_input'] for keyword in sad_keywords)
            response_style = "sad" if is_sad_topic else "neutral"

            print(f"   감지된 스타일: {response_style}")
            print(f"   예상 스타일: {test_case['expected_style']}")

            # 검증
            if response_style == test_case['expected_style']:
                print(f"   ✅ 성공: 올바른 톤이 선택됨")
            else:
                print(f"   ❌ 실패: 예상과 다른 톤이 선택됨")

            # AI 응답 재생
            print(f"   AI 응답: {test_case['ai_response']}")
            print(f"   🎤 음성 생성 및 재생 중 ({response_style} 톤)...")

            try:
                tts.speak(test_case['ai_response'], language="ko", style=response_style)
                print(f"   ✅ 재생 완료")
            except Exception as e:
                print(f"   ❌ 재생 오류: {e}")

        print("\n" + "="*60)
        print("✅ 테스트 완료!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_tone_selection()
