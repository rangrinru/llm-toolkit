# 디자인 토큰 정의

> 대상 모델: Claude, GPT | 마지막 테스트: YYYY-MM-DD

## 언제 쓰나
- 새 프로젝트의 디자인 기준을 잡을 때
- 여러 화면의 스타일을 통일해야 할 때

## 프롬프트
```text
{브랜드/서비스 설명}과 {톤앤매너}에 맞는 디자인 토큰을 정의해줘.

포함 항목:
- Color: primary/secondary/neutral 스케일(50~900), semantic(success, warning, error, info), light/dark 모드
- Typography: 폰트 패밀리, 크기 스케일, line-height, weight
- Spacing: 4px 기반 스케일
- Radius, Shadow, Border, Motion(duration/easing)

출력: 1) 표로 정리 2) CSS 변수 3) Tailwind config 형식
```

## 메모
- 
