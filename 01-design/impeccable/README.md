# Impeccable 정리

> 원본: [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+30k stars)

**"코딩 에이전트를 위한 디자인 어휘."** `polish`, `bolder` 같은 명령으로 UI를 조향하고, `critique`, `audit`으로 리뷰하고, 출시 전에 AI slop을 잡는 프론트엔드 디자인 스킬. Anthropic의 `frontend-design` 스킬에서 출발했다.

- 지원: Claude Code, Cursor, Codex CLI, GitHub Copilot, Gemini CLI, OpenCode, Devin, Replit Agent, Kiro, Trae 등 + Chrome 확장, VS Code 확장
- [Hallmark](../hallmark)가 "새 페이지를 처음부터 만드는" 데 강하다면, Impeccable은 **기존 UI를 명령어로 다듬고 점검**하는 데 강하다

## 설치
```bash
npx impeccable install          # 이후 도구를 리로드하고
/impeccable init                # 에이전트에서 실행 (Codex는 $impeccable init)
```
- Claude Code 플러그인: `/plugin marketplace add pbakaus/impeccable` 후 `/plugin`에서 설치
- VS Code(Copilot): `code --install-extension renaissance-geek.impeccable`
- 업데이트: `npx impeccable update` (`--providers=claude,codex,cursor --scope=project|global`)
- 텔레메트리 끄기: `npx impeccable telemetry off` 또는 `DO_NOT_TRACK=1`

## 명령어
**사용 패턴: `명령어 + 좁은 대상`** (예: `/impeccable bolder the pricing cards`). 페이지 전체보다 한 섹션을 가까이 보는 게 낫다.

| 그룹 | 명령 | 하는 일 |
|---|---|---|
| Steer (조향) | `bolder` | 밋밋하고 안전한 디자인을 증폭 |
| | `quieter` | 과한 디자인을 톤다운 |
| | `distill` | 불필요한 것 제거 |
| | `colorize` | 회색 UI에 색 입히기 |
| | `typeset` | 폰트, 위계, 크기 수정 |
| | `layout` | 간격과 리듬 수정 |
| | `animate` | 전환, 인터랙션 피드백 추가 |
| | `delight` | 개성 추가 |
| | `overdrive` | 셰이더, 스프링 물리, 스크롤 효과까지 |
| Review (리뷰) | `critique` | 사용성 휴리스틱 기반 점수형 UX 리뷰 |
| | `audit` | 접근성, 성능, 테마, 반응형 기술 점검 (P0 차단 ~ P3 다듬기) |
| Finish (마무리) | `polish` | 출시 직전 최종 패스 |
| | `harden` | 에러, i18n, 오버플로, 엣지 케이스 |
| | `clarify` | 불명확한 카피 재작성 |
| | `adapt` | 화면 크기, 디바이스 대응 |
| | `optimize` | 로딩, 렌더링 성능 |
| | `onboard` | 첫 실행 플로우, empty state 설계 |
| Iterate (실시간) | `live` | 브라우저에서 요소를 골라 variant를 돌려보고 수락하면 소스에 반영 |
| | `generate` | 이름 붙인 요소의 variant 생성 |
| Plan / Setup | `shape` | 코드 전에 UX 계획 |
| | `init` | `PRODUCT.md` 작성 (제품, 사용자, 제약) |
| | `document` | `DESIGN.md` 작성 (시각 시스템) |
| | `extract` | 반복 패턴을 디자인 시스템으로 추출 |
| 기타 | `pin`/`unpin`, `hooks`, `doctor`, `foundations` | 단축 명령, 감지 hook 관리, 설정 점검, 제품 기본기 로드맵 |

```text
/impeccable critique the onboarding flow
/impeccable quieter the landing page
/impeccable polish settings
/impeccable harden checkout
/impeccable redo this hero section
```

## Slop 감지기 (CLI, LLM 없이 동작)
62개의 결정적 규칙으로 AI 티를 검사. API 키 불필요.
```bash
npx impeccable detect src/
npx impeccable detect https://example.com      # 대비/작은 글씨 규칙은 URL 스캔에서만
npx impeccable detect --json .
npx impeccable detect --list-rules
npx impeccable ignores add-value overused-font Inter --reason "Brand font"   # 예외 등록
```
- exit code `2` = 발견 있음, `1` = 스캔 불가 → CI에 넣기 좋음

## 핵심 개념
- **컨텍스트 파일**: 모든 명령이 `PRODUCT.md`(제품/사용자/제약)와 `DESIGN.md`(시각 시스템)를 읽는다
- **Surface 모드**: Persuade(랜딩/마케팅), Operate(앱/대시보드), Read(문서), Experience(포트폴리오). 목적에 맞춰 야심의 크기를 조절
- **네이티브 앱**: `PRODUCT.md`의 `## Platform`을 ios/android/adaptive로 두면 HIG / Material 3 기준

## 설치 없이 응용할 원칙
1. **브리프가 우선**: 사용자가 지정한 미학, 폰트, 팔레트가 AI 취향보다 우선
2. **수정(Refinement)과 재디자인(Redesign)을 구분**: 수정은 기존 정체성과 범위 밖을 보존, 재디자인은 이전 룩을 안티 레퍼런스로 두고 교체. 절충 금지
3. **금지 목록**: 같은 크기 아이콘+제목+텍스트 카드 그리드, 중첩 카드, "큰 숫자 + 작은 라벨" hero-metric 템플릿, 제목 위 eyebrow, 01/02/03 섹션 번호, 그라데이션 텍스트, 장식용 글래스모피즘, 1px 초과 컬러 `border-left/right`, (네오브루탈이 아닌데) 오프셋 하드 섀도, 장식용 모노스페이스, 이모지 아이콘, 업종 습관으로 라이트/다크 선택
4. **수치 기준**: 본문 대비 4.5:1 이상(큰 글씨 3:1), 본문 폭 65~75ch, display 최대 6rem, letter-spacing 하한 -0.04em, 색 배경 위 보조 텍스트는 회색 대신 해당 색조로
5. **모션**: "저작된 순간" 하나만. 모든 섹션에 같은 등장 효과 반복 금지. 지수형 ease-out
6. **상태 완비**: hover, disabled, loading, error, empty, 키보드 포커스. 선택 하이라이트, 캐럿, 스크롤바까지 팔레트로
7. **카피**: 컨트롤은 동작을 이름으로, 에러는 문제와 복구 방법을

## 주의
- **Hook은 모델 승인 밖에서 실행**된다 (모델 명령을 거부해도 hook은 돌고, 첫 편집 시 엔진 바이너리를 내려받을 수 있음)
- `live` 모드는 상황에 따라 로컬 `claude`/`codex` CLI를 승인 우회 모드로 실행할 수 있다. `IMPECCABLE_LIVE_COPY_AGENT=chat` 또는 `off`로 제어. 배포 사이트에는 쓰지 말 것
- 감지기, live, 편집 hook은 웹 전용. 활발히 개발 중이라 명령 수와 규칙 수는 바뀔 수 있음
