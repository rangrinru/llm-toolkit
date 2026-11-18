# 08. Agent Instructions

Claude Code, Codex, Cursor 등 에이전트에게 주는 **지속적인 지침**(프로젝트 규칙, 시스템 프롬프트, 서브에이전트, 커맨드, hooks).

## 폴더 구조
```
08-agent-instructions/
├── claude-code/       # CLAUDE.md, .claude/agents, .claude/commands, hooks
│   ├── CLAUDE.md.template
│   ├── agents/        # 서브에이전트 정의
│   ├── commands/      # 슬래시 커맨드
│   └── hooks/         # settings.json hooks 예시
├── codex/             # AGENTS.md, Codex 설정
├── cursor/            # .cursor/rules
└── system-prompts/    # ChatGPT 커스텀 GPT, Claude Projects용 시스템 프롬프트
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`claude-code/CLAUDE.md.template`](./claude-code/CLAUDE.md.template) | Claude Code 프로젝트 지침 템플릿 |
| [`claude-code/agents/code-reviewer.md`](./claude-code/agents/code-reviewer.md) | 리뷰 전용 서브에이전트 |
| [`claude-code/commands/commit.md`](./claude-code/commands/commit.md) | 커밋 슬래시 커맨드 |
| [`claude-code/hooks/settings.example.json`](./claude-code/hooks/settings.example.json) | hooks 설정 예시 |
| [`codex/AGENTS.md.template`](./codex/AGENTS.md.template) | AGENTS.md 템플릿 (Codex, Cursor 등 공용) |
| [`cursor/project-rules.mdc`](./cursor/project-rules.mdc) | Cursor 프로젝트 규칙 |
| [`system-prompts/personal-assistant.md`](./system-prompts/personal-assistant.md) | 개인 어시스턴트 시스템 프롬프트 |
| [`system-prompts/korean-writing-guide.md`](./system-prompts/korean-writing-guide.md) | 자연스러운 한국어 문장 작성 시스템 지침 (번역투 제거, 단문화, 문체 리듬) |

## 작성 규칙
- 지침은 짧고 구체적으로 (모호한 "잘 해줘" 금지)
- 명령어, 금지 사항, 검증 방법을 반드시 포함
- 실제 프로젝트에서 효과 있었던 문장만 남기고 계속 다듬기

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
