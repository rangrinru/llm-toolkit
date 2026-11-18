# Impeccable: 핵심 원리 정리

> 원본: [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) | 정리일: 2026-11-18 | 분석 기준: commit `d41d986` (2026-11-16, package 4.9.2, 탐지 규칙 62개)

이 문서는 설치나 사용법이 아니라 Impeccable이 "어떻게 생각하는가"를 정리한다. 원문은 `skill/SKILL.src.md`, `skill/reference/*.md`(명령별 플레이북), `skill/agents/*.md`(서브에이전트), 그리고 Rust 탐지 엔진(`crates/foundation/src/registry.rs`, `crates/core/src/checks/*`, `crates/core/src/browser/*`, `crates/detect/src/regex_matchers.rs`)이다. 원문에서 확인하지 못한 세부는 [미확인]으로 표시한다.

관련 문서: [../hallmark/](../hallmark/), [../taste-skill/](../taste-skill/), [../references/design-skills-compared.md](../references/design-skills-compared.md)

---

## 1. 해결하려는 문제

- 아무 지시 없이 코딩 에이전트에게 페이지를 시키면 모델과 프로젝트가 달라도 같은 결과가 나온다. Inter 일색, 보라에서 파랑으로 가는 그라디언트, 카드 안의 카드, 색 배경 위 회색 글자, 모든 제목 위의 둥근 사각형 아이콘 타일. README는 이것을 "AI slop"이라 부른다.
- 원인은 두 가지로 본다. (1) "멋지게 해줘" 같은 모호한 요청은 모델에게 추측을 맡기고, 추측은 학습 분포의 평균(가장 흔한 룩)으로 수렴한다. (2) 모델은 자기 결과물을 객관적으로 검증하지 못한다. 특히 "이미지를 HTML/CSS로 재현했다"고 믿을 때 실제로는 실패한 경우가 많다고 명시한다.
- 그래서 Impeccable은 세 가지를 준다.
  1. **어휘**: `bolder`, `quieter`, `polish` 같은 동사 하나가 그 한 가지 동작에 맞춘 플레이북을 로드한다.
  2. **리뷰어**: `critique`(휴리스틱 점수 + P0~P3), `audit`(기술 품질 0~20점), 그리고 빌드 후 신선한 맥락의 finish reviewer.
  3. **결정적 탐지기**: LLM 없이 도는 62개 규칙. "slop"(AI 티) 31개 + "quality"(품질 결함) 31개.
- 목표는 "out-of-distribution craft", 즉 분포 바깥의 장인 수준 결과물이다. 수상 경력의 디자인 디렉터처럼 일하라는 것이 스킬의 첫 문장이다.

## 2. 핵심 철학

SKILL.md의 원칙과 "How to design" 규칙을 요약한다.

- **일을 끝낸다.** 얼버무리거나 지름길을 쓰지 않는다. 사용자가 제공해야 하는 자산을 빼고는 완성품을 낸다.
- **야심은 표면의 모드에 맞춰 조절한다.** Persuade와 Experience는 관점이 뚜렷한 대담한 작업. Operate와 Read는 정밀함과 절제가 곧 야심이며, 방문자가 이미 아는 패턴이 자리를 차지할 자격이 있다.
- **렌더된 결과를 실제 출시 크기에서 보고 검증한다.** 단, 확인은 묶어서 한다. 한 번 보고 드러난 것을 다 고친 뒤 다시 본다. 수정마다 스크린샷을 찍지 않는다.
- **브리프가 이긴다.** 지정된 미학, 시대, 소재, 폰트, 팔레트는 "흔한 패턴 경고"와 충돌해도 따른다. 명확한 브리프를 내 취향으로 돌리는 것은 실패다.
- **다듬기(refinement)는 보존하고, 재설계(redesign)는 교체한다.** 다듬기는 기존 정체성, 동작, 카피, 범위 밖 모든 것을 지킨다. 재설계는 제품의 사실, 콘텐츠, 기능, 제약은 지키되 옛 룩은 "증거이자 반(反)참조"로 취급하고 새 세계를 고른다. 둘 사이에서 타협(버린 룩 위에 polish)하지 않는다.
- **시각적 권위는 파일명이 아니라 증거다.** DESIGN.md가 없다고 그린필드가 아니다. 코드에 일관된 정체성이 있으면 그것이 기존 세계다.
- **혐오, 군국주의 상징을 장식으로 쓰지 않는다.** 주제가 그 세계라도 중립적 형태를 쓴다(예: 욱일기 광선, 남부연합기).
- **곁가지 수리 금지.** 디자인 작업 중 발견한 컨텍스트 드리프트(CONTEXT_STALE)는 보고만 하고 고치지 않는다.
- **바닥(floor)은 방향을 정하지 않는다.** 모든 체크가 통과한 뒤 남은 힘은 선택한 세계에 쓴다. "정제된 것"과 "확고히 밀어붙인 것" 사이에서 고민되면 밀어붙인다.

## 3. 컨텍스트 모델

세 층으로 분리한다. 각 층은 서로의 내용을 복사하지 않는다.

| 파일 | 소유하는 것 | 넣지 않는 것 |
|---|---|---|
| `PRODUCT.md` | 지속되는 제품 사실(사용자, 목적, 포지셔닝, 제약, 증거) | 시각 세계, 팔레트, 타이포, 페이지 컨셉, CTA 순서 |
| `DESIGN.md` (+ `.impeccable/design.json` 사이드카) | 지속되는 시각 결정(토큰, 규칙) | 제품 전략, 표면별 컨셉 |
| 표면 브리프 `.impeccable/surfaces/` | 특정 라우트/산출물 하나의 전략, Direction contract | 전역 제품 사실, DESIGN 토큰 복사본 |

### 3.1 PRODUCT.md (`init`이 작성)

스키마 마커 `<!-- impeccable:product-schema 1 -->`를 그대로 복사한다. 이후 버전이 "의도적으로 짧은 기록"과 "섹션이 생기기 전에 쓴 기록"을 구분해 같은 인터뷰를 반복하지 않게 하려는 장치다.

필드와 이유:

- `## Platform`: `web` / `ios` / `android` / `adaptive` 중 하나. 모바일 웹은 web, 웹사이트를 감싼 네이티브 래퍼도 web이다. 이 값이 탐지기 사용 여부와 네이티브 레퍼런스 로드를 결정한다.
- `## Stack`: 그린필드에서만. 스택은 사용자의 결정이므로 한 번 묻고, 위임받았으면 "delegated: 무엇을 왜"로 기록한다(제안이 있었음을 남긴다).
- `## Users`: 주 사용자, 상황, 해야 할 일. critique의 프로젝트별 페르소나가 여기서 파생된다.
- `## Product Purpose`: 무엇을, 왜, 성공의 정의.
- `## Positioning`: 이웃 제품이 정직하게 베낄 수 없는 메커니즘이나 주장.
- `## Operating Context`: 실제 사용 환경, 도구, 문서, 의식(ritual).
- `## Capabilities and Constraints`: 확정 기능, 기술 제약, 용어, 미결 사항.
- `## Brand Commitments`: 사용자가 구속력을 부여한 이름, 보이스, 자산.
- `## Evidence on Hand`: 실제 콘텐츠, 데이터, 후기, 언론 등 경로 포함. **없는 것도 명시**해 후속 작업이 날조하지 못하게 한다.
- `## Product Principles`: 3~5개 전략 원칙. 시각 레시피 금지.
- `## Accessibility & Inclusion`: 확정된 요구가 있을 때만.

인터뷰 규칙: 저장소를 먼저 스캔해 아는 것은 묻지 않는다. 한 라운드 최대 3문항, 새 PRODUCT.md 작성 전 최소 한 번은 실제 답을 받는다. 가장 결정을 많이 바꾸는 3가지(누가 어떤 상황에서 무슨 일을, 무엇이 가능해지며 무엇이 다른가, 보존할 제약/자산/증거)부터 묻는다. **init에서는 미학, 감정, 색, 타이포를 묻지 않는다.** 응답자가 없으면 한 번 실제로 질문을 시도(probe)한 뒤에만 추론하고, 추론한 항목에 라벨을 단다.

부가로 `.impeccable/config.json`의 `buildPath`(comp-first 또는 code-first)를 한 번 묻는다. 사용자가 고른 값만 쓰고, 침묵에서 추론한 값은 저장하지 않는다(아무도 정하지 않은 기본값이 이후 모든 라운드를 조종하게 되므로).

### 3.2 DESIGN.md (`document`가 작성)

Google Labs의 DESIGN.md 포맷 스펙을 따른다. **토큰이 규범이고 산문은 적용 맥락이다.**

