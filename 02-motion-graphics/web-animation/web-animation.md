# 웹 인터랙션 애니메이션

> 대상 모델: Claude, Codex | 마지막 테스트: YYYY-MM-DD

## 언제 쓰나
- 웹페이지에 스크롤, 호버, 진입 애니메이션을 넣을 때

## 프롬프트
```text
{라이브러리: CSS / GSAP / Framer Motion} 로 아래 애니메이션을 구현해줘.

[대상] {요소}
[트리거] {페이지 진입 / 스크롤 / 호버 / 클릭}
[느낌] {부드럽게, 탄력 있게, 빠르고 단단하게}

- duration, easing 값을 명시하고 이유를 짧게 설명
- prefers-reduced-motion 대응 포함
- 성능을 위해 transform, opacity 위주로
```

## 메모
- 
