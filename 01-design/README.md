# 01. Design

UI/UX, 웹/앱 화면, 디자인 시스템, 슬라이드, 이미지 생성 등 **정적인 시각 결과물**을 만드는 프롬프트.

## 폴더 구조
```
01-design/
├── ui-web/            # 웹/앱 화면, 랜딩페이지, 컴포넌트
├── design-system/     # 디자인 토큰, 컴포넌트 규칙, 스타일 가이드
├── slides/            # 발표자료, 피치덱
├── image-gen/         # Midjourney, GPT Image, Imagen 등 이미지 생성
└── references/        # 레퍼런스 사이트, 스타일 키워드 모음
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`ui-web/landing-page.md`](./ui-web/landing-page.md) | 랜딩페이지 / 웹 UI 생성 |
| [`ui-web/ui-polish.md`](./ui-web/ui-polish.md) | 기존 UI 개선(폴리싱) |
| [`design-system/design-tokens.md`](./design-system/design-tokens.md) | 디자인 토큰 정의 |
| [`slides/presentation.md`](./slides/presentation.md) | 발표자료 구성 + 디자인 |
| [`image-gen/image-prompt.md`](./image-gen/image-prompt.md) | 이미지 생성 프롬프트 공식 |
| [`references/style-keywords.md`](./references/style-keywords.md) | 스타일 키워드 / 레퍼런스 |

## 작성 규칙
- 결과물 스크린샷은 같은 폴더의 `assets/`에 저장
- "피해야 할 스타일"을 프롬프트에 꼭 명시 (뻔한 AI 디자인 방지)

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