- YAML 프론트매터: `name`, `description`, `colors`, `typography`(display/headline/title/body/label 역할별 객체), `rounded`, `spacing`, `components`. 이 다섯 그룹 외에는 넣지 않는다(Stitch의 Zod 스키마가 받지 않음).
  - 토큰 참조는 `{colors.primary}` 형식. 컴포넌트는 원시 토큰을 참조할 수 있으나 원시 토큰끼리는 참조 금지.
  - 컴포넌트 하위 토큰은 8개 속성만: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`. 변형은 `button-primary-hover` 같은 형제 키로.
  - 색 키는 서술적 슬러그(`oxblood-deep`), `blue-800` 금지. 프로젝트가 쓰는 색 형식(hex, oklch)을 그대로 유지하고 진실의 원천을 둘로 나누지 않는다.
- 본문 8개 섹션, 고정 순서, 제목 철자까지 고정: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts. 툴이 정확한 헤더로 파싱하므로 "Color Palette & Roles" 같은 변형 금지.
- Overview는 **Creative North Star**(시스템 전체를 하나의 이름 붙은 은유로, 예: "The Editorial Sanctuary")에서 시작한다.
- **Named Rules**: `**The [Name] Rule.** 짧은 교리` 형식을 섹션당 1~3개. 예: "The One Voice Rule. 주 강조색은 어느 화면에서도 10% 이하." 불릿보다 AI 소비자에게 훨씬 잘 붙는다는 것이 근거다.
- 서술 우선, 정확한 값은 괄호: "부드럽게 굽은 모서리(8px)"가 "rounded-lg"보다 낫다. 각 토큰은 무엇인지보다 어디서 왜 쓰는지 설명한다.
- 사이드카 `design.json`(schemaVersion 2): 프론트매터가 못 담는 것만. 색별 8단계 tonal ramp(어두움에서 밝음, 명도 약 15%~95%, 양끝에서 채도 감소, OKLCH 합성), 그림자, 모션, 브레이크포인트, 5~10개 컴포넌트의 독립 실행 HTML/CSS 스니펫(Tailwind 전개, `ds-` 접두사, 인라인 SVG 아이콘, hover/focus 상태 포함, 리셋 제외), narrative(북극성, 규칙, do/don't 원문 그대로).
- 두 경로: **Scan 모드**(코드에서 추출 후 정성 언어만 사용자에게 확인. 북극성, 무드, 색 이름, 입체감 철학, 컴포넌트 철학을 2라운드 이내로 질문)와 **Seed 모드**(코드가 없을 때 new-work의 세계 워크숍을 거쳐 방향만 기록. 토큰은 `[to be resolved during implementation]`, 컴포넌트 섹션 생략, 사이드카 없음).
- 기존 DESIGN.md는 조용히 덮어쓰지 않는다. refresh / overwrite / merge 중 선택을 받는다.
- **새 세계의 DESIGN.md는 빌드가 끝난 뒤에 쓴다.** 빌드 전에 쓴 규칙집은 현실을 묘사하는 대신 현실에 맞서 방어되고, 디자인 시스템 탐지기에 불안정한 목표를 준다는 것이 이유다.

### 3.3 Direction contract (표면 브리프 안)

새 표면을 만들 때 코드 전에 약 150단어, 6블록으로 기록한다.

- **THESIS**: 이 표면이 소유하는 하나의 아이디어와 거부하는 카테고리 기본 배치.
- **OWN-WORLD**: 콘텐츠를 다 지워도 알아볼 수 있을 만큼 구체적인 팔레트와 컴포넌트 언어.
- **STORY**: 방문자가 이해하고, 믿고, 하게 되는 것.
- **FIRST VIEWPORT**: 무엇이 어디에 어떤 스케일로 있고 주 행동은 어디인지.
- **FORM**: 선택한 형식, 후보 목록에서의 순위, concept-seed가 출력한 시드 참조(`seed:` + 16 hex).
- **FINISH**: 고정 문구 "unreviewed and undocumented is unfinished..." 리뷰, 판정, DESIGN.md, 래스터 출처 기록까지 끝나야 완료.

블록이 분위기(mood)처럼 읽히면 방향이 아직 결정되지 않은 것이다. 계약은 소스, HTML 주석, data 속성, 번들 등 브라우저로 가는 어떤 산출물에도 복사하지 않는다.

## 4. Surface 모드 4종과 판단 기준

모드는 "이 표면에서 방문자의 성공이 무엇인가"를 이름 붙인 것이다. **제품이 아니라 요청된 표면으로 고른다.** 도구의 랜딩 페이지는 Persuade, 패션 하우스의 문서는 Read, 문서 인덱스도 Read다. 모드는 그 표면 브리프에만 저장한다.

| 모드 | 방문자의 성공 | 대상 | 세계(world)가 허용되는 범위 | 기본 빌드 경로 |
|---|---|---|---|---|
| Persuade | 결정하고 행동한다 | 랜딩, 마케팅, 캠페인, 가격 | 페이지를 소유하고 구조화해도 됨 | 이미지 생성 가능 시 comp-led |
| Operate | 과업을 완료한다 | 앱 UI, 대시보드, 에디터, 관리자, 설정 | 타입, 팔레트, 밀도, 시그니처 무브 하나만 | 항상 code-led |
| Read | 무언가를 이해한다 | 문서, 아티클, 가이드, 도움말, 체인지로그 | 프레임만 소유, 읽기 칼럼은 차분하게 | 항상 code-led |
| Experience | 작품 안에 들어간다 | 포트폴리오, 갤러리, 쇼케이스 | 첫 뷰포트부터 작품이 주도, 인터페이스는 물러남 | 이미지 생성 가능 시 comp-led |

모드별 판단 기준(`mode-*.md`, `operate.md`):

- **Persuade**: 첫 화면이 제안을 이해 가능하고 탐나게 만들고, 명확한 행동을 노출하고, 이 제품만 증명할 수 있는 것을 보여야 한다. 행동은 "작동하는 형태"여야 한다(항공사의 노선+날짜 검색, 병원의 예약 가능 슬롯, 상점의 장바구니). 다른 곳을 가리키는 장식 링크는 인정하지 않는다. 세계는 페이지의 "운반체"여야 하고 "그림"이면 안 된다. 뷰포트 전체를 포스터나 책 표지로 칠하고 작동하는 부분이 없으면 실패. 반대 극단인 "헤드라인+서브카피+버튼, 아래 같은 카드 한 줄"도 실패. 분할 히어로(한쪽 카피, 한쪽 제품, 아래 배지 줄)나 중앙 헤드라인+카드 줄은 어떤 세계로 칠해도 템플릿이다. 세계가 오브젝트(책 등)이면 실제 형태를 지킨다(책은 한 거터에 두 페이지, 세 번째 패널 금지).
- **Operate**: 이 종류의 도구를 쓰는 사람이 세계를 알아채기 전에 모든 것의 위치를 알아야 한다. 세계가 빌려주는 것은 정확히 4가지: 타입, 팔레트, 밀도, 시그니처 무브 하나. 레이아웃, 내비게이션 모델, 컨트롤은 절대 제공하지 않는다. 터미널, 계기판, 콕핏 같은 "사용자가 조작하는 도구"를 세계로 가져오면 코스튬이 된다. "회색 화면에 강조색 하나"는 절제가 아니라 카테고리 기본값이다. 셀프체크: 이름을 가리면 이 카테고리의 제품으로 읽히는가, 과업을 할 수 있는가, 카테고리 표준만큼 깔끔하고 그보다 독특한가.
  - 세부 수치: 한 패밀리로 충분한 경우가 많다. fixed rem 스케일(유동 clamp 금지), 단계 비율 1.125~1.2, 산문 65~75ch, 표는 120ch 이상도 가능. 색은 Restrained가 바닥. 모든 인터랙티브 컴포넌트는 default, hover, focus, active, disabled, loading, error 7상태. 로딩은 스켈레톤, 빈 상태는 인터페이스를 가르친다. 트랜지션 150~250ms, 페이지 로드 연출 금지. 모달은 첫 선택지가 아니다.
- **Read**: 독자의 질문이 이끈다. 세계는 프레임(마스트헤드, 내비 레일, 바탕, 제목과 섹션 오프너, 코드/표/콜아웃 조판)을 소유하고 칼럼에 봉사한다. 칼럼은 웹 기준 약 60~75자, 본문 약 16px, 리딩 서체, 실제 대비. 모노스페이스는 코드, 파라미터, 작은 라벨용이고 본문이나 제목 기본값이 아니다. 좋은 후보는 그 세계의 출판 전통(참고서, 서체 견본, 시간표, 도감, 기술 매뉴얼, 학술 장치, 신문 길찾기). 셀프체크: 지금 어디이고 다음은 어디인지 알 수 있는가. 이름을 가리면 다른 제품의 문서일 수도 있는가(그렇다면 프레임이 세계를 덜 가져간 것). 세계가 칼럼까지 들어왔다면 프레임으로 되돌린다.
- **Experience**: 첫 뷰포트부터 작품이 주도한다. 기본적으로 Persuade와 같은 파일의 규칙을 공유한다.

## 5. 명령어 체계의 본질

24개 명령(`craft`는 폐기된 별칭)은 모두 같은 골격을 가진다: `impeccable context`로 PRODUCT/DESIGN/표면 브리프 로드, 해당 플레이북 로드, UI 편집 직전에 craft-floor 로드, 렌더 검증, 마지막에 `polish`로 핸드오프. 인자 없이 호출하면 절대 자동 실행하지 않고, `signals` JSON(디자인 유무, 최근 critique 점수와 P0/P1, git 변경 파일, dev 서버 상태, 플랫폼)과 탐지 결과를 근거로 2~3개 추천을 한 줄 이유와 함께 낸다.

### 5.1 Build: shape, init, document, extract, (new-work)

- **shape**: 코드 없이 확정된 브리프만 낸다. 라운드당 2~3문항, 기본 1라운드. 1라운드는 목적/사람/결과, 2라운드는 소재/동작/경계(실제 콘텐츠 범위의 최소/보통/최대, 상태, 충실도, 건드리면 안 되는 것, "다듬어졌는데도 틀렸다고 느껴질 조건"). CSS 값이나 "미학 레인"은 묻지 않는다. 브리프 7항목(과업과 청중, 결과와 증거, 선택한 방향, 범위와 경계, 상태와 범위, 인터랙션과 레이아웃 의도, 제약과 미결). 확인받고 멈춘다.
- **new-work(새 표면, 세계 교체)**: 가장 무거운 흐름.
  1. 이미 사실인 것 판별: 재설계 / 기존 세계 / 불완전한 브랜드 / 시드된 세계 / 시각 권위 없음.
  2. 모드별로 2~3문항. 새 세계에서는 concept-seed 전에 룩을 제안하지 않는다(질문에 이름 붙인 방향이 곧 답이 확정하는 방향이 되므로).
  3. 발명량 결정: 기존 표면 확장(토너먼트 없음) / 기존 세계 안의 새 표면(내용에서 5~7개 구조 도출, 스크립트가 3개를 "딜"해 순위 고착을 깸) / 세계 생성 또는 교체.
  4. 세계 워크숍(`new-work-world.md`): 제품 메커니즘 한 문장, 청중의 실제 장면, 문화적 고향. 이 카테고리가 늘 내는 페이지와 그 예측 가능한 반대를 "rut(바퀴자국)"로 명시하고 후보에서 뺀다. 청중이 외우고 있는 시각 시스템/유물/장소/의식 7개를 공명 순으로. 3개 넘게 같은 소재 계열이면 더 파서 최소 3계열. Operate/Read에서는 청중이 조작하는 도구를 후보로 쓰지 않는다. 그 다음 **concept-seed 스크립트를 반드시 실행**한다(건너뛰면 계약 위반). 스크립트가 빌드할 방향을 배정하고 카탈로그 도전자를 딜한다. 도전자는 형식과 시스템 문법만 주고 사실은 제품이 준다. 판정 축은 정확히 둘(청중 동일시, 제품 명확성): wins / competitive / declined. 진 도전자의 "규율"(팔레트의 완전한 헌신, 그리드의 밀도 용기)은 배정 방향에 "raise"로 이식하되 옷(버튼 그림자, 디스플레이 서체)은 가져오지 않는다. 결정 페이지에 배정 방향, IMPECCABLE'S PICK 카드 1장(내 1순위가 배정과 다를 때만), 도전자 최대 3장, 카테고리 표준을 그대로 하는 "standing exit"를 둔다. 재추첨은 plain/safer/bolder 세 레지스터.
  5. 세계 확정: 색 전략 먼저(Restrained: 세계에서 틴트한 중립+강조 1 / Committed: 채도 높은 한 색이 표면의 30~60% / Full palette: 3~4개 이름 붙은 역할 / Drenched: 표면 자체가 색). 다크/라이트는 기본값이 아니라 "누가, 어디서, 어떤 빛 아래" 한 문장으로 강제한다.
  6. Direction contract 기록, comp-led면 시안 3장(visualize) 후 측정 계약 빌드, code-led면 계약의 FIRST VIEWPORT와 시그니처 인터랙션이 야심을 운반.
  7. 검사(데스크톱+모바일, 사용자 실제 뷰포트, 모든 상태 구동), 최대 2라운드. 웹은 탐지기 1회. 그 후 신선한 finish reviewer, 판정 단어대로 행동, documenter가 DESIGN.md 작성.
  - 빌드 원칙: 첫 뷰포트는 헤더가 아니라 논지다("한 시간 뒤 무엇을 묘사할까?"의 답이 무드면 실패). 주장 말고 증명(시연 데이터는 고품질로 만들고 synthetic 라벨, 주장은 날조 금지). 자산을 만들고 크롬으로 대체하지 않는다(그라디언트, 글래스, 아이콘 타일, 다꼭짓점 clip-path가 빈칸을 가린 것). 세계가 기법(canvas, WebGL, view transitions)을 지명하면 정적 모방 말고 기법 자체를 만든다. 스튜디오처럼 스크롤 페이스를 짠다(밀도 높은 구간 다음 조용한 구간, 진짜 마무리).
  - 폰트 금지 목록(Persuade/Experience에서 "찾기를 멈췄다는 신호"): Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, display로 쓴 Inter, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans. 쓰려면 다른 서체로는 안 되는 이유가 필요하고, "책이니 세리프" 같은 주제 연상은 이유가 아니다.
  - 보정(calibration): AI 인터페이스가 몰리는 4개 룩. (a) 따뜻한 크림 바탕+고대비 세리프 디스플레이+테라코타/시그널 레드 강조, (b) 거의 검정+네온 강조 하나+빛나는 테두리, (c) 신문식 헤어라인+이탤릭 세리프+작은 트래킹 모노 라벨, (d) 평면 고채도 잉크+검은 박스+하드 오프셋 그림자+굵은 콘덴스드. 브리프가 요구하면 정당하지만 자유로운데 여기 착지하면 셀프체크 실패. 카테고리만으로(또는 카테고리+회피만으로) 미학을 맞힐 수 있으면 다시 한다. Claude 전용 블록은 "따뜻하고 책 같고 가족, 아이 대상 주제에서 크림, 세리프 이탤릭, 램프빛으로 가는 렌디션 편향"을 명시하고 첫 팔레트를 "이미 소진됨"으로 취급하라고 한다.
- **document**: 3.2 참조.
- **extract**: 같은 의도로 3회 이상 쓰인 것만 추출. "섣부른 추상화는 중복보다 나쁘다." 비슷해 보여도 의도가 다르면 분리 유지. 발견, 패턴 식별, 계획, 추출과 보강, 마이그레이션(모든 인스턴스 교체, 옛 구현 삭제), 문서화.

### 5.2 Evaluate: critique, audit

6장 참조.

### 5.3 Refine: polish, bolder, quieter, distill, harden, onboard

- **polish**: 다듬기이며 숨은 재설계가 아니다. 컨셉 자체가 틀렸으면 그렇게 말하고 redesign이나 bolder를 권한다.
  1. 드리프트를 4종으로 분류하고 가장 좁은 올바른 레벨에서 원인을 고친다: missing token / one-off implementation / conceptual mismatch / local defect.
  2. 최근 critique 스냅샷을 백로그로 읽는다. 파일 내용 지문이 바뀌었으면 그 백로그는 닫힌 것으로 본다.
  3. 트리아지 순서: (1) 막힌 과업, 데이터 손실, 오해를 부르는 상태, 접근 불가 경로 (2) 로딩/빈/오류/성공/비활성/권한 상태 누락 (3) 흐름, 위계, 반응형, 시스템 드리프트 (4) 시각과 모션 불일치 (5) 코드와 자산 정리.
  4. 한 구석만 완벽하게 하고 나머지를 같은 바 아래 두지 않는다. 처리한 P0/P1을 모두 해결했을 때만 스냅샷을 닫는다.
- **bolder**: "범위는 주권"이다. 지목된 대상만 건드리고 새 색, 폰트, 반경, 그림자를 추가하지 않는다. 섹션이 밋밋한 이유는 이웃 섹션이 이미 해결한 시스템의 가장 강한 수(풀 강도 디스플레이 타입, 시그니처 모티프, 밀도와 페이스)에서 조용히 빠졌기 때문이다. 시스템이 가진 것을 증폭한다. 하나를 완전히 하고 주변을 조용히 한다("모든 요소가 커지면 섹션은 더 평평해진다"). **스켈레톤 테스트**: 카피를 다 빼도 구조만으로 이 섹션이 무엇이고 왜 중요한지 말하는가. 효과를 더 넣는 반사는 대담함의 반대다.
- **quieter**: 조용한 디자인이 더 어렵다. Persuade에서는 팔레트 절제, 여백, 타입의 숨, Operate에서는 노이즈 제거. 수치: 채도를 70~85%로, 색은 강조로만(10% 규칙), 굵기 900→600, 700→500, 모션 거리 40px→10~20px, ease-out-quart, bounce 금지, 색 위 회색 금지(그 색의 어두운 셰이드). "조용한" 것이 "회색 글자, 균일 굵기 산세리프, 동일 카드 그리드" 같은 generic이 되면 실패.
- **distill**: 주 목표는 하나. 장식/브랜드 색 1~2개+중립(의미 색은 유지하되 비색상 단서 동반), 폰트 한 패밀리, 크기 3~4개, 굵기 2~3개. 카드 안 카드 금지, 기본 레이아웃에 카드 불필요. 주 행동 하나, 보조 몇 개, 나머지는 3순위나 숨김. 능동태, 반복 카피 제거.
- **harden**: 완벽한 데이터에서만 작동하면 프로덕션이 아니다. 극단 입력(아주 긴/짧은 텍스트, 이모지, RTL, 억 단위 숫자, 1000개 이상 항목, 빈 상태), 오류(오프라인, 400/401/403/404/500, 레이트 리밋, 동시성), i18n(독일어 약 30% 더 김, 30~40% 여유, 로케일 숫자/날짜/통화). 모바일 본문 16px 최소(iOS Safari는 16px 미만 입력에 포커스 시 강제 확대). 200% 확대 테스트. 페르시아어 ZWNJ(U+200C) 보존, 아랍/페르시아 Yeh, Kaf 변형은 저장은 원형, 검색은 동치.
- **onboard**: 목적은 제품을 가르치는 것이 아니라 "aha 순간"까지 최단 시간. 보여주기, 건너뛰기 허용, 핵심 개념 1~3개, 빈 상태는 온보딩 기회(무엇이 나타날지, 왜 가치 있는지, 첫 항목 CTA, 템플릿).

### 5.4 Enhance: animate, colorize, typeset, layout, delight, overdrive

typeset, layout, colorize는 같은 구조를 공유한다: **두 개의 격리된 평가**(설계 평가를 먼저, 그 다음 `detect --scope type|layout` 기계 스캔. 탐지 결과가 설계 판단을 앵커링하지 않도록 순서를 지킨다) 후 종합, 시스템 선언, 적용, 증거 기반 검증("예"만으로 검증 불가, 렌더나 소스 증거로 답한다), polish 핸드오프. 수치는 7장에 모았다.

- **animate**: 모션은 상태, 관계, 위계를 설명하거나 표면이 획득한 "작성된 순간" 하나를 만든다. 계획 4요소(Focal moment, Continuity, Feedback, Budget). 일반적인 fade-and-rise, hover lift, 패럴랙스, 스크롤 리빌은 논지가 아니다. 소재는 의미로 고른다(연속성: shared element, FLIP, view transition / 초점: 제한된 blur, backdrop / 리빌: mask, clip-path / 에너지: 색, 그라디언트 위치, 셰이더). 검증은 `motion-capture`로 일반 모드와 reduced-motion 각각 프레임(이전, 첫 애니메이션, 중간, 마지막, 안정)을 찍고 motion reviewer에게 넘긴다.
- **colorize**: 색은 스와치 묶음이 아니라 역할 체계(캔버스와 상승 표면, 1차/2차 텍스트, 행동/포커스/선택, 경계, 성공/경고/오류/정보, 데이터 범주). 새 웹 팔레트는 OKLCH. 색상(hue)은 제품 의미와 시각 방향에서 고르고 카테고리 연상에서 고르지 않는다. 가장 강한 색은 흩뿌리지 말고 한 영역이나 역할을 소유하게 한다. 다크 모드는 기계적 반전 금지. 반투명 오버레이 사슬보다 명시적 색(알파는 대비를 맥락 의존적으로 만든다).
- **delight**: 범용 위트가 아니라 유용한 상호작용에서 드러나는 제품 성격. "한 문장 delight thesis"(사용자가 무엇을 왜 느껴야 하는가). 반응 강도는 빈도와 결과에 비례(루틴 저장은 확실하게만, 큰 마일스톤은 확장). 기다림을 가짜 작업으로 늘리지 않는다. 돈, 손실, 프라이버시 오류에 농담 금지. 100번째 사용에도 만족스러워야 한다.
- **overdrive**: 오작동 위험이 가장 크다. **코드 전 2~3개 방향을 제안하고 선택받는다**(브라우저 지원, 성능 비용, 복잡도 트레이드오프를 옵션 안에). "비범함"은 맥락이 정한다. 포트폴리오의 파티클은 인상적이지만 설정 페이지에서는 민망하다. 대신 설정 페이지의 즉시 낙관적 저장은 비범하다. 기능 UI의 "와우"는 느낌(트리거에서 모핑하는 다이얼로그, 10만 행 60fps 가상 스크롤).

### 5.5 Fix: clarify, adapt, optimize

- **clarify**: 상태마다 (1) 지금 필요한 사실 하나 (2) 다음 행동 (3) 결정을 바꾸는 맥락 (4) 톤을 정한다. 각 아이디어는 한 번만. 버튼은 제스처가 아니라 결과를 말한다. 파괴적 행동은 대상과 결과를 명시하고, 복구가 안전하면 확인 대화상자보다 undo. 확인 시 Yes/No/OK 대신 행동 이름. 오류는 무엇이 실패했나, (알면) 왜, 어떻게 복구하나. 진행률은 꾸며내지 않는다. 플레이스홀더는 라벨이 아니다.
- **adapt**: 적응은 스케일링이 아니라 맥락에 맞춘 재고다. 모바일은 단일 칼럼, 하단 내비, 44x44px 터치, 바텀시트, 16px 텍스트. 태블릿은 2칼럼, master-detail. 데스크톱은 다중 패널, 4K에서 늘어나지 않게 max-width, 단축키.
- **optimize**: 측정 전후 비교. 느리지 않은 것은 최적화하지 않는다. 읽기/쓰기 일괄 처리(layout thrashing 방지), 이미지 80~85% 품질, `content-visibility: auto`, 가상 스크롤.

### 5.6 Iterate: live, generate

- 브라우저에서 요소를 고르고 액션을 고르면 HTML+CSS 변형이 HMR로 교체된다. generate는 "요소, 방향, 개수"를 한 문장으로 받는 고속 레인(숫자 없으면 3개, 최대 8개). 방향 단어를 고정 액션 어휘로 매핑(bold 계열은 bolder, calm 계열은 quieter, simpler는 distill, 폰트 단어는 typeset, 색 단어는 colorize, 배치 단어는 layout, 장치 단어는 adapt, 모션은 animate, 장난스러움은 delight, 규칙 파괴는 overdrive, 그 외 의도는 `impeccable`+프롬프트).
- 변형마다 거친 파라미터 하나를 CSS 변수로 노출해 재생성 없이 조정한다: typeset은 `scale`(0.85~1.3), layout은 `density`(0.6~1.4), colorize는 `color-amount`(0~1, 기본 0.5).

## 6. critique와 audit 채점 루브릭

### 6.1 critique (UX 디자인 리뷰)

**구조적 불변식**:

- 두 평가가 필수다. Assessment A(디자인 리뷰, LLM 판단)와 Assessment B(탐지기+브라우저 오버레이 증거).
- 서브에이전트 도구가 있으면 **반드시 두 개의 격리된 서브에이전트**로 병렬 실행한다. 서로의 출력을 보지 않는다. A가 끝나기 전에는 탐지 결과가 부모의 종합 맥락에 들어오지 않는다(결정적 출력도 판단을 앵커링하므로).
- 인라인 실행은 서브에이전트가 없을 때만 허용되며, 보고서 첫 줄에 `DEGRADED: single-context (<사유>)` 배너를 단다. "조용한 degraded critique는 실패한 critique."
- 네이티브 플랫폼은 B가 적용되지 않아 A만 실행하고 배너 없음.
- 보고서를 채팅에 먼저 전부 쓰고, 질문은 맨 마지막. 질문 없이 끝나면 미완료 실행(Priority Issue 3개 미만일 때만 `Questions skipped: <사유>` 허용).

**Assessment A 루브릭** (`critique-rubric.md`):

1. **Design specificity**: 이 제품을 위해 만들어졌는가, 무관한 제품이 그대로 써도 되는가. 탐지 결과를 보기 전에 판단한다. 보고서는 이 판정부터 시작한다.
2. **Cognitive load 체크리스트 8항목**: Single focus, Chunking(그룹당 4개 이하), Grouping, Visual hierarchy, One thing at a time, Minimal choices(결정 지점 가시 옵션 4개 이하), Working memory(이전 화면 기억 필요 여부), Progressive disclosure. 실패 0~1개 낮음, 2~3개 보통, 4개 이상 높음(치명).
   - Working Memory Rule(Cowan 2001): 결정 지점 동시 고려 항목 4개 이하 관리 가능, 5~7개 경계, 8개 이상 과부하. 적용: 주 버튼 1, 보조 1~2, 나머지 메뉴. 최상위 내비 5개 이하. 문서 사이드바 레벨당 형제 4개. 갤러리 인덱스는 화면당 결정 하나.
   - 8대 위반 패턴: Wall of Options, Memory Bridge, Hidden Navigation, Jargon Barrier, Visual Noise Floor(1개 주, 2~3개 보조, 나머지 음소거로 해결), Inconsistent Pattern, Multi-Task Demand, Context Switch.
3. **Nielsen 10 휴리스틱을 각 0~4점**. 4는 "충분히 좋음"이 아니라 진짜 탁월함. 각 휴리스틱에 0~4 기준표가 있다(예: 1번 시스템 상태 가시성은 0 피드백 없음, 2 부분적, 4 모든 행동이 확인되고 진행이 항상 보임). "대부분의 실제 인터페이스는 40점 중 20~32점."
   - Persuade/Experience 표면에서는 7번(유연성과 효율)과 10번(도움말)을 `n/a` 처리 가능. 최대점을 재정규화(예: 24/32)하고 밴드는 백분율로 읽는다.
4. **Emotional journey**: peak-end rule, 감정 골짜기, 고위험 순간의 안심.
5. **페르소나 레드플래그**: 5개 원형 중 2~3개 + PRODUCT.md `## Users`에서 1~2개 파생.
   - Alex(성급한 파워유저): 60초 내 핵심 과업, 단축키, Esc로 모달 닫기, 일괄 작업.
   - Jordan(혼란스러운 첫 사용자): 5초 안에 첫 행동이 명확한가, 아이콘에 텍스트 라벨, 단계마다 back/undo.
   - Sam(접근성 의존): 키보드만으로 완주, 보이는 포커스, 4.5:1, 200% 확대, 상태 변화 낭독.
   - Riley(의도적 스트레스 테스터): 0개/1000개/아주 긴 텍스트, 새로고침 중 상태, 이모지/RTL/엑셀 붙여넣기.
   - Casey(산만한 모바일): 엄지 영역(화면 하단 절반), 중단 후 복귀 시 상태 보존, 3G, 44x44pt.
   - 선택표: 랜딩은 Jordan, Riley, Casey / 대시보드는 Alex, Sam / 이커머스는 Casey, Riley, Jordan / 온보딩은 Jordan, Casey / 데이터는 Alex, Sam / 폼은 Jordan, Sam, Casey.
   - 일반적 페르소나 설명이 아니라 "무엇이 그 사람에게 깨졌는가"를 요소 이름으로 쓴다.

