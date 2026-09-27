# [작업 계획서] 고정 가로형 촬영 및 좌➔우 컨베이어 최적화 (To-Do)

## 작업 체크리스트 (전 항목 완료)

### Task 1: 회전 오버레이 제거 및 고정 가로형 레이아웃 단일화
- [x] 1.1 `light.html` 및 `color.html`: `#portrait-overlay` 및 세로 모드 안내 전면 삭제
- [x] 1.2 전체 뷰포트를 가로 모드 고정(Landscape Fixed)으로 고정하고, 우측 패널을 슬림화(220px)하여 좌➔우 컨베이어 가시 영역 최대화
  - *Evidence:* `#portrait-overlay` 제거, `#sidebar` 너비 220px 축소, 카메라 뷰 영역 가로 폭 극대화 완료.

### Task 2: 모바일 실기기 카메라 재생 보장 및 블랙스크린 해결
- [x] 2.1 `v.play()` 명시적 호출 및 `playsinline`, `webkit-playsinline`, `autoplay`, `muted` 강제 적용
- [x] 2.2 모바일 해상도 오버컨스트레인 에러 방지를 위한 3단계 폴백(`environment 1280x720` -> `environment` -> `video: true`) 구현
- [x] 2.3 카메라 상태 표시 인디케이터(`camera-status`) 추가 및 터치 잠금 해제 폴백 구축
  - *Evidence:* `startCamera()` 내 다단계 try-catch 스트림 할당 및 `v.onloadedmetadata` 내 `await v.play()` 처리 완료.

### Task 3: 좌➔우 컨베이어 주행 경로 시각화 및 판별 파이프라인
- [x] 3.1 화면 상단 컨베이어 이송 방향 인디케이터(`컨베이어 주행: 좌 ➔ 우 ▶▶▶`) 렌더링
- [x] 3.2 Trigger ROI를 벨트 좌➔우 흐름의 적정 지점(X: 300, W: 100, H: 280)에 기본 배치 및 좌측 진입 감지 로직 점검
- [x] 3.3 가상 컨베이어 모드 및 실시간 카메라 모드 좌➔우 이송 0.1초 경보 연동 확인
  - *Evidence:* `#conveyor-flow-badge` 슬라이드 애니메이션 추가 및 ROI 가이드 `▶ AI 통과선 [좌➔우]` 오버레이 적용 완료.

### Task 4: 자동화 검증 및 증적 수집 (Gate 3)
- [x] 4.1 Playwright 기반 QA 스크립트 실행으로 고정 가로형 레이아웃 및 좌➔우 검사 증적 캡처
- [x] 4.2 `docs/04_qa_evidence/gate3_qa_report.md` 작성 및 판정
  - *Evidence:* `python run_gate3_qa_feature1_2.py` 실행 결과 ALL PASS (exit code 0), 증적 캡처 완료.

### Task 5: Wiki 갱신 및 완료 (Gate 4)
- [x] 5.1 `wiki/landscape_ai_vision_upgrade.md` 및 `wiki/index.md` 갱신
- [x] 5.2 사용자 테스트 안내 보고
  - *Evidence:* 위키 아키텍처 및 고정 가로형 설명 갱신 완료.
