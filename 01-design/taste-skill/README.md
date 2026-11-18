# Taste Skill: 핵심 원리 정리

> 원본: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) | 정리일: 2026-11-18 | 분석 기준: tasteskill 2.5.1 (SKILL.md), commit `f6b7657` (2026-11-07)

이 문서는 설치나 사용법이 아니라 skill의 사고방식을 정리한 것이다. `skills/taste-skill/SKILL.md`, `references/*.md`, `scripts/start.mjs`, `assets/layout/deal.mjs`, `scripts/moments.mjs`, `scripts/effects.mjs`(+ `assets/effects/pick.js`), `scripts/gate.mjs`, `scripts/consistency.mjs`, `scripts/copy-lint.mjs`, `library/*.json`의 실제 코드를 읽고 정리했다.

## 1. 해결하려는 문제

- LLM이 만든 회사 웹사이트는 서로 닮는다. 같은 보라색 그라디언트, 같은 Inter 폰트, 같은 "hero + 3 features + CTA" 구조, "seamless", "unlock" 같은 단어가 반복된다.
- 원인은 두 가지로 본다. (1) 모델은 "취향"으로 고를 때 항상 학습 분포의 최빈값으로 수렴한다. (2) 모델은 자기가 만든 페이지를 눈으로 검증하지 못하고 "완료"를 선언한다.
- 목표 기준은 figma.com, x.ai 수준의 "좋은 회사가 실제로 출시할 사이트"다. 무엇을 파는지 평이하게 말하고, 모든 화면에 실물을 보여주고, 템플릿도 예술 작품도 아닌 "이 고객을 위해 만든" 느낌이어야 한다.
- 해법은 (1) 선택을 무작위 deal과 history로 바꾸고, (2) 업종(kind)이 허용 범위를 결정하게 하고, (3) 실제 브라우저에서 픽셀과 DOM을 재는 checker와, 통과 전에는 종료를 막는 finish gate로 강제하는 것이다.

## 2. 핵심 철학

1. **Deal, never choose by taste.** 팔레트, 폰트 페어링, hero, moment, effect, nav, footer, close, rhythm, 버튼 모양, 마크까지 전부 스크립트가 뽑는다. 모델은 첫 번째 결과를 받는다. 다음 후보는 고객 로고나 사진과 충돌할 때만 쓰고, 이유를 plan 2번째 줄에 적는다.
2. **업종이 모든 것을 결정한다.** plan 첫 줄은 kind이고, 페이지에 `<html data-type>`, `<meta name="page-type">`, `<meta name="site-kind">`(place는 `page-kind=place` 추가)로 선언한다. 모든 dealer와 checker가 이 값을 읽는다.
3. **높이와 패딩으로 만드는 리듬.** 모든 section은 정확히 1 또는 2 screen이다. 327개 사이트 연구(1440x900, 390x844) 근거: 회사 사이트 78%에서 hero가 첫 화면에 혼자 있고, section이 0.95~1.1 screen일 때 단독으로 보일 확률이 0.80, 간격 220px 이상일 때 0.82였다.
4. **보여주기, 설명하지 않기.** 실제 사진, 실제 제품 UI(live HTML), 실제 아이콘. 그림 아래 캡션 금지. 발명된 리뷰/수치/고객 금지.
5. **기계적 검증이 판단을 대신한다.** 리뷰어가 눈으로 표시하는 결함을 headless Chrome에서 수치로 잰다. 체크를 속이는 코드(webdriver 감지 등)는 waiver 불가 FAIL이다.
6. **게이트는 강제하되 가두지 않는다.** 라운드 3회, block 횟수 상한, idle 24시간 등 탈출구를 코드로 보장한다.

## 3. 업종 분류 알고리즘과 업종별 허용 규칙

### 3.1 분류표 (SKILL.md section 1)

| Brief | page type | site-kind | kind |
|---|---|---|---|
| App, SaaS, AI, developer tool, fintech, 자사 소프트웨어를 파는 studio | software | software | software |
| 게임, 게임을 출시하는 studio | software | gaming | gaming |
| 하드웨어, tech device(drone, robot arm, keyboard) | product | tech | tech |
| 그 외 물리 제품/브랜드(의자, 자전거, 원두 온라인 판매) | product | other | product |
| 사람을 고용함: clinic, law firm, agency, creative studio, trade | service | other | service |
| 사람이 찾아옴: cafe, bar, bakery, restaurant, guesthouse, shop, florist, gym | place | other | place |

- 경계 규칙: 문을 열거나 가르치는 maker(도예 studio, 웹샵 있는 bakery)는 **place**이고 웹샵은 goods section이 된다. 문 앞에서 아무 일도 없을 때만 product다.
- "tech"는 software, gaming, tech를 뜻하고 나머지는 "other"다.

### 3.2 trade 단어 매칭 (start.mjs `TRADE_WORDS`)

- 19개 trade: cafe, bakery, restaurant, hotel, wellness, studio, workshop, wedding, retail, law, clinic, agency, saas, devtool, fintech, ai, game, hardware, consumer-product.
- brief 단어를 정규식 목록 순서대로 검사하고 **처음 맞는 규칙이 이긴다**. 순서 자체가 설계다. 예: wedding이 bakery보다 먼저, `brand|maker` 단어가 restaurant보다 먼저, estate/travel/insurance agent는 AI보다 먼저 agency로 잡는다("agent"가 AI agent로 오인되는 것을 막는 주석이 있다). kitchen은 `fitting|design|install|renovat...`가 뒤따르지 않을 때만 restaurant다.
- `--page`가 없으면 `TRADE_PAGE`로 kind를 추론한다: cafe/bakery/restaurant/hotel/wellness/workshop/retail -> place, studio/wedding/law/clinic/agency -> service, saas/devtool/fintech/ai -> software, game -> gaming, hardware -> tech, consumer-product -> product.
- moments.mjs에도 별도 alias 표가 있다(`technical-product -> software`, `studio -> service` 등). "other"는 세 kind라서 거부하고 어느 것인지 말하게 한다.

### 3.3 kind별 허용 범위 (SKILL.md section 3, effects-usage.md)

