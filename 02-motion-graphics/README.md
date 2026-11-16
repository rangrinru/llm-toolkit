# 02. Motion Graphics

코드 기반 모션그래픽(Remotion, Manim, After Effects 표현식)과 AI 영상 생성(Seedance, Veo, Kling 등) 프롬프트.

## 폴더 구조
```
02-motion-graphics/
├── remotion/          # React 기반 영상 (Remotion)
├── manim/             # 수학/개념 설명 애니메이션 (Manim)
├── after-effects/     # AE 표현식, 스크립트
├── web-animation/     # CSS, GSAP, Framer Motion, Lottie
└── ai-video/          # AI 영상 생성 모델용 프롬프트
```

## 파일 목록
| 파일 | 설명 |
|---|---|
| [`remotion/remotion-video.md`](./remotion/remotion-video.md) | Remotion 영상 컴포넌트 생성 |
| [`manim/manim-explainer.md`](./manim/manim-explainer.md) | Manim 개념 설명 애니메이션 |
| [`after-effects/ae-expressions.md`](./after-effects/ae-expressions.md) | After Effects 표현식 |
| [`web-animation/web-animation.md`](./web-animation/web-animation.md) | 웹 인터랙션 애니메이션 |
| [`ai-video/video-gen-prompt.md`](./ai-video/video-gen-prompt.md) | AI 영상 생성 프롬프트 공식 |

## 작성 규칙
- 코드 기반: 렌더 명령어와 의존성 버전을 함께 기록
- AI 영상: 사용한 모델/버전, 시드, 길이를 기록

새 파일은 [`templates/prompt-template.md`](../templates/prompt-template.md) 형식을 따른다.