**점수 밴드(40점 만점)**: 36~40 Excellent, 28~35 Good, 20~27 Acceptable, 12~19 Poor, 0~11 Critical. n/a가 있으면 백분율로 90%+, 70%+, 50%+, 30%+, 그 미만.

**P0~P3 심각도** (critique, audit 공통):

| 등급 | 이름 | 정의 | 조치 |
|---|---|---|---|
| P0 | Blocking | 과업 완료를 완전히 막음 | 즉시 수정 |
| P1 | Major | 큰 어려움이나 혼란(audit에서는 WCAG AA 위반 포함) | 릴리스 전 수정 |
| P2 | Minor | 불편하지만 우회 가능 | 다음 패스 |
| P3 | Polish | 실사용 영향 없음 | 시간 날 때 |

판정 팁: "사용자가 이 문제로 고객지원에 연락할까?" 그렇다면 최소 P1.

**보고서 구성**: 헤더 출처 표기(dual-agent / degraded / native) → 휴리스틱 표 → Design Specificity Verdict(LLM 평가, 결정적 스캔, 오버레이) → 전체 인상 → 잘 되는 것 2~3 → Priority Issues 3~5개(각각 P등급, 무엇, 왜 중요, 수정, 추천 명령) → 페르소나 레드플래그 → 사소한 관찰 → 도발적 질문. 스냅샷을 `.impeccable/critique/`에 저장(점수, 최대점, n/a 목록, P0/P1 수)하고 최근 5회 추이 한 줄. 이후 질문 2~4개(우선 영역, 톤 의도, 범위, 제약), 각각 발견 사항에 묶인 2~3개 옵션. 답을 받은 뒤 명령 순서 추천, 마지막은 항상 polish.

