# Cloudflare Security Audit Skill 정리

> 원본: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (MIT) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 1위 (+44k stars)

**여러 단계로 나눠 보안 감사를 하고, 발견 사항을 독립적으로 검증해 기계가 읽을 수 있는 형식으로 내놓는 코딩 에이전트 스킬.** 격리된 에이전트들이 정찰, 헌팅, 검증, 보고를 나눠 맡는다. tool use와 병렬 서브에이전트를 지원하는 에이전트(Claude Code 등)에서 동작.

## 설치
```bash
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit
# 전역 설치
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit \
  --global
```
슬래시 명령이 아니라 요청이 맞으면 자동 활성화:
```text
security audit this codebase
find security vulnerabilities in ./src
do a security review, output to ~/audits/my-project
```
- full audit 결과 기본 경로: `~/security-audit-skill/<repo-name>/run-<N>`

## 6단계
| 단계 | 내용 |
|---|---|
| 1. Reconnaissance | 아키텍처, 신뢰 경계, 입력 표면을 `architecture.md`, `coverage-ledger.json`에 기록 |
| 2. Coverage-led hunting | ledger 단위별로 격리된 hunter 배정, coverage critic이 빈틈을 찾음 |
| 3. Candidate validation | 후보마다 **새 verifier가 반증**을 시도 |
| 4. Structured output | `findings.json`에 confirmed / needs_validation / rejected 기록, 스키마 검증 |
| 5. Independent record verification | 새 에이전트들이 최종 주장을 다시 검증 |
| 6. Reporting | `REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md` 생성 |

- **모드**: 기본은 guidance mode(질문/집중 리뷰, 파일 생성 없음). full audit은 감사/pen-test/리포트를 명시적으로 요청할 때만
- **프로필**: `quick`(hunter 1 wave + critic 1회), `standard`(기본), `deep`(critic이 clean pass까지 반복)
- **반복 실행은 누적**: 이전 ledger와 findings를 읽어 빈틈을 겨냥. README에 따르면 한 번 실행은 반복 실행 총합의 대략 절반을 찾음
- 공격 클래스별 문서: 웹 프로토콜/인증, 클라이언트, 공급망/릴리스, 클라우드/배포, AI와 LLM, 메모리 안전성, 리소스 고갈, 데이터 격리, 데스크톱/모바일 IPC 등

## 설치 없이 응용할 원칙 (내 보안 점검 프롬프트에 추가)
1. **경계와 결과가 없으면 finding이 아니다**: 낮은 신뢰 주체, 입력, 의도된 통제, 넘은 경계, 영향받는 자원, 관찰된 결과를 모두 명시
2. **찾는 에이전트와 검증하는 에이전트를 분리**: 검증자는 새 컨텍스트에서 반증을 시도
3. **판정 3종**: `confirmed`(소스 추적 + 관찰된 결과), `needs_validation`(모르는 사실 하나를 적고 심각도 없음), `rejected`(반증됨)
4. **심각도는 confirmed에만**, likelihood x impact. 심층 방어 부재는 취약점이 아니라 hardening note
5. **배포/프록시 설정을 추측하지 않는다**: 소스에 없으면 needs_validation
6. **수정안은 가장 작은 효과적 소스 수정** + 지켜야 할 invariant + 회귀 테스트
7. **안티패턴**: 체크리스트 위반을 취약점으로 보고, 라이브 환경 테스트, 자기 영향(self-impact)을 경계 침범으로 취급, 검증 전에 보고서부터 쓰기

## 응용 프롬프트
```text
이 코드베이스를 보안 점검해줘. 수정하지 말고 읽기만.
1. 먼저 아키텍처, 신뢰 경계, 외부 입력 지점을 정리해.
2. 후보마다 [낮은 신뢰 주체 / 입력 / 의도된 통제 / 넘은 경계 / 영향 자원 / 관찰된 결과]를 채워. 못 채우면 finding이 아니야.
3. 서브에이전트(또는 새 관점)로 각 후보를 반증해 봐.
4. confirmed / needs_validation / rejected로 분류. 심각도는 confirmed에만.
5. 배포 설정은 추측하지 말고 needs_validation에 "확인할 사실 하나"를 적어.
6. confirmed마다 가장 작은 수정안과 회귀 테스트를 제안해.
```

## 주의
- 대상 코드를 실행하려면 OS 수준 샌드박스(네트워크 차단 등)가 필요. 없으면 실행하지 않고 needs_validation으로 남김
- 에이전트를 많이 호출하므로 **토큰 사용량이 크다**. Node.js 필요(검증 스크립트)
- 관련: [기본 보안 점검 프롬프트](./security-audit.md)
