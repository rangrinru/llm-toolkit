# AI 디자인 스킬 비교 (Hallmark / Impeccable / Taste Skill / frontend-design)

> 정리일: 2026-11-18 | 2026년 11월 GitHub 월간 트렌딩 상위에 디자인 스킬 3개가 동시에 올라옴

| | [Hallmark](../hallmark) | [Impeccable](../impeccable) | [Taste Skill](../taste-skill) | [frontend-design](https://github.com/anthropics/skills) |
|---|---|---|---|---|
| 만든 곳 | Together AI (Nutlope) | pbakaus | Leonxlnx | Anthropic (anthropics/skills) |
| 라이선스 | MIT | Apache-2.0 | MIT | Apache-2.0 (스킬별 확인) |
| 강점 | **새 페이지를 처음부터** 만들기 | **기존 UI를 명령어로 조향/점검** | **회사/랜딩 사이트** 완성도 | 가볍게 미학 방향 잡기 |
| 방식 | 50개 테마(재료) 중 3개 deal → 히어로 먼저 → sloplint | 24개 명령 (bolder, polish, critique, audit...) + `PRODUCT.md`/`DESIGN.md` | 업종 분류 → 팔레트/폰트/레이아웃 deal → 다중 폭 gate | SKILL.md 지침 |
| 자동 검사 | `sloplint --render` (8개 폭), 새 컨텍스트 리뷰어 | `npx impeccable detect` (62개 규칙, CI 가능) | `gate.mjs` (5개 폭, 최대 3라운드) | 없음 |
| 기존 페이지 | `/hallmark redesign`, `audit` (이름을 불러야만) | 주 용도 | 리디자인 시 브라우저 감사 후 변경 | - |
| 요구 | Node 18+, puppeteer-core + Chrome(렌더 검사) | Node(npx), 엔진 바이너리 자동 다운로드 | Node 22+, Chrome | 없음 |

## 공통으로 금지하는 "AI 티"
세 스킬이 공통으로 막는 패턴. 어느 LLM에서든 프롬프트에 넣을 수 있다.
- 제목 위 **eyebrow / kicker** 라벨
- **아이콘 + 제목 + 설명 카드 3개** 균등 그리드, 카드 안의 카드
- **그라데이션 텍스트**, 보라색 계열 그라데이션, 장식용 글래스/글로우
- **지어낸 수치, 후기, 로고**
- 이모지 아이콘, 장식용 모노스페이스
- 모든 섹션에 같은 등장 애니메이션
- seamless / unlock / elevate / robust 같은 버즈워드

## 언제 무엇을 쓰나
- 아무것도 없는 상태에서 랜딩페이지를 만든다 → **Hallmark** (또는 회사 사이트라면 **Taste Skill**)
- 이미 있는 앱/페이지가 밋밋하거나 과하다 → **Impeccable** `bolder` / `quieter` / `polish`
- 출시 전 점검, CI에 AI 티 검사 넣기 → **Impeccable** `detect`, Hallmark `audit`
- 설치 없이 ChatGPT/Claude.ai에서 → [hallmark/prompts.md](../hallmark/prompts.md)의 압축 프롬프트 + 위 공통 금지 목록
