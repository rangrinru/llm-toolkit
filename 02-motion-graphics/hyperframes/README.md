# HyperFrames 정리

> 원본: [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (Apache-2.0, HeyGen) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+20k stars)

**"Write HTML. Render video. Built for agents."** HTML, CSS, 미디어, seekable 애니메이션을 **결정적(deterministic) MP4**로 렌더하는 오픈소스 프레임워크. 에이전트가 영상을 만들게 하는 데 특화.

## 동작 원리
- 영상을 HTML로 정의: `data-composition-id`, `data-start`, `data-duration`, `data-width`, `data-height`, `data-track-index` 같은 data 속성으로 타이밍과 트랙 지정
- 애니메이션: GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI (seekable해야 함)
- **일시정지된 타임라인을 프레임 단위로 seek** → headless Chrome 캡처 → FFmpeg 인코딩. 같은 입력 = 같은 결과
- 빌드 단계 없음 (`index.html`이 그대로 재생/프리뷰)

## Remotion과 비교 (README 기준)
| 항목 | HyperFrames | Remotion |
|---|---|---|
| 작성 | HTML + CSS + seekable 애니메이션 | React 컴포넌트 |
| 빌드 | 없음 | 번들러 필요 |
| 에이전트 인계 | 일반 HTML 파일 | JSX/React 프로젝트 |
| 분산 렌더 | 로컬, AWS Lambda | Remotion Lambda (성숙) |
| 라이선스 | Apache 2.0 | Source-available Remotion License |

공통점: headless Chrome + FFmpeg. 기존 Remotion 프로젝트는 `/remotion-to-hyperframes` 스킬로 변환 가능. → [Remotion 프롬프트](../remotion/remotion-video.md)

## 설치
```bash
# Claude Code
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes      # 사용: /hyperframes:hyperframes

# 다른 에이전트 (OpenCode, Codex, Cursor, Gemini CLI 등)
npx skills add heygen-com/hyperframes             # core 스킬
npx skills add heygen-com/hyperframes --all       # 전체 9개
```
- 요구사항: **Node.js 22+, FFmpeg**. 기본 포맷 1920x1080, 30fps

## 수동 CLI
```bash
npx hyperframes init my-video
cd my-video
npx hyperframes preview      # 브라우저 미리보기 (live reload)
npx hyperframes render       # MP4로 렌더
npx hyperframes check --json # 계약(contract) 검증
npx hyperframes add flash-through-white   # 셰이더 전환
npx hyperframes add data-chart            # 애니메이션 차트
```

## 스킬 9종
| 스킬 | 용도 |
|---|---|
| `/hyperframes` | 계약과 작업 루프 (먼저 읽을 것) |
| `/hyperframes-cli` | CLI 사용 |
| `/hyperframes-registry` | 약 450개 블록/컴포넌트 카탈로그 |
| `/media-use` | 음악, 효과음, 이미지, 아이콘, 음성, 자막 |
| `/figma`, `/slideshow`, `/remotion-to-hyperframes` | 필요할 때 (온디맨드) |
| `/reverse-any-video`, `/style-sampling` | Pro 기능 |

예시 프롬프트:
```text
Using /hyperframes, create a 10-second product intro with a fade-in title, a background video, and subtle background music.
```

## 설치 없이 응용할 모션 원칙 (스킬 문서 기준)
1. **모든 화면 상태는 타임라인 시간의 함수**: `Date.now()`, 시드 없는 `Math.random()`, 네트워크 fetch, 타이머, 무한 반복 금지 → 결정적 애니메이션
2. **SPEC 먼저**: 형용사를 수치로 바꾸고, 샷은 프레임 단위로. 긴 영상(약 15초 초과)은 서로 다른 스토리라인 3개를 말로 먼저 제시하고 고르게 한 뒤 SPEC → 스냅샷 리뷰 → 승인 후 렌더
3. **Ease는 역할별로**: 도착은 긴 꼬리(`expo.out`, `power4.out`), 카메라/컬러 플러드는 `power2.inOut`, 줌 스루/퇴장은 `power3.in`. **모든 것에 power2.out 0.5s는 "생성된 티"**
4. **타이밍 수치**: 빠른 이동 0.3~0.6s, 퇴장은 입장보다 40~50% 짧게, 앞 요소가 30~50% 진행됐을 때 다음 시작, stagger는 단어 60~120ms / 리스트 40~80ms, 스프링 damping 0.7~0.85(0.3 미만은 만화적)
5. **타이틀은 안착하면 완전히 정지**, 움직임은 다음 요소/카메라/배경으로 넘김. 모든 요소에 fade + slide-up 금지
6. **비트 그리드**: frames per beat = fps x 60 / BPM, 비트마다 인덱스로 계산해 반올림 (누적하면 드리프트). 비트에 컷, 마디에 레이아웃 변경
7. **Safe zone**: 콘텐츠는 90% action-safe, 자막과 핵심 텍스트는 80% title-safe 안
8. **요청한 것만**: 요청하지 않은 보이스오버, 자막, 새 화면비를 추가하지 않음. 명명된 효과/차트는 직접 만들기 전에 레지스트리 먼저 검색

## 주의
- 스킬이 시작 시 사용량 이벤트(`npx hyperframes events`)를 보내도록 되어 있음 (opt-out 존중)
- `/reverse-any-video`, `/style-sampling`, HeyGen 아바타/음성 모델은 Pro/계정 필요
- 데스크톱 앱(macOS/Windows/Linux)은 무료
