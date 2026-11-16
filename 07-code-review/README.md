# 07. Code Review

PR / 커밋 / 변경사항 단위로 **리뷰**하는 프롬프트와 체크리스트.

## 폴더 구조
```
07-code-review/
├── pr-review/         # PR 리뷰 프롬프트
├── self-review/       # 올리기 전 셀프 리뷰
└── checklists/        # 리뷰 체크리스트
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`pr-review/pr-review.md`](./pr-review/pr-review.md) | PR 리뷰 |
| [`pr-review/review-comment.md`](./pr-review/review-comment.md) | 리뷰 코멘트 작성 |
| [`self-review/self-review.md`](./self-review/self-review.md) | PR 올리기 전 셀프 리뷰 |
| [`checklists/review-checklist.md`](./checklists/review-checklist.md) | 리뷰 체크리스트 |

## 작성 규칙
- 리뷰 결과는 Blocker / Should fix / Nit 3단계로 구분
- 칭찬할 점도 1~2개 포함하면 실제 리뷰 코멘트로 쓰기 좋음

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
