# LLM Toolkit

Claude, Codex, GPT, Gemini 등 LLM을 더 잘 쓰기 위한 **디자인 프롬프트, 스킬, 하네스, 유용한 프롬프트, 도구, 플러그인**을 모아두는 개인 저장소.

## 구조

```
llm-toolkit/
├── design-prompts/   # UI/UX, 랜딩페이지, 슬라이드, 이미지 생성용 디자인 프롬프트
├── skills/           # Claude Skills(SKILL.md) 및 에이전트 스킬 패키지
│   └── _template/    # 새 스킬 템플릿
├── harnesses/        # CLAUDE.md, AGENTS.md, 서브에이전트, 커맨드, hooks 등 에이전트 실행 설정
├── prompts/          # 코딩/글쓰기/리서치 등 범용 프롬프트, 시스템 프롬프트
├── tools/            # 유용한 AI 도구, CLI, 서비스 목록
├── plugins/          # MCP 서버, Claude Code 플러그인, 에디터 확장
└── templates/        # 프롬프트 작성 템플릿
```

## 카테고리 바로가기

| 카테고리 | 설명 |
|---|---|
| [Design Prompts](./design-prompts) | 디자인 결과물을 뽑아내는 프롬프트 |
| [Skills](./skills) | 재사용 가능한 작업 지침 패키지 |
| [Harnesses](./harnesses) | 에이전트를 돌리는 환경/규칙/루프 설정 |
| [Prompts](./prompts) | 범용 프롬프트 모음 |
| [Tools](./tools) | 도구/서비스 정리 |
| [Plugins & MCP](./plugins) | 기능 확장(MCP, 플러그인) |

## 기록 규칙

1. 새 프롬프트는 [`templates/prompt-template.md`](./templates/prompt-template.md) 형식을 따른다.
2. 각 항목에 **대상 모델**과 **마지막 테스트 날짜**를 적는다. (모델 버전이 바뀌면 결과가 달라질 수 있음)
3. 외부에서 가져온 자료는 **출처 링크**를 남긴다.
4. 커밋 메시지: `feat: / docs: / fix:` 등 Conventional Commits.

## License

MIT
