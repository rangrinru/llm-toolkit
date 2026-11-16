# LLM Toolkit

Claude, Codex, GPT, Gemini 등 LLM을 더 잘 쓰기 위한 **프롬프트, 스킬, 에이전트 지침, 작업 과정, 도구, 플러그인**을 카테고리별로 모아두는 개인 저장소.

## 구조

```
llm-toolkit/
│
├── 01-design/               # 디자인: UI/웹, 디자인 시스템, 슬라이드, 이미지 생성
├── 02-motion-graphics/      # 모션그래픽: Remotion, Manim, After Effects, 웹 애니메이션, AI 영상
├── 03-documents/            # 문서 작업: 보고서, 요약, 회의록, 이메일, 오피스 파일
├── 04-context-editing/      # 문맥 수정: 교정, 톤 변경, 논리 재구성, 압축/확장, 번역
├── 05-code-inspection/      # 코드 점검: 구조 파악, 보안, 성능, 품질, 배포 체크리스트
├── 06-code-fix/             # 코드 수정: 디버깅, 리팩토링, 마이그레이션, 테스트
├── 07-code-review/          # 코드 리뷰: PR 리뷰, 셀프 리뷰, 체크리스트
├── 08-agent-instructions/   # 에이전트 지침: CLAUDE.md, AGENTS.md, 서브에이전트, 커맨드, hooks, 시스템 프롬프트
├── 09-workflows/            # 작업 과정: 개발/콘텐츠/리서치 흐름, 작업 회고
│
├── skills/                  # Claude Skills(SKILL.md) 등 재사용 스킬 패키지
├── tools/                   # 유용한 AI 도구, CLI, 서비스 목록
├── plugins/                 # MCP 서버, Claude Code 플러그인, 확장
└── templates/               # 프롬프트 / 워크플로우 작성 템플릿
```

## 카테고리

| # | 카테고리 | 용도 | 대표 파일 |
|---|---|---|---|
| 01 | [Design](./01-design) | 정적인 시각 결과물 | [랜딩페이지](./01-design/ui-web/landing-page.md), [디자인 토큰](./01-design/design-system/design-tokens.md) |
| 02 | [Motion Graphics](./02-motion-graphics) | 코드 기반 모션 + AI 영상 | [Remotion](./02-motion-graphics/remotion/remotion-video.md), [AI 영상](./02-motion-graphics/ai-video/video-gen-prompt.md) |
| 03 | [Documents](./03-documents) | 문서를 새로 작성/가공 | [보고서](./03-documents/writing/report.md), [요약](./03-documents/summarization/summarize.md) |
| 04 | [Context Editing](./04-context-editing) | 이미 있는 글 다듬기 | [교정](./04-context-editing/proofreading/proofread.md), [톤 변경](./04-context-editing/tone/tone-rewrite.md) |
| 05 | [Code Inspection](./05-code-inspection) | 수정 전 점검/분석 | [구조 파악](./05-code-inspection/understanding/codebase-overview.md), [보안](./05-code-inspection/security/security-audit.md) |
| 06 | [Code Fix](./06-code-fix) | 실제 코드 수정 | [디버깅](./06-code-fix/debugging/debug.md), [리팩토링](./06-code-fix/refactoring/refactor.md) |
| 07 | [Code Review](./07-code-review) | 변경사항 리뷰 | [PR 리뷰](./07-code-review/pr-review/pr-review.md), [체크리스트](./07-code-review/checklists/review-checklist.md) |
| 08 | [Agent Instructions](./08-agent-instructions) | 에이전트 지속 지침 | [CLAUDE.md](./08-agent-instructions/claude-code/CLAUDE.md.template), [AGENTS.md](./08-agent-instructions/codex/AGENTS.md.template) |
| 09 | [Workflows](./09-workflows) | 작업 과정 / 프로세스 | [계획-구현-검증](./09-workflows/development/plan-implement-verify.md), [디자인→모션](./09-workflows/content/design-to-motion.md) |
| - | [Skills](./skills) | 스킬 패키지 | [템플릿](./skills/_template/SKILL.md) |
| - | [Tools](./tools) | 도구 목록 | |
| - | [Plugins & MCP](./plugins) | 기능 확장 | |
| - | [Templates](./templates) | 작성 양식 | [프롬프트](./templates/prompt-template.md), [워크플로우](./templates/workflow-template.md) |

## 어디에 넣을지 헷갈릴 때

- 새로 **쓰는** 글 → `03-documents` / 이미 있는 글을 **고치는** 것 → `04-context-editing`
- 코드를 **보기만** → `05-code-inspection` / **고치기** → `06-code-fix` / **변경사항 평가** → `07-code-review`
- 한 번 쓰는 요청 → 카테고리 폴더 / 에이전트가 **항상** 따라야 하는 규칙 → `08-agent-instructions`
- 여러 프롬프트를 **순서대로** 쓰는 흐름 → `09-workflows`
- 스크립트/참고자료까지 묶인 패키지 → `skills`

## 기록 규칙

1. 파일명은 `kebab-case.md`, 폴더는 `카테고리/세부분류/파일` 2단계까지.
2. 새 프롬프트는 [`templates/prompt-template.md`](./templates/prompt-template.md) 형식을 따른다.
3. 각 항목에 **대상 모델**과 **마지막 테스트 날짜**를 적는다.
4. 외부 자료는 **출처 링크**를 남긴다.
5. 새 파일을 추가하면 해당 카테고리 README의 파일 목록에도 추가한다.
6. 커밋 메시지: `feat: / docs: / fix: / chore:` (Conventional Commits).

## License

MIT