### 6.2 audit (기술 품질, 웹 전용)

수정하지 않고 문서화만 한다. 5차원 각 0~4점, 합계 20점.

| 차원 | 확인 항목 | 0점 / 4점 기준 |
|---|---|---|
| Accessibility | 대비 4.5:1(큰 글자 3:1, AAA 7:1), reduced-motion 대안(전역 0.01ms 킬은 유용한 피드백까지 파괴하므로 지적), ARIA, 키보드, 시맨틱, alt, 폼 | WCAG A 실패 / AA 완전 충족, AAA 근접 |
| Performance | layout thrashing, 무제한 blur/filter/shadow, lazy loading, will-change 남용, 번들, 리렌더 | 심각 / 빠르고 가벼움 |
| Theming | 하드코딩 색, 다크 모드, 토큰 혼용, 테마 전환 | 토큰 없음 / 완전한 토큰+다크 모드 |
| Responsive | 고정 폭, 터치 타깃 44x44(WCAG 2.5.8 최소 24x24 CSS px, 24px 원 간격 예외), 터치 제스처(mouse 전용 핸들러, touch-action 누락, 취소 시 드래그 상태 미해제), 가로 스크롤, 텍스트 확대 | 데스크톱 전용 / 모든 뷰포트+제스처 동작 |
| Implementation Integrity | 탐지기 실행 후 맥락 검증, 반복 지름길, 시스템 드리프트, 오해 소지 콘텐츠, 교체 가능한 구조 | 체계적 드리프트 / 일관되고 의도적 |

