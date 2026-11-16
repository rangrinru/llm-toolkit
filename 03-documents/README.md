# 03. Documents

보고서, 기획서, 요약, 회의록, 이메일, 오피스 파일(DOCX/PPTX/XLSX/HWP) 등 **문서 작성/가공** 프롬프트.

## 폴더 구조
```
03-documents/
├── writing/           # 보고서, 기획서, 제안서 작성
├── summarization/     # 요약, 회의록, 핵심 정리
├── business/          # 이메일, 공지, 업무 메시지
└── office/            # DOCX, PPTX, XLSX, HWP 변환/가공
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`writing/report.md`](./writing/report.md) | 보고서 / 기획서 작성 |
| [`summarization/summarize.md`](./summarization/summarize.md) | 긴 문서 요약 |
| [`summarization/meeting-notes.md`](./summarization/meeting-notes.md) | 회의록 정리 |
| [`business/email.md`](./business/email.md) | 업무 이메일 작성 |
| [`office/office-files.md`](./office/office-files.md) | 오피스 파일 생성/변환 |

## 작성 규칙
- 문서 유형별로 원하는 "출력 형식"(목차, 표, 분량)을 프롬프트에 명시
- 민감한 회사 정보는 올리기 전 마스킹

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
