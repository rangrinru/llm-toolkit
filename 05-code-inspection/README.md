# 05. Code Inspection

코드를 **수정하기 전에** 상태를 파악하고 문제를 찾는 프롬프트. (수정은 06-code-fix, PR 단위 리뷰는 07-code-review)

## 폴더 구조
```
05-code-inspection/
├── understanding/     # 처음 보는 코드베이스 파악
├── security/          # 보안 취약점 점검
├── performance/       # 성능 병목 점검
├── quality/           # 코드 품질, 기술 부채
└── checklists/        # 배포 전 체크리스트 등
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`understanding/codebase-overview.md`](./understanding/codebase-overview.md) | 코드베이스 구조 파악 |
| [`security/security-audit.md`](./security/security-audit.md) | 보안 점검 |
| [`performance/performance-check.md`](./performance/performance-check.md) | 성능 점검 |
| [`quality/tech-debt.md`](./quality/tech-debt.md) | 코드 품질 / 기술 부채 점검 |
| [`checklists/pre-release.md`](./checklists/pre-release.md) | 배포 전 체크리스트 |

## 작성 규칙
- 점검 단계에서는 "수정하지 말고 보고만" 하라고 명시
- 결과는 심각도(Critical/High/Medium/Low) 기준으로 정렬

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
