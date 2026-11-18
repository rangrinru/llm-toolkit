# Skills

Claude Skills(`SKILL.md`), Codex/에이전트용 재사용 가능한 **작업 지침 패키지** 모음.

## 구조
```
skills/
├── _template/SKILL.md     # 새 스킬 작성용 템플릿
└── <skill-name>/
    ├── SKILL.md           # 필수: 이름, 설명, 워크플로우
    ├── scripts/           # 선택: 실행 스크립트
    ├── references/        # 선택: 참고 문서
    └── assets/            # 선택: 템플릿, 이미지
```

## 스킬 목록
| 스킬 | 설명 |
|---|---|
| [`hwpx-formatting`](./hwpx-formatting/SKILL.md) | 한글(HWP/HWPX) 문서를 한글 프로그램 없이 고치기: 글 겹침, 띄어쓰기 벌어짐, 끝줄 한 글자, 표 제목 갈라짐, 열 너비 |

## 외부 스킬 (설치해서 쓰는 것)
| 스킬 | 설명 | 설치 | 정리 문서 |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic 공식 스킬 19개 (docx, pdf, pptx, xlsx, frontend-design, skill-creator 등) | `/plugin marketplace add anthropics/skills` | [external/anthropic-skills.md](./external/anthropic-skills.md) |
| [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 다단계 보안 감사 + 독립 검증 | `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit` | [05-code-inspection](../05-code-inspection/security/cloudflare-security-audit-skill.md) |
| [Impeccable](https://github.com/pbakaus/impeccable) | 디자인 명령어 스킬 (bolder, polish, audit...) | `npx impeccable install` | [01-design/impeccable](../01-design/impeccable) |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | 회사/랜딩 사이트 디자인 취향 스킬 | `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"` | [01-design/taste-skill](../01-design/taste-skill) |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HTML로 영상 만들기 | `npx skills add heygen-com/hyperframes` | [02-motion-graphics/hyperframes](../02-motion-graphics/hyperframes) |
| [Claude SEO](https://github.com/AgriciDaniel/claude-seo) | SEO 감사 (26개 이상 하위 스킬) | `/plugin marketplace add AgriciDaniel/claude-seo` | [external/claude-seo.md](./external/claude-seo.md) |
| [Hallmark](https://github.com/Nutlope/hallmark) | AI 티 안 나는 웹 디자인 스킬 (Claude Code, Codex, Cursor, OpenCode) | `npx skills add nutlope/hallmark -g` | [01-design/hallmark](../01-design/hallmark) |

## 작성 팁
- `description`은 "언제 이 스킬을 써야 하는지"를 명확하게 (모델이 이걸 보고 로드 여부를 판단)
- SKILL.md 본문은 짧게, 세부 내용은 `references/`로 분리 (progressive disclosure)
- 반복되는 코드는 프롬프트에 넣지 말고 `scripts/`로

## 참고
- Anthropic Skills: https://github.com/anthropics/skills
- Claude Skills 문서: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