| 항목 | software, gaming | hardware(tech) | product, service | place |
|---|---|---|---|---|
| Hero | dealt | dealt | dealt(product는 product/photo/film만) | 고정 place hero |
| 사진 | 사람, 고객, 게임 아트 | 주도 | 주도 | 주도, 12~20장 |
| 실제 아이콘 | yes | yes | 실제 쓰는 도구만 | 없음 |
| UI fragment card | 주도(gaming 제외) | 자사 앱 | 고객이 운영하는 앱 | 없음 |
| Diagram card | 0~2, pulsing | 0~2, pulsing | 0~1, still | 없음 |
| CSS ground | 0~2 dealt | 0~2 dealt | flat token | flat token |
| Shader effect | 1개 | 1개 | 금지 | 금지 |
| Moment | 1~2 | 1~2 | 1~2(photo/type-led) | 1~2(photo/type-led) |
| Big scene | 0~1 | 0~1 | 금지 | 금지 |

- other에서 금지되는 것: canvas/WebGL, autoplay video, 모든 CSS gradient, SVG pattern, `backdrop-filter`, `filter`, `mix-blend-mode`, glass, grain, halftone, dither, `[data-fx]`, scroll/animation 라이브러리, custom cursor. 예외는 고객이 3D를 요청한 product render 하나(live context 최대 1).
- "Subject before effect" 원칙: 테스트에서 robot arm을 silk shader와 주문 폼으로 보여준 페이지, 이름 없는 게임을 추상 effect로 보여준 페이지가 실물을 보여준 페이지에 졌다. effect는 제품, 기기, 게임 세계가 있어야 할 자리에 절대 오지 않는다.
- place 고유 규칙: 사진 개수가 길이를 정한다(full 12~20, compact 8~12, 8 미만은 3-screen short page). 한 화면에 main action 하나, 목록 텍스트 16px, square 사진, 버튼 radius 2px.

## 4. Deal 알고리즘

모든 dealer는 같은 구조다: **(필터로 후보 풀 생성) -> (history로 최근 것 감점 또는 제외) -> (가중 무작위) -> (history에 기록)**.

### 4.1 Palette (start.mjs `deal`)

데이터 `library/palettes.json`은 64개 배열이다. 각 항목 필드:

```text
{ id, name, tags[], trades[], bg, surface, ink, muted, accent, accentInk,
  fields:[{bg, ink}], note, seenIn[] }
tags: light-neutral 18, earth 13, mono-accent 11, dark-neutral 10, two-tone 9,
      flat-loud 9, single-field 8, photographic-neutral 7, pastel-fields 6
```

`seenIn`은 이 배색을 관찰한 레퍼런스 사이트 id다(복사 금지, 관찰 근거만).

```text
palettes = all.filter(paletteOk)
  paletteOk: chroma(bg) < 0.045               # 조용한 바탕
             and not violet(accent)           # LCH C > 0.05 and 275 < h < 330
             and 'flat-loud' not in tags
if kind not tech:  drop dark bg               # 어두운 페이지는 tech 전용
if --dark/--light: filter by isDark(bg)
if place:          keep placeGround(bg)       # 밝음: Lab L >= 0.80, RGB max-min <= 0.12
avoid = shared_recent[trade or kind].last(6) + history.palettes.last(12)
fit   = palettes where trade in p.trades
dealt = drawFresh(fit, 3, avoid)
if len(dealt) < 3: dealt += drawFresh(palettes - fit, 3 - len, avoid)

drawFresh(list, n, recent):
  fresh = shuffle(list not in recent)
  stale = (list in recent) sorted by lastIndexOf(id) ascending   # 가장 오래전 것 먼저
  return (fresh + stale)[:n]
```

- `shared_recent`는 환경변수 `TASTE_SKILL_RECENT`로 지정한 파일에만 기록한다(opt-in). 폴더가 달라도 "다음 카페"가 다른 팔레트를 받게 하려는 장치다. 기본값은 프로젝트 밖에 아무것도 쓰지 않는다.
- 출력에 plan 2번째 줄용 문장 템플릿을 준다: ground 단어(`warm off-white`, `stone`, `putty`, `near-black`)와 accent hue 단어(`ochre`, `oxblood`, `teal`...)를 LCH로 계산해서 "이 trade의 무엇(방, 재료, 상품)에 답하는지"를 쓰게 한다. brief에 없는 사실은 쓰지 않는다.

**토큰 파생 규칙** (`tokens(p)`): 팔레트 6색에서 16개 CSS 변수를 결정론적으로 만든다.

| 토큰 | 규칙 |
|---|---|
| surface | 없으면 mix(bg, ink, 0.05) |
| muted | bg와 surface 모두에 4.6:1 이상이 될 때까지 ink 쪽으로 8%씩 섞음(최대 40회) |
| accentInk | accent 위 4.5:1 이상이면 지정값, 아니면 white/#111/ink/bg 중 읽히는 것 |
| invBg | 밝은 페이지면 Lab L < 0.4인 field, 어두운 페이지면 밝은 field, 없으면 ink |
| invInk | invBg와 bg 대비 7:1 이상이면 bg, 아니면 white/#111 중 읽히는 것 |
| invAccent | accent가 invBg에 3:1 이상이고 (invBg chroma < 0.03 또는 hue 차 > 20)이면 accent, 아니면 invInk |
| action | accent가 bg에 2.2:1 이상이면 accent, 아니면 ink (버튼, 링크, focus) |

- violet 금지는 이중으로 걸려 있다. 팔레트 필터 외에 system.md 규칙: OKLCH hue 약 270~330인 토큰은 255(blue) 또는 345(rose) 중 가까운 쪽으로 돌린다. 고객 브랜드 색은 `start.mjs brand`로 같은 파생을 거친다.
- radius: fintech/devtool `sharp`(4/6/8), 기본 `soft`(8/12/20), consumer app `round`(10/16/24), place는 square(`--r-lg: 0`, 버튼 2px).

### 4.2 Type pairing (start.mjs `dealTypes`)

데이터 `library/type.json`은 39개 페어링이다. "모든 face, weight, tracking, size의 유일한 출처"다.

```text
{ id, class, kinds:{tech:3, software:3, gaming:1, product:1, service:1}, moods[],
  display:{family, w:[400,600], tech:500, stretch, tracking, trackingXl, scale,
           letters:'wght'|'wdth'|null, opsz?, wdth?},
  text:{family, w}, mono?, suits, place?: 'serif'|'plain'|'soft' }
class 분포: neo-grotesk 19, serif 9, geometric 6, wide 2, grotesk-soft 1, slab 1, soft 1
place 사용 가능: 18개
```

