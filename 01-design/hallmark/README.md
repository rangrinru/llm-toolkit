# Hallmark 정리

> 원본: [Nutlope/hallmark](https://github.com/Nutlope/hallmark) (MIT, Together AI) | 사이트: https://www.usehallmark.com | 정리일: 2026-11-18

**"AI가 만든 티가 나지 않는" 웹 디자인을 만들게 하는 디자인 스킬.** Claude Code, Codex CLI, Cursor, OpenCode에서 동작한다.

## 핵심 아이디어
1. **바닥(Floor)을 강하게 깔고, 그 위는 디자이너에게 맡긴다.** 모델이 습관적으로 만드는 패턴(아이브로우, 자간 넓힌 대문자 라벨, 보라-파랑 그라데이션, 카드 안의 카드 등)을 규칙으로 금지한다.
2. **테마 = 재료(material).** 50개 테마는 종이, 잉크, 서체, 표면, 모션 같은 "재료"만 정의하고, 페이지 구성(섹션 순서)은 정하지 않는다. 같은 테마라도 프롬프트마다 다른 페이지가 나온다.
3. **페이지는 "방문자가 하려는 일(job)"에서 출발한다.** 예약 페이지는 예약을, 쇼핑몰은 구매를 중심으로 구성. 기본 템플릿(히어로 → 기능 3개 → CTA → 이메일 구독 → 푸터) 금지.
4. **지어내지 않는다.** 가짜 수치, 가짜 후기, 가짜 로고, 가짜 "전송 완료" 폼 금지. 없으면 슬롯으로 비워둔다.
5. **실제 브라우저에서 검사한다.** `sloplint`로 8개 화면 폭에서 렌더링해 검사하고, 새 컨텍스트의 서브에이전트가 최종 리뷰.

## 이 폴더의 문서
| 파일 | 내용 |
|---|---|
| [`floor-rules.md`](./floor-rules.md) | 절대 어기면 안 되는 16개 바닥 규칙 (가장 먼저 볼 것) |
| [`ai-slop-gates.md`](./ai-slop-gates.md) | "AI 티" 체크리스트: 색, 타이포, 레이아웃, 카피, 모션, 접근성 |
| [`build-flow.md`](./build-flow.md) | Hallmark의 7단계 빌드 과정과 사전 질문 템플릿 |
| [`genres.md`](./genres.md) | 4개 장르 (editorial, modern-minimal, playful, atmospheric) |
| [`themes-catalog.md`](./themes-catalog.md) | 50개 테마 목록 (배경, 서체, 강조색, 재료) |
| [`macrostructures.md`](./macrostructures.md) | 21개 페이지 구조 + 도메인별 추천 |
| [`custom-direction.md`](./custom-direction.md) | 테마 없이 완전 커스텀으로 디자인할 때의 원칙 |
| [`prompts.md`](./prompts.md) | 바로 쓰는 프롬프트 (스킬 설치 없이 쓰는 압축 버전 포함) |

## 설치
```bash
# 모든 프로젝트에 설치 (Node 18+)
npx skills add nutlope/hallmark -g

# 특정 하네스만
npx skills add nutlope/hallmark -g --agent claude-code   # codex, cursor, opencode, github-copilot

# 브라우저 검사(sloplint --render, 스크린샷)를 쓰려면
npm i -g puppeteer-core   # + Chrome
```

Claude Code 플러그인으로 설치:
```text
/plugin marketplace add nutlope/hallmark
/plugin install hallmark@hallmark      # 호출: /hallmark:hallmark
```

| 하네스 | 설치 위치 | 호출 |
|---|---|---|
| Claude Code | `~/.claude/skills/hallmark` | `/hallmark <프롬프트>` |
| Codex CLI | `~/.agents/skills/hallmark` | `$hallmark <프롬프트>` |
| Cursor / OpenCode | 위 경로를 자동 인식 | `/hallmark <프롬프트>` |

## 주요 명령
```text
/hallmark <만들 페이지 설명>          # 새 페이지 빌드 (테마 3개 중 선택)
/hallmark <설명> custom               # 테마 없이 완전 커스텀
/hallmark redesign ./src/app          # 내용과 동작은 유지하고 디자인만 재구성
/hallmark audit ./index.html          # 수정 없이 리포트만
```
- redesign 옵션: "keep the layout"(스타일만 변경), "polish"(AI 티만 제거)
- 린트만 돌리기: `node skills/hallmark/scripts/sloplint.mjs <파일 또는 폴더> --render`
- 저절로 실행되지 않으면 이름을 직접 부르기: *use hallmark to build ...*

## 게이트 등급
| 등급 | 의미 |
|---|---|
| **Floor** | 절대 배포 불가 (대비, 포커스, reduced motion, 지어낸 사실, 모바일 깨짐 등) |
| **Reflex** | 모델이 습관적으로 빠지는 기본값. 명확한 이유가 있으면 기록을 남기고 예외 허용 |
| **Finish** | 디테일 체크. 답변은 하되 배포를 막지 않음 |

## 함께 보면 좋은 레퍼런스 (Hallmark가 영감을 받은 프로젝트)
- [Impeccable](https://github.com/pbakaus/impeccable)
- [Anthropic frontend-design 플러그인](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)
- [taste-skill](https://github.com/Leonxlnx/taste-skill)
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [Emil Kowalski's skills](https://github.com/emilkowalski/skills)
- [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines)

## 라이선스
원본은 MIT. 이 폴더는 원본 문서를 한국어로 요약/재구성한 것이며, 정확한 규칙은 원본 [`SKILL.md`](https://github.com/Nutlope/hallmark/blob/main/skills/hallmark/SKILL.md)와 [`references/`](https://github.com/Nutlope/hallmark/blob/main/skills/hallmark/references)를 기준으로 한다.
