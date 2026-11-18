# 21개 페이지 구조 (Macrostructures)

> 출처: [hallmark references/macrostructures.md](https://github.com/Nutlope/hallmark/blob/main/skills/hallmark/references/macrostructures.md)
> **메뉴가 아니라 어휘다.** 프롬프트에 맞게 먼저 페이지를 설계하고, 설계한 구조에 이름을 붙이는 용도. 여기서 먼저 고르면 결국 같은 3개로 수렴한다.

| # | 이름 | 설명 |
|---|---|---|
| 01 | Bento Grid | 크기가 다른 블록의 불규칙 그리드. 리듬은 카드 균일성이 아니라 크기 변화에서 |
| 02 | Long Document | 메모, 편지, 일지처럼 읽히는 연속된 글. 마케팅 구조 없음 |
| 03 | Marquee Hero | 첫 화면 전체가 하나의 문장이나 비주얼. 아래는 리스트, 그리드, 글 등 다른 것으로 |
| 04 | Stat-Led | 사용자가 준 수치 하나가 히어로. 나머지는 그 수치를 뒷받침 |
| 05 | Workbench | 실제 제품 캡처가 주 콘텐츠. 마케팅 카피 대신 짧은 캡션의 앱 투어 |
| 06 | Conversational FAQ | 굵은 질문과 바로 나오는 답. 제품과의 솔직한 인터뷰 |
| 07 | Manifesto | 강한 주장을 큰 활자로. 무엇을 사라고 하기 전에 무엇을 믿으라고 말함 |
| 08 | Photographic | 매 화면을 거대한 사진 한 장이 지배. 텍스트는 작은 주석 |
| 09 | Quote-Led | 사용자가 준 인용문이 히어로. 제목이 다른 사람의 목소리 |
| 10 | Specimen | 큰 세리프, 비대칭, 헤어라인. 서체, 출판, 글쓰기 주제에만 |
| 11 | Catalogue | 같은 것의 변형을 균일 그리드로 (서체, 팔레트, 상품) |
| 12 | Letter | 1인칭, 인사로 시작하는 창업자의 편지 |
| 13 | Index-First | 페이지가 링크 목록. 히어로 이미지 없이 내비게이션이 디자인 |
| 14 | Narrative Workflow | 번호 붙은 단계로 사용 과정을 시간순으로 |
| 15 | Split Studio | 화면을 둘로 나눈 딥틱. 한쪽 글, 한쪽 증거 |
| 16 | Feature Stack | 왼쪽 고정 제목 + 스크롤에 따라 바뀌는 오른쪽 캡처 |
| 17 | Type Specimen | 서체 자체가 디자인. 폰트 파운드리, 디자인 시스템 |
| 18 | Portfolio Grid | 필터 가능한 프로젝트 카드. 작업물이 곧 제품인 스튜디오 |
| 19 | Map / Diagram | 큰 공간 다이어그램 하나가 페이지를 구성 (플로차트, 평면도, 네트워크) |
| 20 | Ecosystem Index | 추천, 최신, 카테고리, 사람별 등 여러 탐색 경로. 둘러보기가 가치 |
| 21 | Component Playground | 코드와 미리보기 블록이 주 콘텐츠. 복사해서 쓰는 방법까지 |

## 도메인별 추천 조합 (프롬프트에 구조 언급이 없을 때)
| 도메인 | 추천 3개 |
|---|---|
| 팟캐스트, 오디오, 음악 | Photographic · Quote-Led · Letter |
| 쇼핑몰, 상품, 커머스 | Catalogue · Photographic · Bento Grid |
| 문서, CLI, SDK, API, 오픈소스 | Workbench · Long Document · Component Playground |
| 플랫폼, 인프라, 모니터링, B2B 도구 | Bento Grid · Workbench · Stat-Led |
| 에이전시, 스튜디오, 포트폴리오 | Portfolio Grid · Split Studio · Index-First |
| 개인 원페이지, 이력서 | Long Document · Letter · Index-First |
| 식당, 카페, 바, 메뉴 | Photographic · Long Document · Catalogue |
| 패션, 의류, 뷰티, 룩북 | Photographic(실제 사진) · Catalogue · Marquee Hero |
| 핀테크, 뱅킹, 결제 | Stat-Led · Workbench · Long Document |
| 선언, 캠페인, 사회운동 | Manifesto · Quote-Led · Stat-Led |
| 에디토리얼, 폰트, 매거진 | Specimen · Long Document · Type Specimen |
| 제품 출시, SaaS 마케팅 | Bento Grid · Workbench · Stat-Led |
| 컨퍼런스, 이벤트 | Marquee Hero · Manifesto · Photographic |
| 신호 없음 | Bento Grid · Long Document · Manifesto |

## SaaS 섹션 덱: 순서가 아니라 카드에서 고르기
**기본 카드** (지어낼 것 없이 항상 쓸 수 있음)
| 카드 | 역할 |
|---|---|
| Spec sheet | 제품이 실제로 가진 수치: 제한, 포맷, 버전, 리전 |
| Worked example | 실제 작업 하나를 하는 제품: 명령어와 출력, 캡처와 캡션 |
| Changelog | 실제 날짜가 있는 최근 3~4개 업데이트. 살아있는 제품이라는 증거 |
| Comparison anatomy | 지금의 방식과 제품을 항목별로 비교, 점수 없이 |
| Pricing table | 실제 가격, 2~3개 티어. 전부 "Contact sales"면 신뢰가 떨어짐 |
| FAQ | 실제 반론에 사람처럼 답하기 |
| CTA strip | 요청은 한 번, 버튼 하나 |

**소재가 있을 때만 쓰는 카드**
| 카드 | 필요한 것 | 없으면 |
|---|---|---|
| Hero visual | 실제 캡처 | 슬롯 안에 만든 제품, 또는 타이포 히어로. 슬롯 밖 div 가짜 UI 금지 |
| Logo row | 허락받은 실제 고객 로고 | 카드 자체를 빼기. "Trusted by" 금지 |
| Three features | 캡처나 수치가 있는 기능 3개 | Worked example이나 Spec sheet에 합치기 |
| Testimonials | 이름, 직함, 회사가 있는 실제 인용 | 카드 자체를 빼기. 지어낸 이름 금지 |