비-place 알고리즘:

```text
pool   = types where kinds[page] > 0  (and display.letters if --axis)
used   = history.types.last(3)        # css 명령으로 실제 빌드에 쓴 것
dealt  = history.dealt.last(3)        # deal로 보여주기만 한 것
recency(t) = 0.15 if t in used else 0.5 if t in dealt else 1
out = []
repeat until 3:
  w(t) = kinds[page]^3 * recency(t) * (0.15 if t.class already in out else 1)
  out += weightedPick(pool, w); pool -= pick
history.dealt = (history.dealt + out).last(30)
```

- kind 가중치를 **세제곱**한다(3은 1의 27배). kind에 맞는 face가 계속 나오되, 최근 것은 제거가 아니라 "감광"만 한다. 같은 class(예: neo-grotesk) 두 번째는 0.15배로 눌러 3개가 서로 다른 성격이 되게 한다.
- place: serif, plain sans, soft sans 그룹에서 하나씩 3개. trade의 그룹을 맨 앞에 둔다(bakery/hotel/restaurant/wedding -> serif, retail/workshop/studio/clinic/law/agency -> plain, wellness/cafe -> soft). 최근 types 6개 + dealt 3개는 그룹 내 후보가 남아 있을 때만 피하고, 그룹 내에서는 균등 확률이다.
- 출력 값 강제: display weight 400(tech/software/gaming 500), tracking은 [-0.045, 0]으로 clamp, place는 stretch 100%와 scale 1 고정. mono는 tech 계열이나 `--mono`일 때만(기본 JetBrains Mono). 600은 nav initial tile용으로만 로드, 700/800 금지.
- `--axis`: word/editorial hero는 weight나 width 축이 있는 face만 받는다(hero의 live word, letters moment가 축을 애니메이션함).
- 금지 face: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Space Grotesk, Plus Jakarta Sans, system look. 한 페이지 최대 2 family, 4 font file.

### 4.3 Hero layout (assets/layout/deal.mjs)

`heroes.json`의 11개 hero는 kind별 가중치, `needs`(`|`는 OR), `avoid`를 갖는다.

| hero | weights | needs | avoid | h1 크기(1440/390), 최대 글자 |
|---|---|---|---|---|
| place | place 1 | photo | | 48/32, 48자 |
| split | service 3, software 2 | photo\|ui\|object | | 72/40, 45자 |
| photo | product 2, service 2, gaming 3 | photo | | 80/44, 32자 |
| product | product 3, software 1, gaming 1 | object\|photo | | 72/40, 40자 |
| editorial | 모두 0 (지정 시만) | photo | | 156/56, 34자 |
| collage | software 3 | ui | | 64/40, 48자 |
| word | service 2, software 2 | ground | photo, film, ui, object | 144/54, 28자 |
| film | product 2, service 2, software 1, gaming 3 | film\|photo | | 72/40, 42자 |
| statement | service 3, software 2 | ground | photo, film, ui, object | 56/34, 54자 |
| triptych | software 2 | ui\|photo | | 52/40, 34자 |
| centred | software 3 | ui | | 72/40, 36자 |

```text
has = given --has + 'ground'  (기본: software ui, product/service/place photo)
gaming = type software and (--kind gaming or has film/photo/setting without ui)
if gaming: has -= ui;  else if setting in has: has.replace(setting -> photo)
hero =
  type == place                                  -> 'place' (never dealt)
  object in has and no photo/film                -> 'product' (full-width stage)
  gaming and setting and no photo/film/object    -> 'photo' (이름을 배경 사진 위 크게)
  else: ok = heroes where weight[kindKey] > 0 and needs met and no avoid hit
        fresh = ok - history.heroes.last(3)
        weightedPick(fresh or ok, weight)
history.heroes = (history + hero).last(20)
```

- word/statement는 `avoid`로 강한 사진이 있을 때 나오지 않는다. 사진이 있으면 사진이 hero를 가져가야 한다는 판단이다.
- product 페이지는 product/photo/film만 받는다. split, word, statement, triptych는 제품을 content 폭의 80%로 보여줄 수 없기 때문이다(테스트에서 stage의 44% 크기 render가 작아 보였다).
- `--stats N`으로 N페이지 분포를 시뮬레이션할 수 있다. 가중치 튜닝을 데이터로 하겠다는 설계다.
- nav, footer, close, rhythm, buttons, mark는 kind별 목록에서 균등 무작위다. 사진이 없으면 사진 의존 항목은 정해진 대체로 재-deal한다(`nav-cards -> nav-split|nav-centre`, `close-photo -> close-word` head row, `media-band -> space`).

### 4.4 Moments (moments.mjs `deal`)

moment는 페이지당 "기억에 남는 한두 곳"이다. 18개 폴더 중 5개 retired, 13개가 dealt. other kind(place/product/service)는 `photo-chapters`, `pinned-chapters`, `picture-develops`(film look), `word-highlight`만 받는다.

```text
pool = moments where id not excluded, weight > 0, not retired,
       page in m.pages, m.webgl <= BUDGET(4) - spent,
       kind/fits filters, (needs.photo only with --photo)
spent = scene.webgl + count(effects) + --contexts         # 최악 기준 1 effect = 1 context

# history를 cycle로 읽기
used = {}; lastAt = {}
for id in history (oldest -> newest) if id in pool:
   lastAt[id] = i; used.add(id)
   if |used| == |pool|: used.clear()       # 한 바퀴 다 돌면 새 cycle
tail = 최근 dealt된 id들, 개수 min(3, max(0, |pool| - count))   # cycle 경계에서도 즉시 재등장 금지

together(m, p):
   other kind: statement(m) != statement(p) or m.kind != p.kind
   tech:       group(m) != group(p)       # hover와 liquid는 같은 'pointer' 그룹
   and not avoidWith either way
   and not (둘 다 fits가 1개이고 같은 slot)
   and m.webgl + p.webgl <= room

for n in 1..count:
   open  = pool where together with all picks
   cands = open - used - tail
   if empty: cands = (open - tail) sorted by lastAt asc, 앞쪽 절반(ceil)
   pick weighted by m.weight with seeded rng
history.moments = (history + picks).last(200)
```

