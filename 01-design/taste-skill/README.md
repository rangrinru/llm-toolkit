# Taste Skill 정리

> 원본: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+19k stars)

**코딩 에이전트에게 "취향"을 주는 스킬.** 아트 디렉션, 레퍼런스 이미지, 브라우저 체크로 범용 AI 페이지 대신 전문 기업 웹사이트 수준을 목표로 한다. 현재(2.x) 레포에는 스킬 하나 `design-taste-frontend`만 있고, **회사/랜딩 사이트용**(앱 UI용 아님).

## 설치
```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```
```text
# Claude Code
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```
```bash
# Codex (새 세션에서 로드됨)
codex plugin marketplace add Leonxlnx/taste-skill
codex plugin add taste-skill@taste-skill
```
- 별도 슬래시 명령 없음. "회사 사이트 만들어줘 / 리디자인해줘"라고 하면 로드된다
- 요구사항: **Node 22+**, Chrome/Edge/Chromium(`CHROME_PATH`), ffmpeg 선택. API 키 불필요

## 핵심 개념
- **업종 분류가 모든 것을 결정**: `software`, `gaming`, `tech`, `product`, `service`, `place` 중 하나로 분류 → 페이지 계획과 허용 효과가 달라짐. 카페/호텔/샵(place)은 사진과 타이포 중심, 셰이더와 WebGL은 소프트웨어/게임/하드웨어만
- **취향으로 고르지 말고 Deal**: 스크립트가 팔레트, Google Fonts 페어링, 히어로 레이아웃 11종(split, centred, product, photo, place, collage, editorial, word, film, statement, triptych), 등장 효과와 "moment" 1~2개를 뽑고 기록해서 반복을 피함. 보라색은 쓰지 않음
- **9개 House rules**: 이미지 아래 캡션 금지 / 모든 비주얼이 실제로 렌더 / 한 화면에 한 섹션 / 좌우 가장자리 동일 / hover 마이크로 애니메이션 / 실제 사진 / 실제 풀컬러 브랜드 아이콘 / 업종별 효과 제한 / 주소 규칙
- **실제 자산**: 검증된 사진(Wikimedia Commons, Unsplash)과 실제 브랜드 아이콘 SVG를 가져오고 푸터에 크레딧
- **Finish gate**: headless Chrome에서 1440/1024/820/768/390 폭으로 PASS/WARN/FAIL 검사, 고칠 수 있는 FAIL이 없을 때까지 최대 3라운드 (Claude Code에서는 Stop hook으로 자동)

```bash
node scripts/start.mjs deal --page software
node scripts/consistency.mjs <url or file> --page <kind>
node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"
```

## 설치 없이 응용할 원칙
1. **업종부터 분류**하고 그에 맞는 효과만 허용 (동네 카페에 WebGL 금지)
2. **한 화면에 한 섹션** (1440x900 기준 1~2화면 높이), 좌우 콘텐츠 가장자리 동일, 이미지에 설명 캡션 금지
3. **카피 규칙**: h1은 카테고리와 구매자(또는 장소)를 명시, 첫 화면에 구체적 사실 1개, 제목마다 명사, 버튼은 "동사 + 목적어"(예: Book a room). 지어낸 수치 금지
4. **AI 카피 금지어**: delve, tapestry, seamless, unlock, elevate, robust / "In today's fast-paced world", "Unlock the power of" / -ing 꼬리 문구, 콜론 반전, em dash 남발, 본문 느낌표, 이모지 불릿 / 지표 3~4개를 한 줄로 늘어놓는 stat strip / "X. Y." 두 조각 제목은 1회까지
5. **실제 자산 우선**: 알려진 제품은 실제 아이콘과 실제 UI. 사진이 없으면 대체 사진임을 표시
6. **여러 화면 폭에서 렌더 검증 후 출하**, 최대 3라운드 수정 루프
7. **주소/연락처**: 거리와 지역만, 번호/좌표 없음, 연락처는 `.example` 도메인

## 관련 레포 (이전된 스킬)
- [taste-skill-classics](https://github.com/Leonxlnx/taste-skill-classics): high-end-visual-design, minimalist-ui, industrial-brutalist-ui, gpt-taste 등 이전 버전 스킬
- [imagegen-skills](https://github.com/Leonxlnx/imagegen-skills): imagegen-frontend-web/mobile, brandkit, image-to-code
