# Knowledge Work Plugins: 직무별 방법론 정리

> 원본: [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (Apache-2.0) | 정리일: 2026-11-18 | 분석 기준: `e91a134` (e91a134584eb798bac7fb0379358006a2b63b965)

이 문서는 설치나 실행 방법이 아니라, 각 plugin 안의 SKILL.md에 담긴 방법론(프레임워크, 루브릭, 판단 규칙, 점수 공식, 출력 형식)만 추려 정리한 것이다. 어떤 LLM에서도 프롬프트로 바로 재사용할 수 있도록 원문의 수치와 구조를 그대로 옮겼다.

---

## 1. Plugin 아키텍처 개념

### 1.1 구성 요소

| 구성 요소 | 위치 | 역할 |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | 이름(kebab-case), semver 버전, 설명. `name`만 필수 |
| Skills | `skills/<name>/SKILL.md` (+ `references/`, `scripts/`) | 도메인 지식과 단계별 워크플로. 관련 상황에서 모델이 자동으로 꺼내 쓴다 |
| Commands (legacy) | `commands/*.md` | 사용자가 명시적으로 호출하는 단일 파일 slash command. 현재 UI에서는 skill과 같은 개념으로 통합되었고, 신규 plugin은 skill 형식을 권장한다 |
| Connectors | `.mcp.json` | MCP 서버로 외부 도구(CRM, tracker, warehouse 등)를 연결 |
| Agents / Hooks | `agents/*.md`, `hooks/hooks.json` | 하위 에이전트와 이벤트 훅. Cowork에서는 드물게 사용 |

- 모든 구성 요소는 markdown과 JSON뿐이다. 코드, 인프라, 빌드 단계가 없다.
- SKILL.md는 YAML frontmatter(`name`, `description`, `argument-hint`, `user-invocable`)를 가진다. `description`은 "언제 발동하는가"를 트리거 문장 목록으로 길게 쓴다(예: "Trigger with 'review this design', 'critique this mockup'..."). 즉 description이 라우팅 규칙 역할을 한다.
- `user-invocable: false`인 skill(예: `memory-management`, `task-management`, `knowledge-synthesis`)은 사용자가 직접 부르지 않고 다른 skill이 내부적으로 참조하는 배경 지식이다.
- 긴 지식은 `references/`로 분리해 필요할 때만 읽게 한다(progressive disclosure).

### 1.2 `~~category` placeholder로 도구 추상화

- skill 본문은 특정 제품명 대신 `~~project tracker`, `~~source control`, `~~design tool`, `~~data warehouse`, `~~chat`, `~~knowledge base`, `~~monitoring`, `~~ITSM` 같은 카테고리 placeholder로 도구를 지칭한다.
- 각 plugin 루트의 `CONNECTORS.md`가 "Category | Placeholder | Included servers | Other options" 표로 매핑을 정의한다. 예: `~~source control` = GitHub(포함), GitLab/Bitbucket(대안).
- 결과적으로 워크플로는 도구 독립적(tool-agnostic)이 되고, `.mcp.json`만 바꾸면 회사 스택에 맞춰진다.
- `cowork-plugin-customizer`는 `~~` 접두어를 grep해서 남아 있으면 "Generic plugin setup" 모드로 들어가 placeholder를 실제 값으로 치환한다. 없으면 사용자가 지정한 부분만 고치는 "Scoped customization", 전체를 고치는 "General customization"으로 분기한다. plugin/skill 이름은 절대 바꾸지 않는다.
- `create-cowork-plugin`은 `~~` 패턴을 기본으로 쓰지 말고, 조직 외부 배포가 명시된 경우에만 도입하라고 규정한다.

### 1.3 Standalone + Supercharged 이중 설계

거의 모든 skill이 같은 골격을 따른다.

1. 입력 수집: "What I Need From You"에 필요한 맥락을 열거한다(대화형으로, 한 번에 다 묻지 않는다).
2. 연결 도구가 있으면 끌어오고("If Connectors Available" 절), 없으면 사용자가 준 정보만으로 진행한다. "도구를 연결하라고 요구하지 말고 그냥 진행하라"(write-spec).
3. 고정된 markdown 출력 템플릿을 채운다.
4. Tips 절로 품질을 높이는 사용자 측 요령을 준다.

이 "입력 체크리스트 + 선택적 도구 보강 + 고정 출력 템플릿" 패턴 자체가 재사용 가능한 skill 설계 원칙이다.

### 1.4 Plugin 제작 5단계 (create-cowork-plugin)

Discovery(무엇을, 누가, 어떤 도구와) → Component Planning(필요한 구성 요소 결정) → Design & Clarifying Questions → Implementation → Review & Package. 사용자 대화는 비기술적 언어로 하고 파일 경로나 스키마를 드러내지 않는다. 질문은 이미 답이 나온 것은 건너뛴다.

---

## 2. Engineering

### 2.1 code-review

- 목적: 변경 사항을 보안, 성능, 정확성, 유지보수성 4개 축으로 검토한다.
- 검토 차원별 체크리스트
  - Security: SQL injection, XSS, CSRF, 인증/인가 결함, 코드 내 secret, insecure deserialization, path traversal, SSRF
  - Performance: N+1 query, 불필요한 메모리 할당, hot path의 O(n²), 누락된 DB index, unbounded query/loop, resource leak
  - Correctness: edge case(빈 입력, null, overflow), race condition, 에러 처리와 전파, off-by-one, type safety
  - Maintainability: 이름 명확성, 단일 책임, 중복, 테스트 커버리지, 비자명한 로직의 문서화
- 출력: Summary(1-2문장) → Critical Issues 표(File, Line, Issue, Severity) → Suggestions 표(Category 포함) → What Looks Good → Verdict(Approve / Request Changes / Needs Discussion).
- 판단 요령: "hot path다", "PII를 다룬다" 같은 맥락이 주어지면 그 축에 집중한다.

### 2.2 debug

- 4단계: REPRODUCE(기대 vs 실제, 정확한 재현 절차, 언제부터/누가 영향) → ISOLATE(컴포넌트/서비스/코드 경로 좁히기, 최근 deploy/config/dependency 변경 확인, 로그) → DIAGNOSE(가설 수립과 검증, 코드 경로 추적, 증상이 아닌 root cause) → FIX(설명이 붙은 수정, side effect 검토, 회귀 방지 테스트).
- 출력: Debug Report = Reproduction(Expected/Actual/Steps) → Root Cause → Fix → Prevention(추가할 테스트, guard).
- 규칙: 에러 메시지는 의역하지 말고 원문 그대로 받는다. 최근 변경(deploy, dependency, config)이 1순위 용의자다.

### 2.3 architecture (ADR)

- 3개 모드: ADR 작성, 설계 평가, 시스템 설계.
- ADR 템플릿: Status(Proposed / Accepted / Deprecated / Superseded), Date, Deciders → Context → Decision → Options Considered(옵션별 Complexity, Cost, Scalability, Team familiarity 표 + Pros/Cons) → Trade-off Analysis → Consequences(쉬워지는 것, 어려워지는 것, 다시 볼 것) → Action Items.
- 요령: 제약(출시 기한, 10K rps 등)을 먼저 명시하고, 기울어진 답이 있어도 대안을 이름 붙여 나열해야 균형 잡힌 분석이 나온다. 비기능 요구(latency, cost, 팀 숙련도, 유지보수 부담)를 기능만큼 중시한다.

### 2.4 system-design

5단계 프레임워크.
1. Requirements: 기능 요구, 비기능 요구(scale, latency, availability, cost), 제약(팀 규모, 일정, 기존 스택)
2. High-Level Design: component diagram, data flow, API contract, storage 선택
3. Deep Dive: data model, API endpoint(REST/GraphQL/gRPC), caching, queue/event, error handling과 retry
4. Scale and Reliability: load estimation, 수평/수직 확장, failover/redundancy, monitoring/alerting
5. Trade-off Analysis: 모든 결정의 trade-off를 명시(complexity, cost, team familiarity, time to market, maintainability)

출력 원칙: 다이어그램(ASCII 가능), 명시적 가정, trade-off 분석, 그리고 "시스템이 커지면 무엇을 다시 볼 것인가"를 항상 적는다.

### 2.5 tech-debt

- 6개 범주: Code(중복, 나쁜 추상화, magic number), Architecture(쪼개야 할 monolith, 잘못된 data store), Test(낮은 커버리지, flaky), Dependency(오래된/방치된 라이브러리), Documentation(runbook 부재, tribal knowledge), Infrastructure(수동 배포, 모니터링 부재, IaC 없음).
- 점수 공식: 각 항목을 Impact(1-5, 팀을 얼마나 느리게 하나), Risk(1-5, 안 고치면 무슨 일이), Effort(1-5)로 매긴다.
  - `Priority = (Impact + Risk) x (6 - Effort)`
  - Effort를 6에서 빼서 역수화하므로, 쉬운 일일수록 우선순위가 오른다. 최댓값은 (5+5)x5 = 50.
- 출력: 우선순위 목록 + 항목별 예상 노력과 비즈니스 근거 + 기능 개발과 병행 가능한 단계별 상환 계획.

### 2.6 testing-strategy

- Testing pyramid: Unit(많고, 빠르고, 집중) > Integration(중간) > E2E(적고, 느리고, 신뢰도 높음).
- 컴포넌트별 전략: API는 비즈니스 로직 unit + HTTP 계층 integration + consumer용 contract test. Data pipeline은 입력 검증, 변환 정확성, idempotency. Frontend는 component, interaction, visual regression, accessibility. Infra는 smoke, chaos, load.
- 커버할 것: 비즈니스 핵심 경로, 에러 처리, edge case, 보안 경계, 데이터 무결성. 건너뛸 것: 단순 getter/setter, 프레임워크 코드, 일회성 스크립트.
- 출력: 무엇을, 어떤 테스트 유형으로, 커버리지 목표, 예시 테스트 케이스, 기존 커버리지의 갭.

### 2.7 deploy-checklist

- Pre-Deploy: CI 통과, 리뷰 승인, 알려진 critical bug 없음, migration 테스트, feature flag 설정, rollback 계획 문서화, on-call 통보.
- Deploy: staging 배포/검증 → smoke test → production(가능하면 canary) → error rate와 latency 15분 모니터링 → 핵심 사용자 흐름 검증.
- Post-Deploy: 지표 정상 확인, release note, 이해관계자 통보, 티켓 종료.
- Rollback Triggers를 사전에 수치로 정한다: error rate > X%, P50 latency > X ms, 핵심 흐름 실패. 핵심 원칙: "롤백 기준은 배포 중이 아니라 배포 전에 정한다."
- 맞춤화 규칙: feature flag 사용 시 flag 검증 단계, DB migration 포함 시 migration 전용 점검, breaking API change 시 consumer 통보 단계를 추가한다.

### 2.8 incident-response

- 4단계: TRIAGE(SEV 판정, 영향 시스템/사용자, 역할 지정: IC, comms, responders) → COMMUNICATE(내부 상태 업데이트, 필요 시 고객 공지, war room과 업데이트 주기) → MITIGATE(조치 기록, 타임라인, 해결 확인) → POSTMORTEM(blameless, 타임라인 재구성, 5 Whys, owner가 있는 action item).
- 심각도 기준

| Level | 기준 | 대응 시간 |
|---|---|---|
| SEV1 | 서비스 다운, 전체 사용자 영향 | 즉시, all-hands |
| SEV2 | 주요 기능 저하, 다수 사용자 | 15분 내 |
| SEV3 | 부분 기능 문제, 일부 사용자 | 1시간 내 |
| SEV4 | 외관상/저영향 | 다음 영업일 |

- 상태 업데이트 필수 4요소: 무슨 일인지, 누가 영향받는지, 무엇을 하고 있는지, 다음 업데이트는 언제인지. Status 값은 Investigating / Identified / Monitoring / Resolved.
- Postmortem 템플릿: Summary(2-3문장 평이하게) → Impact → Timeline(UTC) → Root Cause → 5 Whys(5단계 연쇄) → What Went Well / Poorly → Action Items(Owner, P0/P1/P2, Due) → Lessons Learned.
- 규칙: 정보가 불완전해도 즉시 쓰기 시작한다. 업데이트는 사실만, 추측 금지. postmortem은 사람이 아니라 시스템과 프로세스에 초점.

### 2.9 standup

- 출력 3칸: Yesterday(티켓 참조 포함 완료 항목) / Today(계획) / Blockers(맥락과 누가 도울 수 있는지).
- 연결 시 수집원: commit과 PR(opened/reviewed/merged), tracker의 "in progress"/"done" 전환, chat의 관련 논의와 응답 필요 스레드, CI/CD 상태.

### 2.10 documentation

- 문서 유형별 필수 요소: README(무엇/왜, 5분 내 첫 성공 quick start, 설정, 기여), API doc(요청/응답 예시, 인증과 에러 코드, rate limit와 pagination, SDK 예시), Runbook(사용 시점, 사전 권한, 단계, rollback, escalation), Architecture doc(맥락과 목표, 다이어그램, 핵심 결정과 trade-off, data flow), Onboarding(환경, 시스템 연결 관계, 대표 작업 walkthrough, 누구에게 무엇을 물을지).
- 5원칙: 독자를 위해 쓴다 / 가장 유용한 정보를 먼저 / 말하지 말고 보여준다(코드, 명령, 스크린샷) / 최신 유지(낡은 문서는 없는 것보다 나쁘다) / 복사하지 말고 링크한다.

---

## 3. Design

### 3.1 design-critique

- 입력: 디자인 자체, 맥락(무엇, 누구를 위한, 단계: exploration / refinement / final), 선택적 초점.
- 5단계 프레임워크
  1. First Impression(2초): 시선이 처음 가는 곳이 맞는가, 감정 반응, 목적이 즉시 명확한가
  2. Usability: 목표 달성 가능, 내비게이션 직관성, 상호작용 요소의 명확성, 불필요한 단계
  3. Visual Hierarchy: 읽기 순서, 강조 대상, 여백, 타이포 위계
  4. Consistency: design system 준수, spacing/color/type 일관성, 유사 요소의 유사 동작
  5. Accessibility: 대비, touch target, 가독성, alt text
- 피드백 규칙: 구체적으로("CTA가 내비게이션과 경쟁한다" vs "레이아웃이 헷갈린다"), 이유를 원칙/사용자 니즈와 연결, 대안 제시, 잘된 점 인정, 단계에 맞춘 피드백(탐색 단계에 픽셀 지적 금지).
- 출력: Overall Impression → Usability 표(Finding, Severity: Critical/Moderate/Minor, Recommendation) → Visual Hierarchy(시선 첫 지점, reading flow, emphasis) → Consistency 표 → Accessibility → What Works Well → Priority Recommendations Top 3(왜, 어떻게).

### 3.2 accessibility-review (WCAG 2.1 AA)

- 핵심 기준 요약
  - Perceivable: 1.1.1 alt text, 1.3.1 의미적 구조, 1.4.3 대비 4.5:1(일반) / 3:1(큰 글자), 1.4.11 비텍스트 대비 3:1
  - Operable: 2.1.1 키보드로 모든 기능, 2.4.3 논리적 focus 순서, 2.4.7 보이는 focus, 2.5.5 touch target 44x44 CSS px
  - Understandable: 3.2.1 focus 시 예측 가능, 3.3.1 에러 식별, 3.3.2 입력 label
  - Robust: 4.1.2 모든 UI 요소의 name, role, value
- 흔한 결함 8가지: 대비 부족, form label 누락, 키보드 접근 불가, 의미 있는 이미지 alt 누락, modal의 focus trap, ARIA landmark 누락, 제어 없는 자동 재생, 연장 불가 시간 제한.
- 테스트 절차: 자동 스캔(이슈의 약 30%만 잡는다) → 키보드만으로 탐색 → screen reader(VoiceOver, NVDA) → 대비 측정 → 200% 확대 시 레이아웃 붕괴 여부.
- 출력: 이슈 수(Critical/Major/Minor) → POUR 4원칙별 표(Issue, WCAG Criterion, Severity, Recommendation) → Color Contrast 표(전경, 배경, 비율, 요구치, 통과) → Keyboard Navigation 표(Tab 순서, Enter/Space, Escape, Arrow) → Screen Reader 표(낭독 결과, 문제) → Priority Fixes(누구에게 영향, 무엇을 막는지).
- 우선순위 원칙: 대비와 키보드부터(가장 흔하고 영향이 크다), 사용자를 막는 이슈 먼저.

### 3.3 design-handoff

- 포함 범위: Visual(정확한 치수, token 참조, breakpoint, variant/state), Interaction(click/tap, hover, transition의 duration과 easing, gesture), Content(글자 수 제한, truncation, empty/loading/error state), Edge cases(최소/최대 콘텐츠, 긴 다국어 문자열, 느린 연결, 누락 데이터), Accessibility(focus 순서, ARIA, 키보드, SR 낭독).
- 4원칙: 가정하지 않는다(명시하지 않으면 개발자가 추측한다) / 값이 아니라 token(`spacing-md`, 16px 아님) / 모든 state(default, hover, active, disabled, loading, error, empty) / 이유를 적는다("한 손 사용이 많아 모바일에서 접힌다"는 개발자의 판단을 돕는다).
- 출력: Overview → Layout → Design Tokens 표 → Components 표(Variant, Props) → States and Interactions 표 → Responsive 표(Desktop >1024, Tablet 768-1024, Mobile <768) → Edge Cases → Animation 표(Trigger, Duration ms, Easing) → Accessibility Notes.

### 3.4 design-system

- 구성: Tokens(color: brand/semantic/neutral, typography scale, spacing, border, shadow/elevation, motion), Components(variants, states, sizes, behavior, accessibility), Patterns(forms, navigation, data display, feedback).
- 4원칙: 창의성보다 일관성 / 제약 안의 유연성(조합 가능하게) / 문서화되지 않으면 존재하지 않는다 / breaking change에는 migration 경로.
- 3개 모드와 출력
  - audit: Score X/100, 이름 불일치 표, Token Coverage 표(정의 수 vs hardcoded hex/임의 spacing/커스텀 폰트 발견 수), Component Completeness 표(States, Variants, Docs, 10점 만점), Priority Actions.
  - document: Description, Variants(언제 쓰는지), Props 표, States 표, Accessibility(role, keyboard, SR), Do's and Don'ts, 코드 예시.
  - extend: Problem → 기존 패턴 표(유사성, 왜 부족한가) → 제안 API/Variants/States/Tokens → Accessibility → Open Questions.
- 요령: 10개를 100% 문서화하는 것보다 80% 커버리지가 낫다.

### 3.5 user-research

- 방법 선택표

| 방법 | 적합한 목적 | 표본 | 기간 |
|---|---|---|---|
| User interviews | 니즈와 동기의 깊은 이해 | 5-8 | 2-4주 |
| Usability testing | 특정 디자인/흐름 평가 | 5-8 | 1-2주 |
| Surveys | 태도와 선호 정량화 | 100+ | 1-2주 |
| Card sorting | 정보 구조 결정 | 15-30 | 1주 |
| Diary studies | 시간에 따른 행동 | 10-15 | 2-8주 |
| A/B testing | 특정 디자인 선택 비교 | 통계적 유의성 | 1-4주 |

- 인터뷰 가이드 구조(총 50분): Warm-up 5분 → Context 10분(현재 워크플로) → Deep dive 20분 → Reaction 10분(컨셉/프로토타입) → Wrap-up 5분.
- 분석 도구: affinity mapping, impact/effort matrix, journey mapping, Jobs to be done.

### 3.6 research-synthesis

- 입력: 인터뷰 전사, 설문, usability 노트, 지원 티켓, NPS/CSAT, 앱 리뷰.
- 출력: Executive Summary(3-4문장) → Theme별(Prevalence "X of Y participants", Summary, 인용 근거 P#, Implication) → Insights → Opportunities 표(Impact, Effort H/M/L) → User Segments 표(특성, 니즈, 대략 %) → Recommendations(어떤 발견에 근거하는지) → 추가 연구 질문 → Methodology Notes(한계와 편향).
- 3규칙: 원문 인용을 넣는다 / 관찰과 해석을 분리한다("8명 중 5명이 잘못된 버튼 클릭"은 관찰, "버튼 위치가 헷갈린다"는 해석) / 수량화한다("대부분" 대신 "10명 중 7명").

### 3.7 ux-copy

- 5원칙: Clear, Concise, Consistent(같은 것은 같은 용어), Useful, Human.
- 패턴별 공식
  - CTA: 동사로 시작, 구체적으로("Create account", "Submit" 아님), 결과와 label 일치
  - Error: 무슨 일이 + 왜 + 어떻게 고치나
  - Empty state: 이것이 무엇인지 + 왜 비었는지 + 어떻게 시작하나
  - Confirmation dialog: 행동을 명확히("Delete 3 files?", "Are you sure?" 아님), 결과 설명("되돌릴 수 없다"), 버튼은 행동명("Delete files" / "Keep files", OK/Cancel 아님)
  - Tooltip: 간결, 뻔한 말 금지 / Loading: 기대 설정과 불안 감소 / Onboarding: 점진적 공개, 한 번에 한 개념
- 톤 조절: Success는 축하하되 과하지 않게, Error는 공감과 도움, Warning은 명확하고 실행 가능하게, Neutral은 정보적이고 간결하게.
- 출력: 추천 copy → 대안 A/B/C 표(Tone, Best For) → Rationale → Localization Notes(관용구 회피, 문자열 확장, 문화 맥락).

---

## 4. Product Management

### 4.1 write-spec (PRD)

- 맥락 수집 항목(대화형으로 중요한 것부터): 사용자 문제와 겪는 사람, 대상 세그먼트, 성공 지표, 제약(기술, 일정, 규제, 의존성), prior art.
- PRD 8개 섹션
  1. Problem Statement: 2-3문장, 누가 얼마나 자주, 해결 안 하면 비용(사용자 고통, 비즈니스, 경쟁 위험), 근거(리서치, 지원 데이터, 지표)
  2. Goals: 3-5개, 측정 가능, output이 아닌 outcome("time to first value 50% 감소", "온보딩 위저드 구축" 아님), 사용자 목표와 비즈니스 목표 구분
  3. Non-Goals: 3-5개, 각각 제외 이유(영향 부족, 너무 복잡, 별도 이니셔티브, 시기상조)
  4. User Stories: "As a [구체적 user type], I want [capability] so that [benefit]", persona별 묶음, 에러/빈 상태/경계 포함, 우선순위순
  5. Requirements: P0 Must-Have / P1 Nice-to-Have / P2 Future Considerations, 각각 acceptance criteria 포함
  6. Success Metrics: leading과 lagging 지표, 구체 목표치
  7. Open Questions: 답할 주체 태그(engineering, design, legal, data), blocking과 non-blocking 구분
  8. Timeline: hard deadline, 의존성, phasing
- P0 판정 질문: "이걸 빼도 핵심 문제를 여전히 해결하는가?" 아니면 P0. "모든 것이 P0이면 아무것도 P0이 아니다." P1은 곧 만들 확신이 있는 것(위시리스트 금지), P2는 지금 안 만들지만 설계에 반영할 "아키텍처 보험".
- User story 품질: INVEST(Independent, Negotiable, Valuable, Estimable, Small, Testable). 흔한 실수 5가지: 모호함("더 빠르게"), 해법 지정("dropdown을 원한다"), 이득 없음, 너무 큼("팀 관리"), 내부 관점("엔지니어링 팀은 DB를 리팩터링하고 싶다"는 task이지 story가 아님).
- 지표: Leading(일~주 단위: adoption, activation, task completion, time to complete, error rate, 사용 빈도), Lagging(주~월: retention, revenue, NPS, 지원 티켓 감소, competitive win rate). 목표치는 구체적으로("30일 내 50% adoption"), 비교 기능/벤치마크/가설에 근거, success와 stretch 두 단계, 측정 방법(도구, 쿼리, 기간)과 평가 시점(1주, 1달, 1분기) 명시.
- Acceptance criteria: Given/When/Then 또는 체크리스트. happy path + error + edge case, 구현이 아닌 동작, "일어나면 안 되는 것"(negative case) 포함, 각 항목 독립 검증 가능, "빠른", "직관적" 같은 모호어 금지.
- Scope creep 방지: 모든 spec에 non-goal 명시, 범위 추가 시 반드시 다른 범위 삭제나 일정 연장과 교환, v1/v2 분리, 원래 문제 진술 대비 재검토, 조사 time-box("2일 안에 못 풀면 뺀다"), parking lot.
- 출력 규칙: 헤더와 굵은 글씨만 읽어도 요지가 잡히게. 맥락으로 답할 수 있는 질문은 Open Questions에 넣지 않는다.

### 4.2 sprint-planning

- 입력: 팀과 가용성, 스프린트 길이, 우선순위 백로그, carryover, 타 팀 의존성.
- 출력: Sprint Goal(한 문장) → Capacity 표(가용일 X of Y, PTO/on-call) → Backlog 표(P0 must ship / P1 should / P2 stretch, Estimate, Owner, Dependencies) → Sprint Load = 계획 포인트 / 용량 % → Risks → Definition of Done(리뷰/머지, 테스트 통과, 문서, product sign-off) → Key Dates(시작, 중간 점검, 종료/데모, 회고).
- 규칙: 용량의 70-80%로 계획한다. 한 문장으로 못 쓰는 목표는 초점이 없다는 뜻이다. 늦어지면 무엇을 자를지 stretch를 미리 정한다. carryover는 왜 못 끝냈는지 이해한 뒤 재약속한다.

### 4.3 roadmap-update: 우선순위 프레임워크

- RICE = (Reach x Impact x Confidence) / Effort
  - Reach: 기간당 영향 사용자 수(예: 분기당 500명)
  - Impact: 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal
  - Confidence: 100% 데이터 근거, 80% 일부 근거, 50% 직감
  - Effort: person-month(엔지니어링, 디자인 등 전 직군 포함)
  - 용도: 큰 백로그의 정량적, 방어 가능한 비교. 영향 추정이 어려운 전략적 베팅에는 약하다.
- ICE = Impact x Confidence x Ease (각 1-10). 데이터가 부족한 초기 제품의 빠른 정렬.
- MoSCoW: Must / Should / Could / Won't(이번에는). 릴리스나 분기 범위 협상용.
- Value vs Effort 2x2: Quick wins(먼저), Big bets(신중히 범위 설정), Fill-ins(여유 있을 때), Money pits(백로그에서 제거).
- Roadmap 형식: Now/Next/Later, Quarterly Themes, OKR-aligned, Timeline/Gantt.
- 의존성 5유형: technical, team, external, knowledge(리서치 결과 필요), sequential. 관리: owner 지정, need-by 날짜, 버퍼, 팀 경계를 넘는 의존성은 조기 경보, slip 시 contingency. 감소: 단순 버전, interface contract/mock으로 병렬화, 순서 변경, 작업 흡수.
- 용량: 엔지니어는 계획된 기능 작업에 시간의 60-70%를 쓴다(경험칙). 배분 기본값 70% 기능 / 20% 기술 건전성 / 10% 계획 외. 신제품은 기능 쪽, 성숙 제품과 사고 이후는 안정성 쪽으로 조정. "용량 문제를 사람이 더 할 수 있다고 가정해 풀지 말고 범위를 잘라서 풀라. 무언가를 추가할 때는 항상 '무엇을 뺄 것인가'를 묻는다."

### 4.4 stakeholder-update: 상태 보고와 위험 커뮤니케이션

- Green / Yellow / Red 정의
  - Green: 계획대로, 유의미한 위험 없음. 기본값으로 쓰지 말고 실제로 잘 될 때만.
  - Yellow: 계획보다 느리거나 위험이 현실화, 완화 중이나 결과 불확실. 위험의 첫 징후에서 전환(확신할 때까지 기다리지 않는다).
  - Red: 크게 지연, 완화책 없는 주요 blocker, 개입(범위 축소, 인력 추가, 일정 연장) 없이는 약속 실패. 자체 수단을 소진해 escalation이 필요할 때.
  - Green 복귀는 위험이 "멈춘" 것이 아니라 "해결된" 경우에만. 상태 변경 시 이유를 기록한다.
- ROAM: Resolved / Owned / Accepted / Mitigated로 위험을 분류.
- 위험 전달 5단계 문장틀: "[이유] 때문에 [일]이 일어날 위험이 있다" → "그러면 [결과]" → "[근거]로 보아 [가능성]" → "[조치]로 관리 중" → "[구체적 도움]이 필요하다".
- 금지: 좋은 소식 속에 위험 숨기기, 모호한 표현("약간 지연될 수도"), 완화책 없는 위험 제시, 늦은 보고("일찍 알린 위험은 계획 입력, 늦게 알린 위험은 소방 훈련").
- 청중별 템플릿: Executive, Engineering, Cross-functional, Customer/External.

### 4.5 metrics-review: 지표 위계

- North Star: value-aligned, leading(장기 성과 예측), actionable, understandable. 예: 협업 도구 "3명 이상 기여하는 주간 활성 팀", 마켓플레이스 "주간 완료 거래".
- L1(5-7개, 생애주기 단계별): Acquisition, Activation(activation rate, time to activate), Engagement(DAU/WAU/MAU, DAU/MAU stickiness, 핵심 행동 빈도), Retention(D1/D7/D30, cohort curve, churn, resurrection), Monetization(전환, MRR/ARR, ARPU, expansion, NRR), Satisfaction(NPS, CSAT, 티켓).
- L2(진단용): 단계별 funnel 전환, 기능별 사용, 세그먼트 분해, 성능 지표.
- 목표 설정 5요소: Baseline, Benchmark, Trajectory(이미 월 5% 오르는 지표에 6% 목표는 야심이 아니다), Effort, Confidence(commit과 stretch 이중 목표).

### 4.6 synthesize-research

- Thematic analysis 6단계: Familiarization → Initial coding(넉넉하게, 합치기가 쪼개기보다 쉽다) → Theme development → Theme review(근거 충분, 서로 구별, 일관된 이야기) → Refinement(1-2문장 정의) → Report.
- Affinity mapping 규칙: 노트 하나에 관찰 하나, 범주를 미리 정하지 않는다, 너무 큰 cluster는 쪼갠다, outlier를 억지로 넣지 않는다.
- Triangulation: methodological(같은 질문, 다른 방법), source(다른 참가자/세그먼트), temporal(다른 시점). 출처 간 불일치는 오류가 아니라 신호(다른 세그먼트일 수 있다).
- 인터뷰 분석: 행동(하는 것)과 태도(생각하는 것) 구분, workaround는 "변장한 미충족 니즈", 행동 관찰이 진술된 선호보다 강한 증거, 강도 신호(감정어, 빈도, workaround 노력, 실패 시 결과). 인용은 이름이 아닌 유형으로("Enterprise admin, 200명 팀"). 인용은 증거이지 발견이 아니다.
- 설문 함정: 분포 없이 평균만 보고(3.5는 모두 미지근하거나 반반 극단일 수 있다), 무응답 편향 무시, 작은 차이 과해석(NPS 0.1 변화는 노이즈), Likert를 등간 척도로 취급, 교차표의 상관을 인과로.
- Qual-Quant 루프: 질적으로 WHAT/WHY 가설 생성 → 양적으로 HOW MUCH 검증 → 예상 밖 양적 결과를 다시 질적으로 파고든다.
- Persona: 인구통계가 아닌 행동 기반, 3-5개, 데이터로 규모 추정, 제품 결정을 바꾸지 않는 persona는 쓸모없다.
- Opportunity sizing: Impact = 영향 사용자 x 빈도 x 심각도, 여기에 증거 강도, 전략 정합성, 실현 가능성을 함께 본다. 수식을 보여주고, 거짓 정밀도 대신 범위로("월 1,500-2,500명").

### 4.7 product-brainstorming

- 모드: Problem Exploration, Solution Ideation, Assumption Testing, Strategy Exploration.
- 프레임워크: HMW, JTBD, Opportunity Solution Tree, First Principles, SCAMPER, OODA, Reverse Brainstorming.
- 세션 5단계: Frame(무엇을, 왜 지금, 이미 아는 것, 제약, 좋은 결과의 모습) → Diverge(판단 금지, 처음 3-5개 뻔한 아이디어를 넘어서 계속) → Provoke("가장 강한 반론은?", "누가 싫어하고 왜?", "반대가 참이라면?", "10배 야심 버전은?") → Converge(사용자 영향, 실현성, 전략, 증거로 평가해 상위 2-3개, 각각 가장 큰 미지수와 그걸 푸는 가장 싼 방법) → Capture(가정, 질문, 다음 단계, 보류한 아이디어).
- 사고 파트너 행동 규칙: 의견을 낸다, 건설적으로 도전한다("그건 X를 가정한다. 확신하는가?"), 예상 밖 각도, 상대의 열정에 먼저 맞춘 뒤 구멍을 찌른다, 패턴에 이름 붙인다. 하지 말 것: 프레임워크 나열, 목록 던지고 끝내기, 무조건 동의, divergent 단계에서 실현성 평가, 첫 아이디어에 앵커링, 브레인스토밍을 의사결정과 혼동.
- Anti-pattern: framing 전 solutioning, feature parity 함정("경쟁사가 X가 있으니"), 제약에 앵커링, 1-아이디어 브레인스토밍, 분석 마비("지금 하나 고른다면?"으로 수렴 유도), 리서치가 필요한데 브레인스토밍하기.

---

## 5. Productivity: Task와 Memory 시스템

### 5.1 memory-management (2계층 메모리)

- 목표: 사내 약어, 별명, 코드명을 해독해 "ask todd to do the PSR for oracle"을 "Todd Martinez(Finance lead)에게 Oracle Systems 딜($2.3M, Q2 마감)의 Pipeline Status Report 준비를 요청"으로 바꾸는 것.
- 구조
  - Hot cache `CLAUDE.md`: 자주 상호작용하는 사람 약 30명, 흔한 용어 약 30개, 활성 프로젝트 5-15개, 선호. 목표는 일상 해독의 90% 커버, 약 50-80줄(최대 100줄, "hot 30" 규칙). 표 형식.
  - Deep memory `memory/`: `glossary.md`(전체 해독표: 약어, 내부 용어, 별명→실명, 코드명), `people/{name}.md`(별칭, 역할, 보고 라인, 소통 선호, 맥락), `projects/{name}.md`(코드명, 별칭, 상태, 핵심 인물, 맥락), `context/company.md`(도구, 팀, 프로세스).
- 조회 순서(tiered lookup): CLAUDE.md → glossary.md → people/projects → 사용자에게 질문("X가 뭔지 아직 모른다. 알려주면 기억하겠다"). 요청을 실행하기 전에 항상 해독한다.
- 기록 규칙: 용어는 glossary에, 자주 쓰면 CLAUDE.md에도. 사람과 프로젝트는 별명/코드명을 반드시 함께 기록. 파일명은 소문자-하이픈.
- Promotion / Demotion: 자주 쓰거나 활성 작업이면 CLAUDE.md로 승격, 프로젝트 종료/연락 감소/드물게 쓰는 용어는 memory/로만 강등. 과거 정보는 hot cache에서 제거하되 deep memory에는 유지.
- Progressive disclosure: 요청 파싱은 CLAUDE.md만으로, 실행에 필요한 세부(예: Todd는 Slack 선호, 직설적)는 deep memory에서.

### 5.2 task-management (TASKS.md)

- 고정 템플릿 4섹션: Active / Waiting On / Someday / Done.
- 항목 형식: `- [ ] **Task title** - context, for whom, due date`, 완료는 `- [x] ~~Task~~ (date)` 후 Done으로 이동. 약속이면 "for [person]", 마감은 "due [date]", 대기는 "since [date]". Done은 약 1주 보관 후 정리.
- 회의/대화 요약 시 사용자의 약속("I'll send that over"), 할당된 action item, follow-up을 추출하되, 추가 전 반드시 확인을 받는다.

### 5.3 update (동기화와 정리)

- Default 모드 7단계: 현재 상태 로드 → 외부 tracker와 diff(외부에만 있으면 추가 제안, fuzzy 매칭으로 이미 있으면 skip, TASKS.md에만 있으면 stale 의심, 외부에서 완료면 완료 처리 제안) → stale 분류(마감 지남, Active 30일 이상, 맥락 없음 → 완료/재일정/Someday) → 각 task의 엔티티 해독 시도 → 미해독 용어를 묶어서 질문 → task에 담긴 링크, 상태 변화, 관계, 마감을 memory에 반영(예: "launch done"이면 프로젝트 상태 갱신 후 CLAUDE.md에서 강등) → 요약 보고.
- Comprehensive 모드: chat, 보낸 메일, 문서, 캘린더를 스캔해 추적 안 된 약속을 "Possible Missing Tasks"로, 메모리에 없는 반복 등장 인물/프로젝트를 빈도와 함께 제안, 30일간 언급 없는 프로젝트는 정리 제안. 신뢰도별로 묶어 고신뢰는 바로 추가 제안, 저신뢰는 질문.
- 불변 규칙: 사용자 확인 없이 task나 memory를 자동 추가하지 않는다.

---

## 6. Marketing

### 6.1 brand-review

- 가이드라인이 있을 때 4축: Voice and Tone(편차 문장을 지목하고 이유 설명), Terminology(선호/금지 용어, 제품명 표기), Messaging Pillars(승인된 메시지와의 정합), Style Guide(Oxford comma, title/sentence case, 숫자/날짜, 약어 첫 등장 정의).
- 가이드라인이 없을 때 3축: Clarity(첫 문단에 핵심 메시지), Consistency(동의어 혼용 금지), Professionalism(근거 없는 주장).
- 항상 검사하는 법무/컴플라이언스 플래그: 근거 없는 최상급("best", "fastest", "only"), 필요한 면책 문구 누락(금융, 건강, 보증), 경쟁사 비교 주장, 규제 산업 언어, 출처/공개 없는 추천사, 표절에 가까운 의역.
- Severity: High(브랜드 보이스와 모순, 컴플라이언스 위험, 메시지 훼손) / Medium(가이드 불일치지만 해롭지 않음) / Low(사소한 스타일).
- 출력: Summary → Detailed Findings 표(Issue, Location, Severity, Suggestion) → 상위 3-5개 before/after 수정안 → Legal/Compliance Flags 별도.
- Brand voice 문서화 프레임워크 7요소: Personality(사람이라면), Voice Attributes 3-5개, Audience, Messaging Pillars 3-5개, Tone Spectrum, Style Rules, Terminology.
- 속성 정의 4줄 형식: We are / We are not(오해 방지) / This sounds like / This does NOT sound like.
- 7개 스펙트럼: Formality, Authority, Emotion, Complexity, Energy, Humor, Innovation.
- 핵심 규칙: voice는 고정, tone은 맥락에 따라 다이얼을 조절한다. "bold and warm" 브랜드는 출시 때 bold를, 장애 공지 때 warm을 올리되 어느 쪽도 사라지지 않는다. 채널별(블로그, LinkedIn, X, 이메일, 세일즈, 도움말, 보도자료, 에러 메시지)과 상황별(출시, 장애, 고객 사례, 사고 리더십, 온보딩, 나쁜 소식, 경쟁 비교) 톤 표가 있다.

### 6.2 content-creation / draft-content

- 유형별 구조 템플릿: blog, social, newsletter, landing page, press release, case study.
- Headline 공식 7개: "How to [결과] [without 흔한 장애물]", "[숫자] [형용사] ways to [결과]", "Why [통념] is wrong (and what to do instead)", "The [형용사] guide to [주제]", "[이것을 하라], not [저것]", "What [인상적 결과] taught us about [주제]", "[주제]: what [청중] needs to know in [연도]".
- Hook 6유형: 놀라운 통계, 역발상 진술, 질문, 시나리오("Imagine..."), 대담한 주장, 이야기 시작.
- CTA 원칙: 행동 동사, 다음에 일어날 일을 구체적으로, 진짜일 때만 긴급성, 위험 감소("No credit card required"), 페이지/메일당 primary CTA 1개. 배치: landing은 above the fold, 이메일은 가치 제시 후(첫 문장 금지), 블로그는 끝(신뢰를 얻은 뒤), 긴 페이지는 하단에 반복.

### 6.3 기타 marketing skill 요지

- campaign-plan: Objective, Audience, Message, Channel, Measure 5요소 프레임 + 10섹션 brief(개요, 타깃, 핵심 메시지, 채널 전략, 캘린더, 필요 콘텐츠, 지표, 예산, 위험, 다음 단계). 채널은 owned/earned/paid로 구분하고 캠페인 유형(awareness, lead gen, launch, retention, event)별 성공 지표가 다르다.
- competitive-brief: 메시지 비교 매트릭스, content gap, positioning map, battlecard(their pitch, 정직한 강점, 약점, 우리의 차별점, objection handling, 설치할 landmine과 해제할 landmine, win/loss 테마).
- email-sequence: 메일별 subject, preview, 목적, 본문, CTA, timing, segment 조건 + 분기 로직 + A/B 제안.
- performance-report: executive summary → 지표 대시보드 → 추세 → 잘된 점/개선점 → 인사이트 → 권고. attribution 모델 기초와 함정 포함.

---

## 7. Data

### 7.1 write-query (SQL 작성 규칙)

- 요청 분해: 출력 컬럼, 필터, 집계, join, 정렬, limit.
- 방언 확인(PostgreSQL, Snowflake, BigQuery, Redshift, Databricks, MySQL, SQL Server, DuckDB, SQLite) 후 세션 내 기억.
- 구조: 논리 단계마다 CTE 하나, CTE 이름은 서술적(`daily_signups`).
- 성능: 운영 쿼리에서 `SELECT *` 금지, 필터는 base table 가까이, partition 필터 사용, 큰 subquery는 `IN`보다 `EXISTS`, 맞는 join 유형(INNER가 맞으면 LEFT 금지), correlated subquery 대신 join/window, many-to-many 폭발 주의.
- 가독성: 비자명한 로직에 "왜" 주석, 의미 있는 alias(a, b, c 금지), 주요 절마다 줄바꿈.
- 제시 형식: 전체 쿼리 → CTE별 설명 → 성능 메모(비용, partition 사용) → 변형 방법(기간, 단위, 필터 변경).

### 7.2 analyze (질문에 답하는 분석)

- 복잡도 3단계 분류: Quick answer(단일 지표) / Full analysis(다차원, 원인 탐색) / Formal report(방법론, 한계, 권고 포함).
- 흐름: 질문 이해 → 데이터 수집(실패 시 컬럼명/방언 확인 후 재시도, 결과가 이상하면 sanity check) → 분석(복잡하면 하위 질문으로 분해) → 제시 전 검증(row count, null, 크기, 추세 연속성, 소계 합) → 수준별 제시(quick은 답과 쿼리, full은 핵심 발견 먼저, formal은 요약/방법/발견/한계/권고).

### 7.3 validate-data (공유 전 QA)

- 최종 판정 3단계: Ready to share / Share with noted caveats(필수 caveat 목록) / Needs revision(우선순위 있는 수정 목록).
- Pre-delivery 체크리스트 4묶음
  - Data Quality: 출처 확인, freshness("as of" 날짜), 완전성, null 처리, 중복 제거, 필터 검증
  - Calculation: GROUP BY와 grain 일치, 분모 정확성과 0 아님, 같은 길이 기간 비교, join 유형과 many-to-many 팽창, 이해관계자 정의와 일치, 부분합 = 전체
  - Reasonableness: 크기(음수 매출, 0-100% 범위), 추세 연속성, 다른 출처와 교차 확인, 자릿수, 경계 사례
  - Presentation: 막대 차트 0 시작, 축 label, 일관 스케일, 숫자 형식, 제목에 지표가 아닌 인사이트, caveat 공개, 재현 가능성
- 대표 함정과 방지법
  - Join explosion: join 전후 row 수 비교, 엔티티 수는 `COUNT(DISTINCT id)`
  - Survivorship bias: "이 데이터셋에 없는 것은 누구인가?"
  - Incomplete period: 완결 기간만 비교하거나 같은 일수끼리
  - Denominator shifting: 정의 변경을 기록하고 기간 간 동일 정의 유지
  - Average of averages: (100명x$50 + 10명x$200)/110 = $63.64가 맞고, ($50+$200)/2 = $125는 틀리다. 항상 원자료에서 집계
  - Timezone mismatch: UTC로 통일하고 기록
  - Selection bias in segmentation: 결과로 세그먼트를 정의하지 말고 처치 이전 특성으로
  - 기타: Simpson's paradox, 상관을 인과로, 작은 표본, outlier에 끌린 평균(중앙값 검토), 다중 검정/cherry-picking, look-ahead bias, 유리한 기간 선택
- 교차 검증 5기법: 두 가지 방법으로 같은 지표 계산, 개별 레코드 수기 추적, 알려진 벤치마크와 대조, 역산(사용자당 매출 x 사용자 수 ≈ 총매출), 경계 필터(하루, 한 사용자)의 미시 결과 확인.
- Red flag: 이유 없이 50% 이상 변동, 정확히 둥근 수, 정확히 0%나 100%, 가설을 완벽히 확인하는 결과, 기간/세그먼트 간 동일 값(차원이 무시되고 있음).

### 7.4 explore-data (데이터 프로파일링)

- Completeness 등급: >99% non-null Complete(초록), 95-99% Mostly(노랑, null 조사), 80-95% Incomplete(주황, 이유와 영향 이해), <80% Sparse(빨강, 대체 없이는 사용 곤란).
- Consistency: 같은 개념의 다른 표기("USA", "US"), 숫자를 문자열로 저장, 참조 무결성, 비즈니스 규칙 위반(종료일 < 시작일), 컬럼 간 모순(status=completed인데 completed_at null).
- Accuracy red flag: placeholder 값(0, -1, 999999, "N/A", "test"), 한 값의 과도한 빈도, 활성 시스템인데 updated_at 정지, 불가능한 값, 0이나 5로 끝나는 값 편중(측정이 아니라 추정).
- Timeliness: 마지막 갱신, 기대 주기, 이벤트-적재 지연, 시계열 공백.

### 7.5 statistical-analysis 핵심 주의

- 통계적 유의성과 실질적 유의성을 구분하고 항상 effect size, 신뢰구간, 비즈니스 영향을 함께 보고한다.
- 비율에는 그룹당 최소 30 event가 기본 신뢰성 경험칙. 작은 효과(전환율 1%p 변화) 탐지에는 그룹당 수천 관측이 필요할 수 있다. 표본이 작으면 검출력 한계를 명시한다.
- 상관 발견 시 역인과, 교란 변수, 우연을 검토한다. 말할 수 있는 것("X 사용자는 retention이 30% 높다")과 없는 것("X가 retention을 30% 올린다")을 구분한다.
- 다중 비교: 20개 지표를 p=0.05로 검정하면 약 1개는 우연히 유의하다. Bonferroni(alpha / 검정 수) 또는 검정 횟수 공개.

### 7.6 data-context-extractor (회사 데이터 skill 생성기)

- 목적: 데이터 웨어하우스에 대한 사내 지식을 별도 skill로 만들어 분석 정확도를 높인다.
- Bootstrap 질문 5개(대화형): Entity disambiguation("'user'나 'customer'가 정확히 무엇인가, user/account/org 관계와 연결 ID"), Primary identifiers(PK vs business key, legacy ID), Key metrics(가장 많이 묻는 2-3개 지표의 정확한 공식, 기간 관례), Data hygiene(항상 제외할 test/fraud/internal 데이터와 플래그 컬럼), Common gotchas(신입 분석가의 흔한 실수: 헷갈리는 컬럼, timezone, NULL, 이력 vs 현재 상태 테이블).
- 산출 구조: SKILL.md + references/(entities.md, metrics.md, tables/도메인별, dashboards.json). Iteration 모드는 기존 skill의 빈틈만 찾아 targeted discovery 후 갱신한다.

---

## 8. Operations

### 8.1 runbook

- 템플릿: Owner, Frequency, Last Updated/Run → Purpose → Prerequisites 체크리스트(권한, 도구, 입력) → Procedure(단계마다 정확한 명령 + Expected result + If it fails) → Verification → Troubleshooting 표(Symptom, Likely Cause, Fix) → Rollback → Escalation 표(상황, 연락처, 방법) → History 표(날짜, 실행자, 메모).
- 원칙: 고통스러울 만큼 구체적으로("스크립트 실행"이 아니라 "ops 서버에서 `python sync.py --prod --dry-run`"), 단계별 실패 모드 포함, 과정을 모르는 사람에게 실제로 따라 하게 해서 막히는 곳을 고친다.

### 8.2 process-doc (SOP)

- 템플릿: Owner, Last Updated, Review Cadence → Purpose → Scope(포함/제외) → RACI 표(Responsible 수행자, Accountable 책임자, Consulted 자문, Informed 통보) → Process Flow(ASCII) → 단계별 Who/When(trigger)/How/Output → Exceptions and Edge Cases 표 → Metrics 표(Target, 측정법) → Related Documents.
- 원칙: 지저분하게 시작해도 된다. "보통은 X지만 가끔 Y"라는 예외가 문서화할 가치가 가장 큰 부분이다. 역할이 바뀌더라도 현재 누가 하는지 이름을 적는다.

### 8.3 risk-assessment

- 3x3 매트릭스(Likelihood x Impact → Level)

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| High Likelihood | Medium | High | Critical |
| Medium Likelihood | Low | Medium | High |
| Low Likelihood | Low | Low | Medium |

- 6개 범주: Operational, Financial, Compliance, Strategic, Reputational, Security.
- Risk register 필드: Description, Likelihood, Impact, Risk Level, Mitigation(가능성이나 영향을 줄이는 조치), Owner, Status(Open / Mitigated / Accepted / Closed).
- 원칙: 통제 가능하고 중대한 위험에 집중하고, 완화책은 구체적이고 실행 가능하게.

### 8.4 기타 operations skill 요지

- change-request: Assess-Plan-Execute-Sustain 4단계. 영향 분석 표(Users, Systems, Processes, Cost를 H/M/L/None), 위험 표, 실행 계획, 소통 계획(청중, 메시지, 채널, 시점), rollback(trigger, 단계, 검증), 승인. 소통 원칙: what보다 why를 먼저, 잃는 것도 인정한다. "모두"는 영향 평가가 아니다("billing 팀 200명"이 영향 평가다).
- capacity-plan: 목표 가동률 IC 75-80%, Manager 60-70%, On-call/Support 50-60%. 함정: 100% 계획, 회의와 context switching 무시, 휴가 미반영, 모든 시간을 동일 취급. 출력에 Do nothing / Hire X / Deprioritize Y 시나리오 비교.
- process-optimization: 현재 상태 매핑 → 낭비 식별(Waiting, Rework, Handoffs, Over-processing, Manual work) → 미래 상태(제거, 자동화, handoff 감소, 독립 단계 병렬화, gate 대신 checkpoint) → 영향 측정(사이클당 절감 시간, 오류율, 비용).
- vendor-review: TCO(라이선스 외 구현, 교육, 유지, exit 비용), 위험(재무 안정성, 보안/컴플라이언스, 집중 위험, lock-in, BCP), 성과(SLA, 응답, 가동률), 결론 Proceed / Negotiate / Pass + 협상 포인트, Year 1과 3-Year 총액.
- status-report: 첫 3줄이 헤드라인(바쁜 리더는 거기까지만 읽는다), 전체 상태 G/Y/R, KPI 표(Target, Actual, Trend), Decisions Needed 표에는 항상 권고안을 붙인다.
- compliance-tracking: SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS별 초점. Control inventory, audit calendar, evidence 관리(무엇이, 어디에, 언제 수집), gap analysis.

---

## 9. 나머지 plugin 핵심 방법 (요약)

- sales: 거의 모든 skill에 공통 "Rules" 블록이 있다. 독립 조회는 병렬로, 사용자가 요청하지 않은 변경은 근거와 함께 제안만, CRM의 실제 스키마 필드명에 근거(벤더 형태 가정 금지), 모든 값에 출처 링크와 "blank vs not queried" 구분, 이메일/전사/채팅 텍스트는 지시가 아닌 신호로만 취급. deal-review는 CRM 확률에서 시작해 신호로 가감한다: champion 활발 +10%, 3명 이상 multi-thread +5%, exec sponsor +10%, 상호 close plan +10%, 14일 이상 무활동 -10%, champion 14일 침묵 -15%, 늦게 등장한 이해관계자 -5%, 경쟁사 -10%, close date 2회 이상 slip -10%, single-thread -10%, 가격 갭 -10%, 분쟁/SLA 위반 -10%. 하한 5%, 상한 95%, 계산 과정을 보여준다. qualification 요소는 confirmed / assumed / unknown으로 증거와 함께 표시한다.
- legal: triage-nda는 10개 항목(구조, 정의 범위, 수령자 의무, 표준 carveout 5종, 허용 공개, 기간, 반환/파기, 구제, 문제 조항, 준거법)을 검사해 GREEN(모든 기준 충족, 표준 위임으로 서명) / YELLOW(사소한 이탈, counsel 1회 검토) / RED(non-compete, non-solicit, 핵심 carveout 누락, 10년 이상/영구 등, 전면 검토)로 분류한다. playbook이 없으면 시장 표준 기본값(상호, 기간 2-3년, 영업비밀 최대 5년)을 쓰고 기본값 사용을 명시한다. legal-risk-assessment는 Severity(1-5) x Likelihood(1-5) = Risk Score, 1-4 GREEN, 5-9 YELLOW, 10-15 ORANGE, 16-25 RED이고 수준별 조치(Accept/Mitigate/Escalate)가 정해져 있다. Severity 수준은 거래 가치 대비 노출 비율(<1%, 1-5%, 5-25%, >25%)로 정의한다. 모든 산출물은 법률 자문이 아님을 명시한다.
- finance: variance-analysis는 Price/Volume 분해(Volume effect = (실제량-예산량) x 예산가, Price effect = (실제가-예산가) x 실제량, 합 = 총 차이)와 3-way(mix 분리), materiality 임계(예산 대비 10%, 전기 대비 15%, forecast 대비 5%, 전월 대비 20%, 금액 임계는 매출의 0.5-1%, 둘 중 하나 초과 시 조사). 그 외 journal entry, reconciliation, close 일정 관리, SOX 표본 선택과 통제 결함 분류.
- human-resources: interview-prep은 구조화(모든 후보 같은 질문), 역량 기반 4-6개 역량, 역량당 행동 질문 2-3개와 상황 질문 1-2개, rubric scorecard(직감 금지), 다양한 패널. 그 외 comp benchmarking, offer, onboarding(30/60/90), org planning, people report, performance review calibration, policy lookup.
- customer-support: ticket-triage는 9개 카테고리(bug, how-to, feature request, billing, account, integration, security, data, performance)와 P1(1시간 응답, 1-2시간마다 업데이트) / P2(4시간) / P3(1영업일, 3영업일 내 해결) / P4(저영향) SLA, 라우팅 전 중복과 알려진 이슈 확인. 그 외 escalation 패키징, 응답 초안, 해결된 이슈를 KB 문서로 전환.
- enterprise-search: search-strategy는 질문 유형(Decision, Status, Document, Person 등)을 분류해 출처 우선순위와 출처별 쿼리 문법으로 분해한다. knowledge-synthesis는 출처 간 중복 병합(같은 텍스트, 같은 작성자, 가까운 시각, 상호 참조)과 신뢰도 산정(Freshness: 오늘/어제 높음, 한 달 이상 오래됨 표시. Authority: 공식 wiki > 최종 공유 문서 ≈ 공지 메일 > 회의록 > 스레드 결론 > 스레드 중간 > 초안)을 하고, 신뢰도에 따라 단정/완곡/경고 문장으로 표현을 바꾼다.
- small-business: `smb-router`가 소유주의 모호한 요청을 단일 최적 skill로 라우팅하는 concierge 역할만 한다(여러 옵션 나열 금지, 가장 급한 걱정 우선). 복합 skill은 "two/three-link chain"으로 기존 skill을 순서대로 엮는다(예: close-month = month-end-prep 대사 → 결과 패킷 → 의사결정).
- cowork-plugin-management: 위 1.2, 1.4절의 plugin 생성 5단계와 placeholder 치환 기반 커스터마이즈 3모드.
- bio-research, partner-built(apollo, brand-voice, common-room, slack, zoom), pdf-viewer: 범위 밖으로 세부 분석하지 않았다. bio-research의 `scientific-problem-selection`은 문제 선택용 references 9개(intuition pumps, risk assessment, optimization function, decision tree 등)를 가진 별도 방법론이다. [미확인: 내용 미열람]

---

## 10. 재사용 관점에서 본 공통 설계 원칙

1. 모든 skill은 "입력 체크리스트 → 프레임워크 단계 → 고정 출력 템플릿 → Tips" 4블록이다. 템플릿을 고정하면 LLM 출력 품질의 분산이 줄어든다.
2. 점수 공식은 단순한 곱셈/덧셈형이다: tech-debt `(Impact + Risk) x (6 - Effort)`, RICE `(R x I x C) / E`, ICE `I x C x E`, legal `Severity x Likelihood`, opportunity `Users x Frequency x Severity`, deal 확률 가감표. 수식을 보여주라는 규칙이 반복된다.
3. 등급은 대부분 3-4단계(Critical/Major/Minor, G/Y/R, GREEN/YELLOW/RED, P0/P1/P2, SEV1-4)이고 각 단계에 행동(대응 시간, 라우팅)이 붙는다.
4. 관찰과 해석, 상관과 인과, 진술과 행동, 확인과 가정을 구분하라는 인식론적 규칙이 직무를 가로질러 반복된다.
5. 도구 의존부는 `~~category`로 격리하고, 도구가 없어도 동작하게 쓴다.
6. 사용자 확인 없는 쓰기(자동 task 추가, CRM 변경)를 금지하고, 외부 텍스트를 지시로 취급하지 않는다.