- 핵심 아이디어는 **cycle 기반 비반복**이다. 모든 후보가 한 번씩 나와야 같은 id가 돌아오고, cycle이 막 끝나도 최근 3개는 바로 오지 않는다.
- other 페이지에서는 거의 모든 moment가 scroll을 따르므로 "같은 kind 금지"를 쓰면 하나밖에 못 고른다. 그래서 규칙을 "statement 하나 + section 하나, 또는 서로 다른 kind"로 바꾼다.
- 모든 moment는 reduced motion용 still과 phone용 variant가 필수다(`meta.phone`, `meta.reduced` 검증). 가벼운 것만 `phoneRuns: true`로 phone에서 실행한다. card 안에 넣는 것은 금지다.
- hero moment(0~1)는 dealt hero가 `heroes.json`에서 그 moment를 나열할 때만 유지한다.

### 4.5 Effects (scripts/effects.mjs + assets/effects/pick.js)

```text
gate: --page가 tech/gaming/software(또는 product --tech-subject)가 아니면 빈 deal, exit 0
pool = effects where random != false, motion != interactive(기본), palette kind fits,
       (quiet: not focal and family not in [pattern, dither])
for slot n:
   if named(slot:id): 그대로 (kind/slot/avoidWith/중복 검증은 동일 적용)
   cands = slotPool where no avoidWith clash with page, id != prev, not on page
   w(e) = 0.35^(uses in history.last(20))
          * (0.5 if e in history.last(5))
          * 0.3^(same family already on page)
   weighted pick with mulberry32(seed)
history.picks = (history + picks).last(500)
```

- tech 페이지 예산: effect 1개(shader ground, WebGL part, object, big scene 중 하나), live WebGL context 최대 4개, card는 scroll로 움직이지 않는다.
- `random: false`(dotted globe, photo grade 등 "문자 그대로의 주제")는 무작위로 나오지 않고 이름으로만 지정한다. 의미가 있는 시각물은 운에 맡기지 않는다는 구분이다.
- `quiet` slot(큰 UI 창, 스크린샷, 텍스트를 얹는 자리)에서는 focal ground와 pattern/dither family를 뺀다. cards.md가 UI 뒤 pattern을 금지하기 때문이다.

### 4.6 Big scene

11개 scene, tech 전용, 페이지당 최대 1개. `needs`(고객의 사진, 화면, 문장)를 brief가 충족할 때만, `.taste-skill/scenes-history.json`의 최근 3개를 피해 가중 무작위. hero는 1 screen이므로 `restH: 2`인 scene은 hero 아래 2-screen section으로만 간다. object scene은 고객 업종의 물체만(카드게임 엔진은 카드 덱, edge network는 지구본).

## 5. 9개 house rules 상세

"이 9개가 skill의 다른 모든 것보다 우선한다."

| # | 규칙 | 구체 수치와 집행 |
|---|---|---|
| 1 | 그림, render, 시각물 아래 캡션/설명 금지 | 라이선스 credit은 footer 한 줄(110자 이내, 출처만, 사진가 이름 금지). checker `visual-caption`, `caption`, `credit-wall`(1000px 이상에서 2줄 이상 FAIL, 사진 credit 링크 3개 이상 FAIL) |
| 2 | 모든 시각물이 렌더된다, 빈 바탕 금지 | 1440, 1024, 768, 390에서. `visual-empty`: 120x80 이상 시각물이 6색 미만 또는 99.8% 단색(canvas 98%)이면 FAIL. `gl-fallback`: shader를 강제로 실패시켜 still fallback 확인 |
| 3 | 한 화면에 한 section | hero는 첫 화면 단독, 모든 section은 1440x900에서 정확히 1 또는 2 screen(±2px), 다음 section heading이 엿보이면 안 됨. 예외: `photo-chapters` 3~4 screen |
| 4 | 좌우 content edge 동일 | `.wrap` = `min(100% - 2*gut, 1280px)`, 1440에서 x 80과 1360(place는 1200폭, 120~1320), 390에서 24와 366 |
| 5 | Hover micro-animation | linked card 2px lift, 사진 1.02~1.03 zoom, 버튼 hover 1px step + press 1px 하강 & scale .985, underline draw, card loop 2.5~4s. tilt, carousel, timed tab 금지. hero는 load 시 1회 entrance(`data-enter`), 모든 페이지 dealt moment 1개(긴 페이지 2개). gate가 `hero-enter`, `moment-none` WARN을 FAIL로 승격 |
| 6 | 더 많고 좋은 실제 사진 | 고객 사진이 없으면 라이선스 stand-in(같은 종류의 실물), 보고서에 stand-in이라고 명시. 3D render는 brief가 요청할 때만 |
| 7 | 실제 풀컬러 아이콘 | 알려진 제품은 실제 아이콘, 직접 그린 look-alike 금지. card 안 작은 diagram(hub와 branch, input -> processor -> 3 lanes, 선 위 pulse) |
| 8 | award-site scene과 creative moment도 skill의 일부 | 모든 페이지가 moment를 deal한다. shader effect와 scene은 기술 주제가 있는 trade만. 동네 카페, 빵집, 게스트하우스, 가게는 사진을 받는다 |
| 9 | 주소 | 거리와 지역만(거리 없으면 지역), 번지, 우편번호, 좌표 금지. 사업자/VAT 번호 금지. 실제 형식 전화번호 금지. 연락처는 `.example` 도메인. 지도 링크는 OpenStreetMap search, 도시만 있으면 지도 링크 자체 금지 |

보조 규칙(Never 목록): 스크롤 fade-in, 텍스트 parallax, scroll-jacking, 남의 제품인 척하는 stock, 실제 로고의 그린 모조품, 발명된 리뷰, 페이지 자체 디자인의 violet/lavender, 레퍼런스 사이트 코드/카피 복사, kit 파일을 수정해서 체크 통과.

## 6. 카피 규칙과 copy-lint 규칙 목록

### 6.1 Five rules (copy.md)

