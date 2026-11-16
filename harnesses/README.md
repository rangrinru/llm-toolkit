# Harnesses

에이전트(Claude Code, Codex CLI, Cursor 등)를 **어떤 환경/규칙/루프로 돌릴지** 정의하는 설정 모음.

## 포함 대상
| 분류 | 예시 |
|---|---|
| 프로젝트 지침 파일 | `CLAUDE.md`, `AGENTS.md`, `.cursorrules` |
| 서브에이전트 정의 | `.claude/agents/*.md` |
| 슬래시 커맨드 | `.claude/commands/*.md`, Codex prompts |
| Hooks | `settings.json`의 PreToolUse / PostToolUse 등 |
| 실행 루프 / 평가 | 자동 테스트-수정 루프, eval 스크립트 |

## 구성
- `CLAUDE.md.template` - Claude Code용 프로젝트 지침 템플릿
- `AGENTS.md.template` - Codex 등 범용 에이전트 지침 템플릿

## 참고
- Claude Code 문서: https://docs.claude.com/en/docs/claude-code/overview
- Codex CLI: https://github.com/openai/codex
- AGENTS.md: https://agents.md