- RTL 규칙: `<html>`/`<body>`에 `dir="rtl"`이 선언된 페이지에서만 물리 방향 속성(margin-left 등)을 지적한다. `lang`만으로는 방향이 정해지지 않는다. `left:50%; transform:translateX(-50%)`는 방향 무관 센터링이므로 바꾸면 깨진다. RTL 실패가 만연하면 반응형 점수 1점 감점.
- 밴드: 18~20 Excellent, 14~17 Good, 10~13 Acceptable, 6~9 Poor, 0~5 Critical.
- "Implementation Integrity Verdict"(pass/fail)부터 시작. P3는 적게(긴 꼬리가 중요한 것을 묻는다). 검증 안 된 오탐 보고 금지. 긍정 발견도 기록.

## 7. Craft floor 규칙 전체

`craft-floor.md`는 방향이 정해진 뒤 **모든 UI 편집 직전**(작은 수정 포함)에 로드한다. 계획만 하는 작업에서는 로드하지 않는다. 고정된 브리프나 확정된 세계가 아래를 덮어쓸 수 있지만 "ban"으로 표시된 줄은 예외다. 내 습관은 덮어쓸 자격이 없다.

### 7.1 Verify (빌드 결과에 대한 검사, 한 번의 렌더에서 묶어서)

1. **Contrast**: 본문, 플레이스홀더 4.5:1 이상, 큰 글자 3:1 이상. 색 표면 위 보조 텍스트는 그 색상이나 전경에서 틴트, 회색 금지.
2. **Depth**: 그림자는 오프셋과 부드러운 블러를 가진다. 오프셋 0의 색 후광은 장식이다.
3. **Spacing**: 촘촘한 그룹, 넉넉한 분리, 제목 위 간격 > 제목 아래 간격. 계산된 값을 읽는다.
4. **Type**: 본문 measure 65~75ch, 디스플레이 최대 6rem, 트래킹 하한 -0.04em, 균형 잡힌 제목, 분명한 크기와 굵기 단계. 실제 카피로 모든 브레이크포인트에서 넘침 확인.
5. **Motion**: 흩어진 효과나 모든 섹션 동일 등장이 아니라 작성된 순간 하나. 이미 보이는 기본 상태에서 지수형 ease-out. transform/opacity 너머(blur, backdrop-filter, clip-path, mask, shadow)도 부드러우면 팔레트에 속한다.
6. **States**: hover, disabled, loading, error, empty. 실제 콘텐츠, 작동하는 컨트롤, 반응형 구성, 키보드 포커스.
7. **Browser surfaces**: 직접 그리지 않은 부분도 디자인을 운반한다. 텍스트 선택색, 캐럿, 커스텀 스크롤바, 포커스 링, 밑줄 오프셋, 표 숫자(tabular numerals)를 팔레트로 테마링한다. "조립이 아니라 제작되었다는 가장 싼 신호이자 모델이 가장 확실히 건너뛰는 것."
8. **Copy**: 제품 자신의 언어. 컨트롤은 행동을 이름 짓고, 오류는 문제와 복구를 말한다.
9. **Coverage**: 브리프의 모든 요구가 존재하고 몇 초 안에 찾을 수 있다.

### 7.2 Refuse (카테고리 기본값. 축이 자유로운데 손이 가면 결정하지 않은 것)

페이지 스캐폴드:

- 같은 크기의 아이콘+제목+텍스트 카드를 페이지 구조로. 카드는 게으른 컨테이너이고 중첩 카드는 항상 틀리다.
- 히어로 지표 템플릿(큰 숫자, 작은 라벨, 보조 통계, 강조).
- **제목 위 kicker/eyebrow: 기본값이 아니라 금지(ban).** 어떤 브리프도 되살리지 못한다.
- 섹션 번호(01/02/03): 순서 자체가 독자에게 필요한 정보일 때만.
- 방해도 보호된 포커스도 필요 없는 과업에 모달.

표면 습관:

- 그라디언트 텍스트(강조는 굵기나 크기로).
- 특정 효과가 아닌 장식으로서의 글래스와 블러.
- 카드, 리스트 항목, 콜아웃, 알림에 1px 초과 색 `border-left`/`border-right`.
- 실제 네오브루탈리즘 세계가 아닌 곳의 하드 오프셋 그림자(`box-shadow: 4px 4px 0`). "깊이 체계가 아니라 코스튬."
- 콘텐츠를 대신하는 스파크라인, 진행 링, 부드러운 그림자 둥근 사각형.
- "기술적"이라는 코스튬으로서의 모노스페이스(코드, 데이터, 측정이 아닐 때).
- 자기 세계 페이지의 디스플레이 목소리로 시스템 디스플레이 서체(Impact, Arial Black, 플랫폼 산세리프). "설치된 가장 비슷한 폰트는 대체가 아니라 실패."
- 아이콘 시스템 대신 유니코드 글리프나 이모지. 아이콘은 실제 라이브러리나 직접 그린 SVG, 일관된 획과 굵기.
- 유기적 윤곽을 대신하는 기하학 마스크(원, 다각형, radial-gradient 컷아웃). 실제 이미지에서 알파 매트를 만들거나 컷아웃 자산을 생산한다.
- 카테고리로 정한 라이트/다크. 사용 장면(누가, 어디서, 어떤 주변광)으로 고른다.

Codex 전용 추가 블록(모델별 편향 보정):

- 트래킹은 -0.04em에서 멈춘다. -0.02~-0.03em이 대개 더 낫다.
- 입체감은 한 번만 선언한다. 테두리 아니면 그림자. 넓고 부드러운 그림자 아래 1px 테두리는 "유령 카드". 카드 반경 12~16px, 알약형은 작은 컨트롤용.
- 진짜 일러스트레이션이거나 없거나. 스케치 스타일 SVG 장면, `loose-sketch`/`doodle` 클래스, `feTurbulence` 그레인은 아마추어. 단, 기하(다이어그램, 선 애니메이션, 셰이더)를 하는 SVG는 일급 매체.
- 배경은 표면이다. `repeating-linear-gradient` 줄무늬와 2축 그리드는 실제 캔버스, 지도, 청사진, 측정 도구가 있을 때만.
- 주장과 설정값은 제공된 사실에서. 예시 값은 정직하게 라벨링. 개념을 "~ theater"로 비꼬는 것은 주장이 아니다.

## 8. 타이포, 색, 레이아웃, 모션의 구체 수치

### 타이포 (`typeset.md`, `operate.md`, craft-floor, 탐지기)

- 웹 본문 하한 1rem(16px). 탐지기 기준 본문 12px 미만은 `tiny-text`, 기능 UI 텍스트 11px 미만은 `undersized-ui-text`(법적 소형 문구만 10px).
- 산문 measure 45~75ch(typeset), craft-floor와 DESIGN 템플릿은 65~75ch. 탐지기는 약 80자 초과 줄이 2줄 이상이면 `line-length`.
- 줄 간격: 본문 1.5~1.7 권장, 1.3 미만이면 `tight-leading`. 넓은 줄은 더 많은 행간(measure와 반비례).
- 어두운 바탕의 밝은 글자는 세 축 모두 보정: 행간 조금 더, 트래킹 조금 더, 필요하면 굵기 한 단계 더.
- 트래킹: 하한 -0.04em(권장 -0.02~-0.03em). 본문 0.05em 초과는 `wide-tracking`. 대문자 본문 80자 이상은 `all-caps-body`.
- 위계: 지배적 역할 간 비율이 모든 단계에서 1.25배 미만이면 `flat-type-hierarchy`. Operate 스케일 비율 1.125~1.2, fixed rem.
- 디스플레이 최대 6rem. 72px 이상, 40자 이상 문장형 h1이 뷰포트 높이 28% 이상 또는 면적 25% 이상을 차지하면 `oversized-h1`.
- 줄바꿈: 제목과 짧은 중앙 블록 `text-wrap: balance`, 본문 `text-wrap: pretty`. 수동 줄바꿈은 구(phrase) 사이에서만, 모든 폭에서 확인. 의도된 불균형 줄바꿈은 드물게, 명시적으로.
- 광학 정렬: `text-box: trim-both cap alphabetic`은 flex 컨테이너가 아니라 라벨 요소(`display:block` span)에. 대체 폰트는 `size-adjust`를 캡하이트 비율로.
- 문단 리듬은 문단 간격 또는 첫 줄 들여쓰기 중 하나만(둘 다 쓰면 경계를 이중 표시).
- 두 번째 패밀리는 그것만 할 수 있는 역할이 있을 때만.

### 색 (`colorize.md`, new-work, quieter, distill)

- WCAG AA: 본문 4.5:1, 큰 글자 3:1(탐지기는 24px 또는 굵은 18.67px 이상을 큰 글자로 본다), 컨트롤/아이콘/포커스 표시 3:1.
- 4가지 색 전략: Restrained / Committed(30~60%) / Full palette(3~4 역할) / Drenched. Operate는 Restrained가 바닥.
- 강조색은 주 행동, 현재 선택, 상태 표시에만(Operate). DESIGN 예시 규칙: 주 강조색은 화면의 10% 이하.
- OKLCH 램프: 명도를 바꾸고 흰색과 검정 근처에서 채도를 줄인다. 8단계, 약 15%~95%.
- quieter: 채도 70~85%로. distill: 장식 색 1~2개+중립.
- 색만으로 정보를 전달하지 않는다(텍스트, 모양, 아이콘, 위치 병행).

### 레이아웃 (`layout.md`)