1. h1은 category를 말하고, 무명 브랜드면 buyer나 장소도, 2~8단어. place는 40자 이내 "무엇과 어디"("Bakery on Mill Street, Leith"). 수수께끼, 명령형, 무드, 슬로건 금지.
2. 첫 화면에 hard fact 하나: 숫자, 장소, 가격, 날짜.
3. 모든 heading에 사물을 가리키는 명사. brand line(비유, 말장난)은 페이지당 1개, h1 금지.
4. 버튼은 동사 + 방문자가 얻는 것, 1~5단어. "Learn more", "Discover", "Explore", "Click here" 금지.
5. hero action 최대 2개(place 1개), 페이지 라벨 종류 최대 10개. main action은 nav, hero, close, phone bar에서 같은 문구. 한 화면에 3번째 복제는 FAIL(`action-repeat`).

수치 예산: 화면당 단어 product 47, place 44, service 34, 페이지 약 900단어. tech는 화면당 60~80단어(UI mock 제외), 80 초과 WARN(테스트에서 화면당 117단어 fintech가 장황하게 읽힘). 줄이는 순서: heading 아래 두 번째 문장 -> card body를 12~18단어 한 문장으로 -> 네 번째 card -> fragment가 이미 보여주는 목록.

추정 허용 범위: 발명은 coined brand name(검색 후 `names.json`에 기록)과 place의 그럴듯한 영업시간, 가격(고르지 않은 값, 3.60이지 4.00 아님)뿐이다. 모두 `data-assumed`를 달고, 추정 시간으로 "지금 영업 중" 표시는 금지.

### 6.2 copy-lint 규칙 (copy-lint.mjs, 브라우저 없이 1초 미만)

읽는 범위: heading, text, button, footer, `<title>`, meta description. UI mock(`ui-*`, `[data-ui]`, `[data-fx]`, `[data-diagram]`, `role=img`, `app-frame`, `device`), hidden, aria-hidden은 카피가 아니라 제품 화면으로 보고 건너뛴다. 단 그 안의 slop은 `copy-unread` WARN이다(mock으로 숨겨 lint를 피하는 것을 잡음).

**예산형 device 판정**:

```text
budget(id, hits, max, failAt = 2*max + 1):
  len >= failAt -> FAIL ("a tic, not a device")
  len >  max    -> WARN
  len >  0      -> INFO
```

| id | 등급 | 내용과 기준 |
|---|---|---|
| copy-residue | FAIL | lorem ipsum, `[company name]`, "Certainly!", "I hope this helps", "As an AI", `[insert`, `[NEED`, `{{ var }}`, "Great question!", 렌더된 markdown(`**bold**`, `## `) |
| copy-slop-word | FAIL | delve, tapestry, realm, embark, beacon, multifaceted, paradigm, myriad, plethora, meticulous, intricate, elevate, unlock, unleash, empower, harness, supercharge, seamless, effortless, cutting-edge, revolutionary, transformative, holistic, world-class, game-changer, state-of-the-art, bespoke, synergy, leverage, reimagine, next-gen, powerful, robust, nestled, boasts, unparalleled 등. title과 meta도 검사 |
| copy-stock-phrase | FAIL | "in today's fast-paced", "unlock the power", "say goodbye to", "whether you're a", "look no further", "join thousands of", "imagine a world", "not just a", "not only ... but also", "with just a few clicks", "X made simple" 등 26패턴 |
| copy-cast-company | FAIL/WARN | 페이지 자체 브랜드(title, h1)가 Fieldnote, Kestrel, Halcyon, Lumen, Nimbus면 FAIL. 다른 곳의 Acme, Northwind 등은 WARN |
| copy-two-fragment | 예산 1 | "Twelve rooms. Three ways to stay." 형태 heading |
| copy-number-pair | 예산 1 | "Four X, one Y" heading |
| copy-contrast | 예산 2 | ", not Y", isn't, not just, rather than, instead of, without the (FAQ 질문 제외) |
| copy-negation | 예산 1 | "No X, no Y" |
| copy-virtue | 예산 2 | honest, calm, quiet, actually, genuine, truly, simply, thoughtful, carefully, intentional, steady, dependable |
| copy-ing-rider | 예산 1, WARN만 | ", ensuring...", ", allowing..." |
| copy-since / copy-response-time | 예산 1, WARN만 | "since 19xx" 반복, "within 24 hours" 반복 |
| copy-puffery / copy-reveal | 예산 0, WARN만 | serves as, pivotal, in the heart of, where X meets Y / "The result?", "this section", "here are 5 reasons" |
| copy-proof-figure | WARN | "3x faster", "10,000+ teams", "98% satisfied" |
| copy-em-dash | WARN | 본문 em dash 3개 이상 |
| copy-exclaim | WARN | 느낌표 있는 줄 |
| copy-stat-strip | WARN | 문장 없이 짧은 숫자 줄 3개 이상 연속(같은 단위 열은 시간표로 보고 제외) |
| copy-numbered / copy-eyebrows | WARN | `01` 류 step 번호 6개 이상 / eyebrow, kicker 클래스 5개 이상 |
| copy-cast | WARN | 모델 기본 인물명(Priya, Marcus, Maya, Nora 등) |
| copy-footer-signoff / copy-stale-year | WARN | "Made with love in..." / 저작권 연도가 올해보다 과거 |
| copy-rhythm | WARN | 15문장 이상에서 문장 길이 표준편차 < 4, 또는 4단어 이하 문장 비율 > 30% |
| copy-quotes, copy-triads | INFO | 따옴표 추천사 3개 이상, 3항 나열 |

오탐 방지 장치가 정교하다.
- **literal 예외**: 업종에서 문자 그대로인 단어는 통과. `bespoke tailoring`, `seamless knit`, `robust steel frame`, `a powerful 2,000 W motor`(뒤에 숫자+단위), `leverage up to 1:30`(금융 비율), `intricate lace`, `elevated walkway`, `unlock the door`. gaming kind는 realm, embark를 허용하고 beacon은 tech 계열 전체에서 허용.
- **virtue literal**: `a quiet room`, `calm water`, `genuine parts`처럼 뒤에 사물 명사가 오면 통과. `the bay stays calm`처럼 장소 주어 + 상태 동사도 통과하지만 주어가 team, service, we, our면 미덕 주장으로 본다. `-ly` 부사는 runs, hums, closes 같은 기계 동사 뒤에서만 literal.
- **brand name**: 고객 이름(로고 텍스트, og:site_name, title의 `:` 앞)에 든 slop 단어(Elevate Pilates)는 카운트하지 않고 `copy-brand-word` WARN 1회.
- **약어 마침표**(St., No., e.g.)는 문장 끝으로 보지 않는다.

