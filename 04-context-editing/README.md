# 04. Context Editing

이미 있는 글의 **문맥, 표현, 톤, 길이**를 다듬는 프롬프트. (새로 쓰는 것은 03-documents)

## 폴더 구조
```
04-context-editing/
├── proofreading/      # 맞춤법, 문법, 어색한 문장 교정
├── tone/              # 톤 변경 (격식, 친근, 전문적)
├── restructure/       # 문맥/논리 흐름 재구성, 압축/확장
└── translation/       # 번역, 현지화
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`proofreading/proofread.md`](./proofreading/proofread.md) | 교정 / 윤문 |
| [`tone/tone-rewrite.md`](./tone/tone-rewrite.md) | 톤 변경 |
| [`restructure/logic-flow.md`](./restructure/logic-flow.md) | 논리 흐름 재구성 |
| [`restructure/condense-expand.md`](./restructure/condense-expand.md) | 압축 / 확장 |
| [`translation/translate.md`](./translation/translate.md) | 자연스러운 번역 / 현지화 |

## 작성 규칙
- 원문의 의미를 바꾸지 않는다는 조건을 항상 명시
- 변경 사항을 diff 또는 표로 보여달라고 하면 검토가 쉬움

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
