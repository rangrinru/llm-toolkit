# 01. Design

UI/UX, 웹/앱 화면, 디자인 시스템, 슬라이드, 이미지 생성 등 **정적인 시각 결과물**을 만드는 프롬프트.

## 폴더 구조
```
01-design/
├── ui-web/            # 웹/앱 화면, 랜딩페이지, 컴포넌트
├── design-system/     # 디자인 토큰, 컴포넌트 규칙, 스타일 가이드
├── slides/            # 발표자료, 피치덱
├── image-gen/         # Midjourney, GPT Image, Imagen 등 이미지 생성
├── infographic/       # 단계 가이드, 프로세스 그림 등 한 장짜리 설명 그림
├── impeccable/        # Impeccable(디자인 명령어 스킬) 정리
├── taste-skill/       # Taste Skill(회사/랜딩 사이트 취향 스킬) 정리
├── hallmark/          # Hallmark(anti-AI-slop 디자인 스킬) 정리: 바닥 규칙, 체크리스트, 테마, 페이지 구조
└── references/        # 레퍼런스 사이트, 스타일 키워드, 프롬프트 품질 요소
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`ui-web/landing-page.md`](./ui-web/landing-page.md) | 랜딩페이지 / 웹 UI 생성 |
| [`ui-web/ui-polish.md`](./ui-web/ui-polish.md) | 기존 UI 개선(폴리싱) |
| [`design-system/design-tokens.md`](./design-system/design-tokens.md) | 디자인 토큰 정의 |
| [`slides/presentation.md`](./slides/presentation.md) | 발표자료 구성 + 디자인 |
| [`image-gen/image-prompt.md`](./image-gen/image-prompt.md) | 이미지 생성 프롬프트 공식 |
| [`infographic/step-guide.md`](./infographic/step-guide.md) | 단계 가이드(프로세스 인포그래픽) + 스타일 프리셋 10종 |
| [`hallmark/README.md`](./hallmark/README.md) | **Hallmark 정리**: AI 티 안 나는 웹 디자인 스킬 개요, 설치, 사용법 |
| [`hallmark/floor-rules.md`](./hallmark/floor-rules.md) | 절대 어기면 안 되는 16개 바닥 규칙 (CLAUDE.md 붙여넣기용 포함) |
| [`hallmark/ai-slop-gates.md`](./hallmark/ai-slop-gates.md) | AI 티 체크리스트 (색, 타이포, 레이아웃, 카피, 모션, 접근성) |
| [`hallmark/build-flow.md`](./hallmark/build-flow.md) | 7단계 빌드 과정 + 사전 질문 템플릿 |
| [`hallmark/genres.md`](./hallmark/genres.md) | 4개 장르별 허용/금지 |
| [`hallmark/themes-catalog.md`](./hallmark/themes-catalog.md) | 50개 테마 카탈로그 |
| [`hallmark/macrostructures.md`](./hallmark/macrostructures.md) | 21개 페이지 구조 + 도메인별 추천 |
| [`hallmark/custom-direction.md`](./hallmark/custom-direction.md) | 테마 없이 커스텀 디자인하는 원칙 |
| [`hallmark/prompts.md`](./hallmark/prompts.md) | Hallmark 명령 + 설치 없이 쓰는 anti-slop 프롬프트 |
| [`impeccable/README.md`](./impeccable/README.md) | **Impeccable 정리**: bolder/polish/critique/audit 등 24개 디자인 명령, slop 감지기 |
| [`taste-skill/README.md`](./taste-skill/README.md) | **Taste Skill 정리**: 업종 분류, deal 방식, house rules, AI 카피 금지어 |
| [`references/design-skills-compared.md`](./references/design-skills-compared.md) | Hallmark / Impeccable / Taste Skill / frontend-design 비교 + 공통 금지 패턴 |
| [`references/style-keywords.md`](./references/style-keywords.md) | 스타일 키워드 / 레퍼런스 / 한글 폰트 / 색 조합 / 문장 톤 |
| [`references/prompt-elements.md`](./references/prompt-elements.md) | 디자인 프롬프트 품질을 올리는 요소 + 틀 |

## 작성 규칙
- 결과물 스크린샷은 같은 폴더의 `assets/`에 저장
- "피해야 할 스타일"을 프롬프트에 꼭 명시 (뻔한 AI 디자인 방지)
- 색은 이름 대신 hex와 쓰는 자리, 폰트는 실제 이름, 문장 톤은 예문 하나로 적는다 ([품질 요소](./references/prompt-elements.md))

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