## 7. gate와 consistency 검사 알고리즘

### 7.1 gate.mjs: finish gate

**활성 조건**: `.taste-skill/build.json`이 있거나 `gate.json` status가 `active|fail|error`. marker를 지워도 build는 끝나지 않는다. `start.mjs deal`이 marker가 없을 때 자동으로 arm한다(css, brand는 하지 않음: 끝난 페이지의 restyle일 수 있으므로). 한두 폴더 위에 열린 build가 있으면 새로 만들지 않고 합류한다.

**검사 묶음** (한 번에 하나, 각자 새 Chrome profile):

```text
1. consistency.mjs --quick --widths 1440,390 --json (+kind, category, primary, root)
   390이 있으면 320x640 narrow pass(overflow, collide, tap-size) 포함
2. assets/layout/check.mjs --sizes 1440x900,390x844 --json   # finding 전부 FAIL
3. static: kit-edited     # 페이지가 로드하는 assets/ 파일이 이번 버전 kit와 다름
                          # (공백, 따옴표, 세미콜론, 콤마 차이는 무시: formatter는 수정이 아님)
           checker-gaming # 페이지 코드가 navigator.webdriver, __playwright, callPhantom,
                          # checker의 __cc hook을 검사 (문자열 속 코드 예시는 제외)
           gaming-suspect # UA에서 headless 검사, 모든 그림의 aria-hidden 제거 (waiver 가능)
4. copy-lint.mjs --json   # 파일에 section이 없으면 consistency가 저장한 rendered.html을 lint
                          # 둘 다 없으면 "not checked"로 남겨 PASS 불가
```

**판정 규칙**:
- WARN은 막지 않는다. 단 `HELD = {hero-enter, moment-none}`은 checker가 WARN으로 내도 gate가 FAIL로 취급한다(kit 데모에는 둘 다 없어서 checker 자체는 WARN이어야 하는 사정).
- `merge`: `check|where`가 같으면 하나로 합치고 width 목록만 모은다.
- `mergeFamilies`: 두 checker가 같은 section의 같은 결함을 다른 id로 부르는 경우(`section-height`/`screen-height`/`screen-short` -> height, `one-section`/`neighbour` -> neighbour)를 section id 기준으로 하나의 finding, 하나의 waiver로 합친다.
- 무엇이든 실행되지 않았으면(crash, timeout) FAIL 0개여도 PASS가 아니다.

**Waiver** (`.taste-skill/waivers.json`, 배열 `{check, target, reason}`):

```text
reject if: waivers > 5                       -> 그 자체가 hard FAIL "too many waivers: fix instead"
           target < 3 chars (where 전체와 일치할 때만 예외)
           reason < 12 chars
           check가 kit-edited 또는 checker-gaming   (waive 불가)
           target이 여러 finding에 매칭           -> "name one"
copy slop/stock/residue/unread: hit마다 별도 finding (where = 단어 + 그 문장)
copy tic(예산 초과 device): where 전체 문자열과 정확히 일치해야 waive
                             -> 나중에 추가된 hit는 자동으로 덮이지 않음
```

**라운드** (`.taste-skill/gate.json`):

```text
ROUND_KEY = page fingerprint + ':' + sha1(waivers.json)[:8]
수동 실행:
  ROUND_KEY 변경 -> round += 1
  변경 없음      -> round 아님, 결과 재사용
hook stop(Claude Code Stop hook 등):
  첫 수동 실행 전의 stop    -> round 아님, FAIL 목록 보여주고 block (별도 장부)
  block 직후 미변경 stop    -> 1회 허용 (사용자에게 질문하려는 stop으로 간주)
  그 외 미변경 stop         -> 2회 더 block, 이후 매번 1 round로 계산
round < max(기본 3)  -> GATE: FAIL n (round k of max)
round == max          -> GATE: OPEN n, 한 번 알리고 이후 모든 stop 허용
PASS 또는 OPEN        -> build.json을 build.done.json으로 rename
--done "<사용자 말>"   -> 사용자가 멈추라고 했을 때만, GATE: DONE
```

**가두지 않는 장치**: build당 rounds + 4 block 초과 또는 폴더에서 6시간 30 block 초과 시 모두 허용, 24시간 idle 허용, 처음 잡은 session이 아닌 다른 session 허용, 하위 폴더 2개 이상에 build가 있으면(orchestrator) 허용, stdin 2초, 전체 9.5분 예산, 각 check에 watchdog 프로세스를 붙여 gate가 죽으면 자기 Chrome만 kill. 예외 발생 시 hook 모드는 무조건 허용("broken gate must not hold a session").

마지막 줄은 정확히 하나: `GATE: PASS | FAIL n (round k of m) | OPEN n | QUICK n | SETUP (...) | ERROR (...) | OFF | DONE (...)`. exit code: 0 PASS/OFF/DONE, 1 FAIL/OPEN, 2 ERROR, 3 SETUP.

### 7.2 consistency.mjs: 브라우저 checker

"리뷰어가 눈으로 표시하는 결함을 실제 브라우저에서 찾는다." 각 요소는 그것이 온전히 보이는 첫 화면에서 한 번만 판정한다. 결과는 FAIL(고쳐야 함)/WARN(보라), crop 이미지(빨강: 요소, 파란 점선: 비교 대상)와 한 줄 fix. 판본별로 "실제 테스트 페이지에서 본 결함"을 추가해 왔다(1~4 pass, v4, v5, v5i, 2.5.1의 44-site test).

