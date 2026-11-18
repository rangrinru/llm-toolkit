# GitHub 월간 트렌딩: 2026년 11월

> 출처: https://github.com/trending?since=monthly | 확인일: 2026-11-18 | 별 수는 확인 시점 기준

## 한눈에 보기
이번 달 트렌딩 14개 중 13개가 LLM/에이전트 관련. 특히 **AI 티 안 나는 디자인 스킬**(Hallmark, Impeccable, Taste Skill)과 **Agent Skills / 플러그인 생태계**가 강세.

| 레포 | 이번 달 | 한 줄 요약 | 정리 문서 |
|---|---|---|---|
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +44.3k | 다단계 보안 감사 + 독립 검증 스킬 | [05-code-inspection/security](../05-code-inspection/security/cloudflare-security-audit-skill.md) |
| [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +35.7k | Claude Code, Codex 등을 PC/폰에서 제어하는 컨트롤 플레인 | [tools/t3code](../tools/t3code.md) |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +30.2k | 코딩 에이전트용 디자인 어휘 (bolder, polish, critique, audit) | [01-design/impeccable](../01-design/impeccable) |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +26.6k | Anti-AI-slop 디자인 스킬 (50개 테마) | [01-design/hallmark](../01-design/hallmark) (기존) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +20.4k | HTML로 쓰고 영상으로 렌더, 에이전트용 | [02-motion-graphics/hyperframes](../02-motion-graphics/hyperframes) |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | +19.7k | 에이전트에게 디자인 취향을 주는 스킬 | [01-design/taste-skill](../01-design/taste-skill) |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | +18.8k | 에이전트 기반 개인화 학습 워크스페이스 | [tools/deeptutor](../tools/deeptutor.md) |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +17.2k | 세션 간 영속 메모리 (캡처 → 압축 → 주입) | [plugins/claude-mem](../plugins/claude-mem.md) |
| [anthropics/skills](https://github.com/anthropics/skills) | +15.4k | Anthropic 공식 Agent Skills 예제 | [skills/external/anthropic-skills](../skills/external/anthropic-skills.md) |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | +11.2k | Claude Code용 SEO 감사 (26개 이상 하위 스킬) | [skills/external/claude-seo](../skills/external/claude-seo.md) |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | +8.3k | 에이전트용 브라우저 자동화 CLI | [tools/agent-browser](../tools/agent-browser.md) |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +6.6k | 직군별 Claude 플러그인 (engineering, design, sales...) | [plugins/knowledge-work-plugins](../plugins/knowledge-work-plugins.md) |
| [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | +3.5k | 에이전트 계획/diff에 주석 달고 피드백 | [tools/plannotator](../tools/plannotator.md) |

## 카테고리별로 보면
- **디자인** (01): Hallmark, Impeccable, Taste Skill → 비교: [design-skills-compared.md](../01-design/references/design-skills-compared.md)
- **모션그래픽** (02): HyperFrames (Remotion 대안)
- **코드 점검** (05): Cloudflare security-audit-skill
- **스킬** (skills): anthropics/skills, claude-seo
- **플러그인** (plugins): claude-mem, knowledge-work-plugins
- **도구** (tools): T3 Code, Plannotator, agent-browser, DeepTutor

## 이번 달의 공통 흐름
1. **"찾는 에이전트"와 "검증하는 에이전트"를 분리**: security-audit-skill(반증 검증자), Hallmark(새 컨텍스트 리뷰어), Taste Skill(gate), Impeccable(detect)
2. **실제 브라우저 렌더로 검사**: 디자인 스킬 3종 모두 headless Chrome으로 여러 화면 폭을 검사
3. **지어내지 않기**: 가짜 수치, 후기, 로고, 가짜 제품 UI 금지가 디자인 스킬의 공통 규칙
4. **progressive disclosure**: 스킬은 짧게 + references 분리(anthropics/skills), 메모리는 인덱스 → 상세(claude-mem)
5. **하네스 중립**: `npx skills add`로 Claude Code, Codex, Cursor, OpenCode에 같은 스킬 설치

## 제외
| 레포 | 이유 |
|---|---|
| [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | 사용자명으로 SNS 계정을 찾는 OSINT 도구. LLM/에이전트 활용과 무관 |
