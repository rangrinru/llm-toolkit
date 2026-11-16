# 06. Code Fix

버그 수정, 디버깅, 리팩토링, 마이그레이션 등 **코드를 실제로 고치는** 프롬프트.

## 폴더 구조
```
06-code-fix/
├── debugging/         # 원인 분석 + 수정
├── refactoring/       # 동작 유지 리팩토링
├── migration/         # 버전 업그레이드, 라이브러리 교체
└── testing/           # 테스트 작성 / 실패 테스트 수정
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`debugging/debug.md`](./debugging/debug.md) | 가설 기반 디버깅 |
| [`debugging/minimal-patch.md`](./debugging/minimal-patch.md) | 최소 범위 버그 수정 |
| [`refactoring/refactor.md`](./refactoring/refactor.md) | 동작 유지 리팩토링 |
| [`migration/migration.md`](./migration/migration.md) | 버전 업그레이드 / 마이그레이션 |
| [`testing/write-tests.md`](./testing/write-tests.md) | 테스트 작성 |

## 작성 규칙
- "원인 분석 → 계획 → 수정 → 검증" 순서를 강제
- 수정 범위를 제한 (관련 없는 파일 수정 금지)

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
