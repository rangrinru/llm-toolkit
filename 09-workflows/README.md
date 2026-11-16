# 09. Workflows

LLM/에이전트와 일하는 **작업 과정(프로세스)** 정리. 여러 카테고리의 프롬프트를 어떤 순서로 쓰는지 기록.

## 폴더 구조
```
09-workflows/
├── development/       # 기능 개발, 버그 수정 흐름
├── content/           # 디자인/영상/문서 제작 흐름
├── research/          # 조사, 비교 분석 흐름
└── logs/              # 실제 작업 회고 (날짜별)
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`development/plan-implement-verify.md`](./development/plan-implement-verify.md) | 계획 → 구현 → 검증 기본 루프 |
| [`development/feature-development.md`](./development/feature-development.md) | 기능 개발 전체 흐름 |
| [`development/bug-triage.md`](./development/bug-triage.md) | 버그 처리 흐름 |
| [`content/design-to-motion.md`](./content/design-to-motion.md) | 디자인 → 모션 제작 흐름 |
| [`research/research.md`](./research/research.md) | 리서치 흐름 |
| [`logs/README.md`](./logs/README.md) | 작업 회고 작성법 |

## 작성 규칙
- 단계마다 어떤 카테고리의 프롬프트를 쓰는지 링크로 연결
- 실패했던 방식도 기록 (다음에 피하기 위해)

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