- 스퀸트 테스트: 디테일을 흐려도 주, 보조, 주요 그룹이 순서대로 보이는가.
- 근접성으로 먼저 그룹핑하고 컨테이너나 장식은 그 다음.
- 간격 스케일은 4 기본 단위 권장(8 전용 스케일이 놓치는 중간 단계 제공). 형제 리듬은 `gap`.
- 제목 위 공간 > 아래 공간. 탐지기 `heading-rhythm`은 렌더된 간격이 반대인 경우가 페이지 전반에 반복될 때.
- 컨테이너 내부 텍스트 여백 최소 8px, 이상적으로 12~16px(`cramped-padding`). 본문은 뷰포트 가장자리에서 16px 이상(480px 이하 뷰포트는 12px), 이상적으로 24~32px(`body-text-viewport-edge`).
- 반응형은 구조적으로(재배치, 접기, 리플로우). 같은 컴포넌트가 여러 맥락에 나오면 container query.
- 변형 자체는 목표가 아니다. 반복은 인식을 돕는다.
- 오버레이는 컨테이너를 탈출해야 한다(`overflow: hidden` 안의 절대 위치 드롭다운은 잘림. `<dialog>`, popover API, `position: fixed`, 포털).

### 모션 (`animate.md`)

| 지속 시간 | 용도 |
|---|---|
| 100~150ms | 즉각 피드백 |
| 150~300ms | 일상 상태 변화 (Operate는 150~250ms) |
| 300~500ms | 레이아웃, 오버레이, 뷰 전환 |
| 500~800ms | 의도적으로 작성된 초점 등장 |

- 퇴장은 등장보다 빠르게. 확신 있는 도착에 `cubic-bezier(0.16, 1, 0.3, 1)`. bounce/elastic은 반사적으로 쓰지 않는다(탐지기는 advisory로 표시).
- Hover: 호버된 요소 자체는 움직이지 않고 자식이 움직인다(`.card:hover .card-surface { transform: translateY(-2px) }`). 자기가 움직이면 가장자리 포인터 아래서 빠져나가 깜빡인다. 미리보기 지연은 hover 상태에만 `transition-delay`(떠날 때는 지연 없음).
- 형제 stagger는 목록이 목록으로 나타날 때만, 총 지연 상한. 모든 스크롤 섹션을 stagger 목록으로 재해석하지 않는다.
- 기본 상태에서 콘텐츠가 보여야 한다(스크립트 실패 시 페이지가 숨지 않도록. 탐지기 `content-hidden-at-rest`).
- width, height, top, left, margin 같은 레이아웃 속성은 가볍게 애니메이트하지 않는다. `will-change`는 알려진 애니메이션 동안만.
- reduced-motion: 공간 이동을 줄이되 의미 있는 opacity, 색, 상태 전환은 유지. "모든 모션 끄기"가 아니다. 비필수 루프는 화면 밖이나 숨김 시 정지.

## 9. Slop 감지기 알고리즘

### 9.1 구조

- 규칙 정의 위치: `crates/foundation/src/registry.rs`의 `ANTIPATTERNS`(테스트가 정확히 62개를 단언). 각 행은 `id`, `category`(slop/quality), `scopes`(type, layout), `severity`(없으면 warning, 또는 advisory, error), `name`, `description`, 스킬 섹션 링크.
- 로직은 `crates/core`의 `check_*`/`scan_*` 함수. 같은 규칙 로직이 네이티브 바이너리와 WebAssembly(브라우저 오버레이, 확장 프로그램) 양쪽에서 돈다. LLM이나 API 키가 없는 결정적 엔진이다.
- **4개 엔진** (`RULE_ENGINE_SUPPORT`):
  1. **regex(text)**: 소스 파일(JSX, Vue, Svelte, CSS, CSS-in-JS)을 정규식과 "페이지 분석기"로 스캔. 렌더 없이 잡을 수 있는 것: 금지 폰트 이름, 그라디언트 텍스트 선언, bounce 키워드, 간격 값 분포, 카피 패턴.
  2. **static-html**: 자체 HTML 파서+CSS 캐스케이드(셀렉터 매칭, shorthand 전개, 기본값)로 정적 DOM을 만들고 요소별, 페이지별 규칙 실행.
  3. **browser**: Chrome을 CDP로 붙여 렌더된 DOM의 계산 스타일과 박스 기하를 읽는다(element, page, layout 패스). 넘침, 가림, 첫 뷰포트, 줄바꿈, 리빌 후 숨김 같은 것은 여기서만 가능하다.
  4. **visual**: 스크린샷 픽셀을 읽어 실제 대비를 판정(그라디언트, 이미지 위 텍스트).
- **2단 티어** (훅): 편집마다 즉시 보고하는 immediate tier는 12개(`broken-image`, `text-overflow`, `body-text-viewport-edge`, `low-contrast`, `gray-on-color`, `tiny-text`, `gradient-text`, `dark-glow`, 그리고 `design-system-font/color/radius/font-size`). 기준은 "기계적이고 모호하지 않으며 편집 지점에서 고치기 쉬운 것, 그리고 방치하면 복리로 쌓이는 시스템 드리프트". 카피 리듬, 팔레트와 타이포 취향, 레이아웃 리듬은 Stop 이벤트의 deep pass에서 세션 동안 건드린 모든 UI 파일을 대상으로 한 번만, 중복 제거해서 보고한다.
- **advisory 15개**: 측정은 맞지만 거의 해롭지 않거나 의도일 수 있는 것(코퍼스 리뷰에서 정밀도가 낮게 나온 규칙을 강등). 실패 카운트에서 빠지고 편집 중 방해하지 않는다. error 2개(`script-error`, `content-hidden-at-rest`)는 "다른 것을 판단하기 전에 고쳐라".
- **오탐 억제 설계가 핵심**: 거의 모든 규칙이 예외 목록을 가진다. 예: 측면 테두리는 blockquote, nav, a, input, li, td 등 "안전 태그" 제외(단 카드형 label은 포함). 중첩 카드는 팝오버, 절대/고정 위치, 칩, 폼 필드 박스, 미디어 프레임, 다이얼로그, figure, 출력 블록 제외, 그려진 제품 목업 안이면 advisory. 브랜드 폰트는 자기 도메인에서 허용(Roboto는 google.com, Geist는 vercel.com, Mona Sans는 github.com). justify는 CJK, 태국어, 아랍어 제외. 인라인 `data-impeccable-ignore="rule-id"`와 설정 파일의 `ignoreRules/ignoreFiles/ignoreValues`로 의도적 사용을 면제.
- **DESIGN.md 연동**: `design-system-*` 4개 규칙은 DESIGN.md 프론트매터와 사이드카 tonal ramp를 읽어 문서 밖의 폰트, 색, 반경, 글자 크기를 드리프트로 잡는다. 램프에 8px을 추가해도 `undersized-ui-text`는 면제되지 않는다(토큰 세탁 방지).
- 확장: 다운스트림 crate가 네임스페이스 id(`mypack/rule`)로 rule pack을 추가할 수 있고, 내장 id를 가리면 panic.

### 9.2 전체 규칙 표

엔진 열은 각 rule id가 어느 소스 파일에 등장하는지 grep한 결과에 기반한 추정이다(text=regex, static=static-html, browser=CDP 렌더, visual=픽셀). 임계값은 소스 상수에서 읽었다.

**A. Slop: 테두리, 카드, 입체감** (`hard-offset-shadow`만 category가 quality)

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `side-tab` | 카드 한쪽의 두꺼운 색 테두리 | 한 변 테두리. 둥근 요소면 폭과 무관, 각진 요소면 3px 이상. 안전 태그 제외 | text, browser |
| `border-accent-on-rounded` | 둥근 카드의 두꺼운 강조 테두리 | 반경과 강조 테두리 충돌 [세부 임계 미확인] | text, browser |
| `nested-cards` | 카드 안 카드 | 테두리나 그림자가 보이는 50x30px 이상, 텍스트 10자 이상 박스가 카드형 조상(페이지 프레임 제외) 안에 있음. 다수 예외 | static, browser |
| `gpt-thin-border-wide-shadow` (advisory) | 한 줄의 모든 카드가 헤어라인 테두리+넓은 그림자 | 같은 크기(25% 허용) 카드 3개 이상, 블러 32px 이상 | browser |
| `dark-glow` | 색 글로우 그림자 | 오프셋 0 유채색 후광(어느 배경이든) 또는 어두운 배경의 유채색 블러 그림자. 강도 3px 이상 등 | text, browser |
| `hard-offset-shadow` (quality, advisory) | 블러 없는 하드 오프셋 그림자 | blur 0, spread 0 이상, 오프셋 최대값 4px 이상, 알파 0.1 초과, inset 아님. 네오브루탈 의도 확인용 | static, browser |

**B. Slop: 색과 배경**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `gradient-text` | 그라디언트 글자 | `background-clip:text`+그라디언트. 한 색 그라디언트(채널 차 12 미만)는 단색으로 간주해 제외 | text, browser |
| `ai-color-palette` | 보라/바이올렛 그라디언트, 어두운 바탕의 시안 | 보라 hue 260~310, 시안 170~197(채도 0.4 이상). 해당 hue 그라디언트는 단독으로 판정, 평면 네온 잉크는 두 번째 tell hue가 있을 때. 고정 hex 목록(7c3aed, 8b5cf6, a855f7, 6366f1, 667eea 등) | text, browser |
| `cream-palette` | 크림/베이지 페이지 바탕 | 화면의 95% 이상을 덮는 바탕색이 크림 범위, 또는 Tailwind 크림 클래스 | static, browser |
| `radial-halo` | 어두운 페이지의 유채색 radial 후광 | 중심 고채도에서 투명으로 가는 radial-gradient | text, browser |
| `radial-spotlight-glow` | 히어로 뒤 스포트라이트 구름 | 강조색 radial, 유효 알파 0.14 이상, 표면 대비 1.30 이상 | browser |
| `repeating-stripes-gradient` (advisory) | 장식 줄무늬 | `repeating-*-gradient` 표면 장식 | browser |
| `codex-grid-background` (advisory) | 장식 그리드 배경 | 고정 px 셀로 타일된 헤어라인 linear-gradient 2축 레이어 | text, browser |