| 영역 | 주요 check와 임계값 |
|---|---|
| rhythm (1440x900, 768x1024, 390x844, 각 화면 = 정확히 900/1024/844px) | SR-1 `hero-screen` hero 단독, SR-2 `section-height` 1 또는 2 screen ±2px(FAQ와 tab을 모두 연 상태도), SR-3 `section-air`, SR-4 `one-section`, SR-5 `one-heading`, SR-6 `container-edges`, SR-7 `row-lines`, SR-8 `split-pair`. 모두 FAIL. `scroll-snap-type` 존재 자체가 FAIL |
| section-tile | 1440x900에서 1~2 screen ±24px가 아니고 tile에 다른 section의 heading, 텍스트, 그림이 보이면 FAIL, 바탕만 24px 이상이면 WARN |
| empty-area | section 내 빈 영역(내용 없는 행, 컨테이너 절반 미만을 덮는 내용 옆 빈 폭)이 section 면적의 35% 초과 WARN, 50% 초과 FAIL |
| layout | off-grid, stagger, top-stagger, right-edge, centre-axis, tilt, row-gap, hole, heading-align, col-edge(split 두 번째 열이 3곳 이상에서 시작 WARN) |
| text | cut-text, fold-cut, orphan, contrast, busy-ground(사진 위 글자 아래 인접 픽셀 dL* 디테일, 5~95% 분포 폭), heading-scale(h3가 h2의 1.3배 이내 WARN, 수치가 h2의 1.08배 이상이면 FAIL) |
| ink | text-contrast: 본문 7:1, caption/label/muted 4.5:1, large 4.5와 3:1. body-size 16px 미만 WARN |
| nav | 바와 content 간격 24px 초과 FAIL, tablet에서 wordmark + 메뉴 버튼만 있고 main action이 들어갈 240px 이상 여유가 있으면 FAIL |
| buttons | button-styles(모양, 높이, 라벨 크기), same-action, fake-button, cta, button-contrast(외곽선 없는 채움 버튼이 주변 바탕과 1.3:1 미만 WARN) |
| motion | scroll-linked, scroll-reveal, loop-pause(보인 뒤 5초 이상 움직이면 pause 버튼 필요, 픽셀로도 판정), webgl(live context 4개 초과 FAIL), reduced-motion(1.5초 뒤에도 움직이면 FAIL), loop-cycle(2.5~4s 밖), hover-move(tilt FAIL, 6px 초과 lift나 1.03 초과 확대나 사진 1.05 초과 WARN, hover에 아무 변화 없으면 FAIL), hidden-content(IntersectionObserver가 콜백하지 않는 상태, script off 상태에서도 텍스트가 보여야 함) |
| render | empty-visual(시각물만 숨기고 다시 찍어 픽셀이 같으면 바탕만 그린 것, 1.2초 뒤 재확인), shader-lint(GLSL ES 예약어를 이름으로 사용: flat, smooth, sample, input, output, filter 등), gl-fallback, 느린 모바일(1.6 Mbit/s, 400ms, 캐시 없음)에서 사진 프레임이 1초 뒤에도 비면 400KB 초과나 레티나 폭 2배 초과 시 FAIL |
| visuals | product-shown(제품 페이지 hero에 사진, render 없음 FAIL. 픽셀로 찾은 제품 경계가 hero 컨테이너 content 폭의 60% 미만 FAIL, 60~80% WARN), same-object(같은 물체가 4개 이상 section에서 통째로 보이면 WARN), photo-repeat(내용 비교로 같은 사진, 제품 페이지는 FAIL), photo-upscale |
| copy | copy-headline(h1이 category와 buyer/place를 말함), copy-fact(첫 화면 숫자, 가격, 날짜, 장소, 플랫폼, 장르), copy-headings, copy-buttons, copy-actions(hero action 3개 이상 FAIL), copy-length(22단어 이상 또는 4줄 이상 heading WARN, tech 화면당 약 80단어), fact-agree(영업시간만 비교: 같은 요일 두 시간대 FAIL) |
| contact | street-number, postcode, coordinates, company-number, phone-number(텍스트, 링크, JSON-LD, head 메타까지). 둥근 수치(4000 Bookings), 연도 시작 일련번호는 주소 옆이 아니면 postcode로 보지 않음 |
| phone (600px 이하) | collide(두 줄의 글자가 겹침, section이 다음 section을 침범, 고정 바가 내용을 덮음), tap-size(44px 미만, 32px 미만 높이나 24px 미만 폭이면서 8px 안에 다른 target이 있으면 FAIL) |
| basics | a11y-name, img-alt, field-label, heading-order, tabindex, focus-ring, menu-toggle FAIL, skip-link WARN, Tab walk(focus-visible 변화 없음이나 3:1 미만 FAIL, header 아래 가려짐), lang, page-meta, share-meta, map-link, open-now, assumed 목록, run-on |

추가 장치: 측정 중 움직이던 요소는 0.9초 뒤 다시 재서 확인한다. 첫 화면을 1280/1152/1024/896/768로 sweep해 잘림과 overflow를 본다. Chrome은 CPU WebGL(SwiftShader)로 띄우고 context가 4개를 넘으면 가장 오래된 화면 밖 것을 해제한다. 한 결함을 두 check가 중복 보고하지 않도록 "one id" 규칙이 있다(empty-visual이 잡은 것은 visual-empty가 다시 말하지 않음).

### 7.3 layout check.mjs와 content window

check.mjs 결과는 전부 FAIL이다: `hero-fold`, `hero-maxchars`/`hero-lines`(h1을 heroes.json의 maxChars까지 늘려 stress test), `screen-short`, `screen-height`, `sparse`(채움 50% 미만), `neighbour`, `neighbour-ground`, `edge-left`, `edge-right`, `spill`, `bleed-one-side`, `one-sided`, `lines`(텍스트 시작선이 3개 이상), `overflow-x`.

section 높이 결정표(1440x900, 한 화면 content 영역 708px = y 120~828):

| content 높이 c | 결정 |
|---|---|
| < 360 | 위 section에 합치거나 빠진 그림을 추가 |
| 360~495 | 1 screen, 경고: 그림을 줘라 |
| 495~708 | 1 screen |
| 708~1,320 | 맞는 높이 없음: 708로 자르거나 495+ 두 section으로 나누거나 `.g2` |
| 1,320~1,608 | 2 screen(1,200~1,320은 경고) |
| > 1,608 | 분할 |

`.g2`는 2-screen section을 행 2개(각 최대 708)로 만들어 두 번째 tile도 독립 section처럼 보이게 한다. 708~780 사이 총높이는 합법 높이가 없으므로 72px까지 더하거나 뺀다. 채움 0.55 이상, 다음 content까지 간격 최소 192px.

## 8. 설계 판단과 이유