**C. Slop: 타이포와 라벨**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `overused-font` | 과용 폰트 | 목록: inter, roboto, open sans, lato, montserrat, arial, helvetica, fraunces, instrument sans/serif, geist(sans/mono), mona sans, plus jakarta sans, space grotesk, recoleta. 렌더 시 글자 점유율 5% 이상. 공백/하이픈 무시 매칭 | text, static, browser |
| `flat-type-hierarchy` | 평평한 크기 위계 | 역할(h1~h6, p, li, td 등) 3개 이상에서 인접 단계 비율이 모두 1.25 미만 | browser |
| `italic-serif-display` | 이탤릭 세리프 히어로 헤드라인 | 알려진 세리프 목록(Fraunces, Recoleta, Playfair, Newsreader 등 30여 개)+이탤릭+디스플레이 크기 | browser |
| `hero-eyebrow-chip` | 히어로 위 작은 대문자 라벨/알약 칩 | 트래킹된 대문자 소형 라벨이 큰 헤드라인 바로 위 | 공유 체크 |
| `kicker-above-heading` | 모든 제목 위 kicker | 기본 14px 이하이고 제목 크기의 0.45배 이하(최대 16px), 40자 이하 트래킹 라벨이 독립 블록으로 제목 바로 위. 반복 여부와 무관하게 금지 | 공유 체크 |
| `numbered-section-labels` (advisory) | 섹션마다 작은 번호 라벨 | 13px 이하 숫자 라벨이 섹션 제목 옆에 반복 | 공유 체크 |
| `oversized-h1` | 디스플레이 크기의 긴 문장 헤드라인 | 72px 이상, 40자 이상, 뷰포트 높이 28% 이상 또는 면적 25% 이상 | 공유 체크 |
| `extreme-negative-tracking` | 짓눌린 자간 | -0.07em 이하(40px 이상 디스플레이는 -0.09em 이하) | static, browser |
| `icon-tile-stack` | 제목 위 둥근 사각형 아이콘 타일 | 배경 알파 0.05 이상의 작은 둥근 컨테이너가 제목 위에 쌓임 | browser |

**D. Slop: 모션과 일러스트**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `bounce-easing` (advisory) | bounce/elastic 이징 | 이름/키프레임 단어 bounce, elastic, wobble, jiggle, spring. 실제로는 pulse만 하는 키프레임은 구분 | text, browser |
| `pulsing-dot` | 장식용 맥동 상태 점 | 종횡비 1.5 이하 작은 점에 pulse 애니메이션 | browser |
| `blinking-cursor` (advisory) | 히어로의 가짜 깜빡이는 커서 | 첫 뷰포트(1200px) 안, 입력 필드가 아닌 곳 | browser |
| `marquee` | 자동 스크롤 마키 | `<marquee>` 또는 무한 translate 애니메이션 트랙 | text, browser |
| `shape-assembled-illustration` (advisory) | 원시 도형 더미로 만든 큰 인라인 SVG | 원시 도형 비율 25% 이상, 막대 차트형(원시 400개 이하)은 제외 | 공유 체크 |

**E. Slop: 카피와 간격**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `em-dash-overuse` (advisory) | em dash 포화 | 8개 이상이면서 500자당 1개 이상 밀도(엔티티 포함, 하이픈 3개 이상 연속은 괘선으로 제외) | text |
| `marketing-buzzword` | 마케팅 상투어 | 고정 구문 목록(streamline your, empower your, supercharge your, unleash the power, best-in-class, world-class, enterprise-grade, next-generation, cutting-edge, revolutionize, game-changer, future-proof, seamless experience, drive growth, harness the power 등 29개) | text |
| `aphoristic-cadence` | 경구형 리듬 | 정규식 "Not a X. Y." 및 "X. No/Just y." 구문이 3회 이상 | text |
| `theater-slop-phrase` (advisory) | "~ theater" 비꼼 | "theater" 앞 단어가 경멸적 수식어일 때만("compliance theater"는 잡고 "Southern Theater Command"는 통과) | 공유 체크 |
| `monotonous-spacing` | 단조로운 간격 | padding/margin/gap(px, rem*16, Tailwind*4) 중 0 초과 200 미만 값을 4px 단위로 반올림. 10개 이상일 때 최빈값이 60% 초과이고 고유값 3개 이하면 보고. 최빈값 0은 리셋으로 보고 제외 | text |

**F. Quality: 렌더 결함과 가시성**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `script-error` (error) | 로드 중 미처리 스크립트 오류 | 페이지 로드 시 예외/파싱 실패 수집 | browser |
| `content-hidden-at-rest` (error) | 리빌 실패로 숨은 콘텐츠 | 리빌 핸들러 실행 후 전체 200자 이상, 숨김 150자 이상, 숨김 비율 30% 초과 | browser |
| `broken-image` | 빈/누락/플레이스홀더 src | 마크업 패턴 | text, static |
| `organic-clip-path` | 코드로 흉내 낸 유기적 윤곽 | `clip-path: polygon` 꼭짓점 10개 이상 또는 곡선 `path()`. 기하 용도(모서리 컷, 사선, 육각형)는 허용 | browser |
| `buried-raster` | 워시나 투명도 아래 묻힌 래스터 | 배경 이미지 위 그라디언트 정지점이 모두 알파 0.9 이상, 또는 거의 0 opacity 래스터 | static, browser |
| `text-overflow` | 해로운 넘침 | 클리핑 조상에 잘림, 다른 박스와 충돌, 뷰포트 가장자리 도달 | browser |
| `text-occlusion` | 겹친 요소에 가려진 글자 | 불투명 박스나 다른 텍스트 런이 위에 그려짐 | browser |
| `edge-flush-cards` | 스크롤러 가장자리에 붙은 카드 | 한쪽만 거터(12~48px)가 있고 반대쪽이 붙어 잘림 | browser |
| `first-viewport-column-overflow` | 첫 화면 한 칼럼만 길게 | 다단 오프닝에서 한 칼럼이 폴드 훨씬 아래로, 형제는 한 화면 | browser |
| `clipped-overflow-container` (advisory) | overflow 클립 안의 절대 위치 자식 | 툴팁, 메뉴가 잘릴 구조 | static, browser |
| `repeated-container-text` | 한 컨테이너 안 같은 문구 반복 | 구조적으로 다른 위치에 같은 리터럴 3회 이상 | static |

**G. Quality: 대비와 가독성**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `low-contrast` | WCAG AA 미달 | 본문 4.5:1, 큰 글자 3:1. 픽셀 판독으로 그라디언트/이미지 배경 처리 | static, browser, visual |
| `gray-on-color` | 색 배경 위 회색 글자 | 배경 채널 편차 40 이상인 유채색 위 무채색 텍스트 | text, browser |
| `tiny-text` | 12px 미만 본문 | 계산 크기 | static, browser |
| `undersized-ui-text` | 11px 미만 기능 텍스트 | 링크, 버튼, 내비, 라벨, 표, 메타. 법적 소형 문구 10px. sup/sub, sr-only, 코드 제외 | static, browser |
| `tight-leading` | 1.3배 미만 행간 | 24px 이상 디스플레이, 3줄 이하 20px 리드 텍스트(1.15), 대문자 라벨(1.0) 등 예외 | static, browser |
| `wide-tracking` | 본문 0.05em 초과 자간 | 짧은 대문자 라벨은 제외 | static, browser |
| `all-caps-body` | 긴 대문자 본문 | 요소 자체 텍스트 80자 이상. 버튼, 내비, kicker는 관례로 제외 | static, browser |
| `justified-text` | 좁은 칼럼 양쪽 정렬 | 줄당 45자 미만, 하이픈 없음. CJK, 태국어, 아랍어 제외 | static, browser |
| `straggler` (advisory) | 문단 마지막 줄 한 단어 | 렌더된 줄 상자 | browser |
| `unbalanced-heading` (advisory) | 마지막 줄이 매우 짧은 제목 | 렌더된 줄 상자 | browser |

**H. Quality: 레이아웃과 구조**

| id | 감지 대상 | 방법과 임계값 | 엔진 |
|---|---|---|---|
| `line-length` | 너무 긴 줄 | 렌더된 줄 중 약 80자 초과가 2줄 이상 | browser |
| `cramped-padding` | 비좁은 내부 여백 | 테두리, 아웃라인, 배경이 있는 컨테이너에서 텍스트까지 8px 미만(글자 크기 대비) | static, browser |
| `body-text-viewport-edge` | 뷰포트 가장자리에 붙은 본문 | 16px 미만(480px 이하 뷰포트는 12px). 넘침은 페이지당 1회 가장 넓은 요소로 보고 | browser |
| `skipped-heading` | 제목 레벨 건너뜀 | h1 다음 h3 등 | static, browser |
| `heading-rhythm` | 이전 블록에 붙은 제목 | 제목 위 간격 ≤ 아래 간격이 페이지 전반에서 반복 [최소 위반 수 2로 추정] | browser |

**I. Quality: 디자인 시스템 드리프트 (DESIGN.md 필요)**

| id | 감지 대상 | 엔진 |
|---|---|---|
| `design-system-font` | DESIGN.md typography에 없는 폰트 | browser + design_system 스캔 |
| `design-system-color` (advisory) | 팔레트와 사이드카 램프 밖 리터럴 색 | 동일 |
| `design-system-radius` (advisory) | rounded 스케일 밖 반경 | 동일 |
| `design-system-font-size` | 타입 램프 밖 리터럴 글자 크기 | 동일 |

합계: A 6 + B 7 + C 9 + D 5 + E 5 + F 11 + G 10 + H 5 + I 4 = 62.

## 10. 서브에이전트 역할 분담

모든 서브에이전트는 **신선한 맥락**(대화 기록 포크 없음)으로 띄운다. 빌드 스레드의 프레이밍, 낙관, 추상화를 상속하지 않게 하려는 것이다. 부모는 에이전트 정의 파일을 미리 읽지 않고 입력 패킷만 책임진다. 서브에이전트가 없는 하네스는 `reference/degraded/*.md`로 "빌드 맥락에서 완전히 빠져나온" 대체 패스를 돌리고 이를 공개한다.