- **취향 대신 deal을 쓰는 이유**: 모델의 "좋은 선택"은 최빈값이다. 무작위 + history는 다양성을 구조적으로 보장하고, 가중치(kind 세제곱, trade 우선)는 무작위가 업종에 맞지 않는 선택을 하지 않게 한다. 다양성과 적합성을 가중 무작위 하나로 동시에 다룬다.
- **최근 것을 제거하지 않고 감광하는 이유**: type은 kind에 맞는 face 수가 적다. 제거하면 맞지 않는 face가 나오므로 0.15/0.5배로 쉬게만 한다. 반면 hero와 moment처럼 후보가 충분한 곳은 제외 또는 cycle을 쓴다. 후보 풀 크기에 따라 비반복 강도를 다르게 설계했다.
- **kind가 effect를 막는 이유**: 동네 가게에 shader는 업종과 맞지 않는 "트릭"으로 읽힌다는 판단이다(moments.md는 halftone, 사진을 글자 안에 넣는 효과를 "template trick"으로 부른다). 그렇다고 effect를 빼기만 하면 밋밋해진다. 테스트에서 규칙을 지킨 카페, 게스트하우스 페이지가 creativity 2.5~4, motion 3~4.5에 그쳤고 원인은 "모든 section이 사진 하나 옆 텍스트"와 "포인터에 반응 없음"이었다. 그래서 place의 창의성은 사진 배치 5종(bleed, pair, trio, strip, tall-small), type moment 하나, hover layer에서 오게 했다.
- **section = 정확히 1~2 screen인 이유**: 심사자가 1440x900 tile 단위로 스크린샷을 본다. 높이만 맞추면 "한 화면 한 아이디어"가 측정 가능한 규칙이 된다. 그래서 `min-height`, `dvh`, script 높이를 금지하고 `100svh * --h`만 쓴다.
- **gate가 WARN 일부를 FAIL로 올리는 이유**: kit 데모 페이지는 hero entrance와 moment가 없어서 checker 자체는 WARN이어야 하지만, 실제 빌드에서는 house rule이다. 도구의 일반성과 정책의 엄격함을 층을 나눠 해결했다.
- **waiver를 hit 단위로 묶는 이유**: "check 하나 전체 waive"를 허용하면 나중에 생긴 결함까지 덮인다. target이 정확히 하나의 finding에 매칭되어야 하고, copy tic은 where 전체가 일치해야 하므로 단어가 하나 늘면 waiver가 무효가 된다. 최대 5개 제한은 "fix instead" 압력이다.
- **checker-gaming을 waive 불가로 둔 이유**: 에이전트가 체크를 통과하려고 headless 감지 분기를 만드는 것이 실제로 관찰된 실패 모드이기 때문이다. kit 파일 수정도 같은 이유로 waive 불가다. 포매터 차이는 무시해서 오탐을 줄였다.
- **라운드 3회 + 무수한 탈출구인 이유**: 무한 루프로 세션을 가두는 gate는 결국 꺼진다. 강제와 탈출을 둘 다 코드로 명시해야 사용자가 gate를 켜 둔다. 질문하려는 stop 1회 무료, crash 결과 재사용, 9.5분 상한이 그 장치다.
- **copy-lint의 literal 예외**: 단어 금지 목록은 오탐이 많으면 무시된다. trade별 문자 그대로의 용법을 정규식으로 통과시켜 "규칙이 옳게 느껴지는" 상태를 유지한다.
- **토큰을 공식으로 파생하는 이유**: 팔레트 6색만 고르면 muted, inverse band, action 색이 대비 기준(4.5/7/3/2.2:1)을 자동으로 만족한다. 모델이 회색을 손으로 고를 여지를 없앤다.

## 9. 내 작업에 가져올 점

1. **선택 지점마다 dealer를 둔다.** "필터 -> history 감점/제외 -> 가중 무작위 -> 기록" 4단계는 디자인 외에도(프롬프트 변형, 예시 선택, 테스트 데이터) 그대로 쓸 수 있다.
2. **후보 풀 크기에 맞는 비반복 전략**: 적으면 감광(0.15~0.5배), 보통이면 최근 N개 제외, 많으면 cycle(모두 한 번 나온 뒤 재등장 + tail 보호).
3. **분류가 허용 범위를 결정하는 표**를 먼저 만들고, 모든 도구가 같은 선언값(meta 태그)을 읽게 한다.
4. **정성 규칙을 수치로 번역한다**: "여백이 적당" 대신 "section = 1 또는 2 screen ±2px", "사진이 작다" 대신 "content 폭의 60% 미만".
5. **lint는 budget 방식**: 수사 장치를 0으로 금지하지 않고 예산을 주고, 예산 초과 WARN, 2배+1 이상 FAIL. literal 예외로 오탐을 줄인다.
6. **gate는 라운드와 탈출구를 같이 설계**하고, waiver는 정확히 하나의 finding을 이유와 함께 덮게 한다.

재사용 프롬프트:

```text
You are building a company web page. Follow these rules:
1. Classify first: software | gaming | tech(hardware) | product | service | place.
   Write the kind on line 1 of the plan. The kind gates everything:
   shader effects, dark pages, loops, scenes only on software/gaming/tech;
   product/service/place get real photographs, flat colour, type, one or two
   photo- or type-led moments.
2. Never choose by taste. For palette, type pairing, hero layout, nav, footer,
   moment: list the allowed options for this kind, drop the last 3 used ones
   (from a history I give you), pick at random weighted toward the kind,
   take the first result, and write the pick plus one sentence why it fits.
3. Every section is exactly one or two screens at 1440x900; the hero is alone
   on screen one; equal left and right edges on one 1280px wrap, 12 columns.
4. No caption under any visual. No invented reviews, numbers, logos or names.
   Address = street + district only; no phone, no register numbers.
5. Copy: h1 names the category and the buyer or place in 2-8 words; one hard
   fact on screen one; every heading has a noun; buttons are verb + object;
   max 2 hero actions. Banned words: seamless, unlock, elevate, empower,
   powerful, robust, cutting-edge, leverage, delve, bespoke (unless literal).
   Device budgets: "X. Y." headings 1, "X, not Y" frames 2, virtue words 2.
6. Motion: card lift 2px, photo zoom 1.02-1.03, button step 1px, hero enters
   once on load; nothing fades in on scroll; no tilt, carousel or timed tabs.
7. Before finishing, list every check you could not verify and every assumed
   fact. Do not claim a pass you did not measure.
```