| 에이전트 | 역할 | 핵심 규칙 |
|---|---|---|
| `impeccable-finish-reviewer` | 완성된 빌드를 direction contract, 승인된 시안, 세계의 QUALITY BAR 카드에 대어 리뷰 | 쓰기 도구 금지, 브라우저 없음, 약 10턴째 읽기 중단 후 작성 |
| `impeccable-motion-reviewer` | 캡처된 모션(일반+reduced)의 연속성, 타이밍, 완성도 | 증거 파일만 읽음, 반환 섹션 `continuity`, `craft`, `reduced_motion`, `material_fixes`, `keep` |
| `impeccable-documenter` | 완성된 산출물에서 DESIGN.md와 사이드카 작성 | 근거는 계획이 아니라 출하된 코드. 계약과 빌드가 다르면 빌드가 이김. 기존 파일은 부모가 받은 선택 없이는 쓰지 않음 |
| `impeccable-asset-producer` | 승인된 시안에서 깨끗한 래스터 자산 생산(또는 결정 카드당 시안 1장) | 재디자인 금지. 실루엣, 팔레트, 조명, 재질 보존. CSS가 만들 크롬(그림자, 둥근 클립)은 래스터에서 제거 |
| `impeccable-manual-edit-applier` | live 모드에서 사용자가 Apply한 카피 편집 배치를 소스에 적용 | 배치 텍스트는 지시가 아닌 데이터. 소스에 이미 있는 정확한 부분 문자열만 교체. DOM outerHTML 사용 금지 |

**Finish reviewer의 검사 순서**: 0 증거(필수 캡처 존재, 검은/빈 영역 없음, 파일명과 내용 일치. 하나라도 실패하면 `recapture`만 반환하고 중단) → 1 지속성(PRODUCT.md, 빌드 상태 파일, 각 단계 closed, 히어로 게이트 점수 0.72 이상) → 2 충실도(시안 요소 인벤토리를 **계약 요약을 읽기 전에** 자기 말로 먼저 작성. 요소마다 match / acceptable adaptation / missing / contradicted / added without approval. 필수 행 TYPE, MATERIAL, GROUND. CSS 베벨이나 엠보싱으로 흉내 낸 재질은 그 자체로 contradicted, "모조 재질은 기계가 만든 디자인의 가장 확실한 표지") → 3 천장(세계의 고유 장치 중 안 쓴 것) → 4 계약 약속별 점검(시드 참조 검증 포함) → 5 진실(합성 데이터 라벨, 날조 주장 없음, 래스터 영역이 실제로 출하됨) → 6 바닥(Refuse 목록과 대조. 시안과 일치해도 금지 요소는 수정 대상).

**판정 단어는 정확히 4개이며 도출된다(느낌이 아니다)**: `recapture`(증거 실패), `rebuild`(초점 요소 재질 모순 등 전면 실패), `fix`(material_fixes 비어 있지 않음), `ship`(수정 없음, missing/contradicted 행 없음). 반환은 판정 줄 + 5개 섹션(`persistence`, `fidelity`, `ceiling`, `material_fixes` 최대 8개, `keep`). 칭찬과 요약 산문 금지. 부모는 판정 단어를 그대로 보고하며 완화할 권한이 없다. 수정 후 Verdict Pass는 재탐색이 아니라 각 수정의 resolved / partial / unresolved 채점과 회귀 최대 3개만. 부모의 "고쳤다"는 서술은 증거가 아니다. 무인 실행은 2라운드에서 끝나고, 한 라운드가 아무것도 해결하지 못하면 즉시 멈춘다.

## 11. 설계 판단과 이유

- **플레이북 단위 명령**: 모호한 요청은 평균으로 수렴하므로 동작 하나에 맞춘 지시문을 로드해 특정 대상에 겨눈다. 좁은 대상이 더 좋은 결과를 낸다("한 섹션을 자세히 보는 것이 페이지 전체를 훑는 것보다 낫다").
- **결정적 탐지기와 LLM 판단의 분리와 순서**: 탐지기는 오탐이 적은 "바닥"이고 좋은 디자인의 증명이 아니다("깨끗한 스캔은 바닥이지 증거가 아니다"). 결정적 출력도 앵커링을 일으키므로 critique, typeset, layout은 설계 판단을 먼저 하고 탐지 결과를 나중에 합친다.
- **무작위 배정(concept-seed)**: 모델은 같은 카테고리에서 같은 방향으로 수렴한다. 주사위로 방향을 배정하고 내 1순위는 PICK 카드 한 장으로만 보여, 순위 고착을 깨면서도 사용자에게 실제 선택을 준다. 후보 목록을 여러 장 늘어놓지 않는 이유는 "가장 안전한 카드를 고르게 유도"하기 때문이다. 친숙한 선택(standing exit)은 언제나 열려 있으나 에이전트가 권하지 않는다.
- **측정 계약으로서의 시안**: 모델은 재현 성공을 과신하므로 comp-led 빌드는 디스크 상태 머신(comps, spec, hero gate, ...)으로 돌고, 게이트가 화면을 시안과 수치로 비교한다(`comp-diff`의 영역별 점수, `font-match`의 글리프 지문 거리). 이 경로는 프런티어급 모델 작업이라고 명시하고 작은 모델은 code-led를 택하라고 한다.
- **신선한 리뷰어**: 빌드 스레드는 "주의의 중력"에 갇힌다. 리뷰어는 맥락을 상속하지 않고 증거 파일만 본다. 유효하지 않은 증거 위의 판정은 아무것도 구속하지 않는다.
- **빌드 후 문서화**: 사전 규칙집은 현실과 싸운다. DESIGN.md는 출하된 것에서 쓴다.
- **advisory 강등의 근거는 측정**: 코퍼스 리뷰에서 정밀도와 해악을 측정해 규칙을 advisory로 내리거나 은퇴시킨다(예: `clipped-overflow-container`는 패턴 정밀도 0.08, 해악 0.04로 판정되어 advisory, `image-hover-transform`, `layout-transition`은 은퇴).
- **모델별 편향 블록**: Claude에는 크림/세리프 편향 경고, Codex에는 유령 카드, 과한 반경, 스케치 SVG, 줄무늬/그리드 배경 경고를 별도로 넣는다. 범용 규칙과 모델 고유 버릇을 분리한 것이다.
- **질문을 아끼되 확실히 묻는다**: 라운드당 2~3문항, 저장소에서 답할 수 있는 것은 묻지 않는다. 대신 "응답자가 있는지"는 판단이 아니라 기계적 테스트(실제 질문 도구 호출)로 확인한다.
- **조용한 실패 금지**: degraded 배너, 대체 리뷰 공개, 판정 단어 그대로 보고, "검증했다"는 증거 없는 '예' 금지. 시스템 전반에 정직성 장치가 깔려 있다.

## 12. 내 작업에 가져올 점

1. **모드 먼저**: 작업 시작 시 이 표면이 Persuade / Operate / Read / Experience 중 무엇인지 한 줄로 정하면 야심의 크기와 색, 타입, 모션 수치가 자동으로 따라온다.
2. **rut 명시**: "이 카테고리가 늘 내는 페이지"와 "그 뻔한 반대"를 먼저 적고 후보에서 뺀다.
3. **제품 사실과 시각 결정과 표면 전략을 분리 저장**한다(PRODUCT / DESIGN / 표면 브리프).
4. **판단 후 탐지, 리뷰는 신선한 맥락으로**: 체크리스트 결과를 보기 전에 정성 판단을 고정한다.
5. **판정 어휘를 고정**한다(recapture / rebuild / fix / ship). 느낌 대신 조건으로 도출.
6. **Named Rule 형식**으로 디자인 규칙을 쓴다. 불릿보다 에이전트에 잘 붙는다.

재사용 가능한 압축 프롬프트:

```text
You are a design director building production UI. Before any UI edit:

1) MODE: Name the surface mode in one line.
   Persuade (visitor decides/acts) | Operate (completes a task) |
   Read (understands) | Experience (inside the work).
   Persuade/Experience: bold, committed point of view.
   Operate/Read: precision and restraint; the world lends only type,
   palette, density, and ONE signature move; never layout, nav, or controls.

2) RUT: Write the page this category always ships and its predictable
   opposite. Exclude both. If someone could guess the aesthetic from the
   category alone, rework. Avoid defaults: cream+serif+terracotta;
   near-black+one neon+glow; editorial hairlines+italic serif+tracked mono
   labels; flat ink+black boxes+hard offset shadows. Fonts needing a unique
   reason: Inter (as display), Fraunces, Playfair, Cormorant, Lora,
   Space Grotesk, DM Sans, Plus Jakarta Sans, Instrument Sans, Geist.

3) COLOR STRATEGY first: Restrained | Committed (one hue 30-60%) |
   Full palette (3-4 roles) | Drenched. Light vs dark from one sentence of
   physical scene (who, where, what light), never by category.

4) CONTRACT (~150 words): THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM.
   If a block reads like a mood, the direction is not decided.

5) FLOOR (verify on the render, batched):
   contrast >=4.5:1 body, >=3:1 large; tinted secondary text on color,
   never gray; shadows have offset+blur, no zero-offset colored halos;
   more space above a heading than below; body 65-75ch, line-height
   1.5-1.7 (never <1.3), display <=6rem, tracking >= -0.04em, body >=16px,
   UI text >=11px; text-wrap: balance on headings, pretty on body;
   motion: one authored moment, ease-out cubic-bezier(0.16,1,0.3,1),
   100-150ms feedback, 150-300ms state, 300-500ms view, exit faster,
   content visible by default, reduced-motion keeps meaningful feedback;
   every control has hover/focus/active/disabled/loading/error;
   theme selection, caret, scrollbar, focus ring, tabular numerals.

6) REFUSE: eyebrow/kicker above headings (banned), gradient text,
   colored border-left/right >1px on cards, nested cards, identical
   icon+heading+text card grids, hero-metric template, 01/02/03 section
   numbers, decorative glass/blur, glyph or emoji icons, mono as
   "technical" costume, system display faces, geometric masks faking
   organic edges, hairline border + wide soft shadow, decorative stripes
   or grid backgrounds, marketing buzzwords, "X. No Y." cadence.

7) REVIEW: judge design specificity before reading any lint output.
   Score Nielsen 10 heuristics 0-4 (most real UIs: 20-32/40), tag issues
   P0 blocking / P1 major / P2 minor / P3 polish ("would a user contact
   support?" => at least P1). End with exactly one verdict:
   recapture | rebuild | fix | ship. Ship only with zero material fixes.
```
