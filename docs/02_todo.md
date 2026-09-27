# [작업 계획서] 모바일 16:9 광범위 카메라 뷰포트 정상화 및 반응형 최적화 (To-Do)

## 작업 체크리스트

### Task 1: 카메라 16:9 광범위 스트림 제약 조건 적용 (Implementation)
- [x] 1.1 `color.html`: `getUserMedia` constraints에 16:9 종횡비 (`aspectRatio: 1.777777778`, `width: { ideal: 1280, min: 640 }`, `height: { ideal: 720, min: 360 }`) 적용 및 단계적 폴백 구성
- [x] 1.2 `light.html`: `getUserMedia` constraints에 16:9 종횡비 (`aspectRatio: 1.777777778`, `width: { ideal: 1280, min: 640 }`, `height: { ideal: 720, min: 360 }`) 적용 및 단계적 폴백 구성
  - *Evidence:* `color.html` 및 `light.html` 내 `getUserMedia` 제약 조건에 `aspectRatio: { ideal: 1.777777778 }` 및 720p/360p 16:9 표준 해상도 적용 완료. 모바일 후면 카메라가 와이드 광각 센서 16:9 비율로 스트림을 반환하도록 표준화.

### Task 2: 모바일 반응형 16:9 뷰포트 레이아웃 구현 (Implementation)
- [x] 2.1 `color.html`: 세로 모드(`orientation: portrait` / 모바일 폭 < 768px) 시 `flex-direction: column`으로 전환하여 상단에 16:9 전폭 뷰포트(`aspect-ratio: 16 / 9`), 하단에 스크롤 컨트롤 패널 배치
- [x] 2.2 `light.html`: 세로 모드(`orientation: portrait` / 모바일 폭 < 768px) 시 `flex-direction: column`으로 전환하여 상단에 16:9 전폭 뷰포트(`aspect-ratio: 16 / 9`), 하단에 스크롤 컨트롤 패널 배치
- [x] 2.3 데스크톱 및 가로 모드(`orientation: landscape`)에서는 기존 좌우 2분할(좌 16:9 뷰포트, 우 슬림 사이드바) 유지
  - *Evidence:* 미디어 쿼리 `@media (max-width: 768px) and (orientation: portrait), (max-width: 600px)`를 적용하여 세로 모드 시 상하 배치(`flex-direction: column`) 및 상단 100vw 전폭 16:9 뷰포트 고정. 가로 모드 시 좌우 배치(`flex-direction: row`)로 16:9 뷰포트 최대화.

### Task 3: 비디오 및 캔버스 16:9 잘림(Crop) 방지 및 터치 좌표 정합 (Implementation)
- [x] 3.1 `color.html`: `object-fit: contain` 및 16:9 종횡비 고정 래퍼를 통해 좌우 화각 크롭 완전 제거 (16:9 광범위 촬영 100% 온전 노출), 오버레이 터치/드래그 ROI 좌표 1:1 정합 유지
- [x] 3.2 `light.html`: `object-fit: contain` 및 16:9 종횡비 고정 래퍼를 통해 좌우 화각 크롭 완전 제거 (16:9 광범위 촬영 100% 온전 노출), 오버레이 터치/드래그 ROI 좌표 1:1 정합 유지
  - *Evidence:* `object-fit: contain` 적용 및 `#stream-wrapper`에 `aspect-ratio: 16 / 9` 고정. 4:3 또는 16:9 카메라 영상의 좌우 80%가 잘려나가던 세로 슬릿 현상을 원천 방지하고 전체 화각 100% 보존. 캔버스 및 비디오의 16:9 비율 고정으로 터치 ROI 드래그 좌표 1:1 완벽 정합.

### Task 4: 사용자 UX 개선 및 가로 회전 권장 안내 HUD (Implementation)
- [x] 4.1 세로 모드 진입 시 "화면을 가로로 회전하시면 16:9 전체 컨베이어를 더 넓게 보실 수 있습니다" 안내 배지/토스트 표시
- [x] 4.2 `index.html` 내 진입 가이드 문구 점검
  - *Evidence:* `#rotate-hint.mobile-rotate-hint` 추가(세로 모드 시 "🔄 가로 회전 시 16:9 와이드 전체화면" 펄스 애니메이션 배지 자동 노출). `index.html` 내 배지 및 설명 문구 16:9 와이드 지원으로 최신화 완료.

### Task 5: Gate 2 교차 리뷰 및 승인 (Reviewer)
- [x] 5.1 Worker의 Diff 근거 검증 및 안정성/부작용 검토
- [x] 5.2 `docs/03_review_logs/gate2_review.md` 작성 및 PASS 발행
  - *Evidence:* `docs/03_review_logs/gate2_review.md` 작성 완료. 16:9 와이드 제약 조건, 세로/가로 반응형 레이아웃, `object-fit: contain` 크롭 방지 전수 검토 후 PASS 발행.

### Task 6: Gate 3 원샷 자동화 QA 및 증적 수집 (QA Evaluator)
- [x] 6.1 `run_gate3_qa_viewport_16_9.py` 원샷 자동화 스크립트 작성 및 모바일 세로/가로 환경 병렬 렌더링/뷰포트 비율 검증
- [x] 6.2 `docs/04_qa_evidence/gate3_qa_report.md` 작성 및 PASS 판독
  - *Evidence:* `run_gate3_qa_viewport_16_9.py` 및 `run_gate3_qa_feature1_2.py` 원샷 자동화 실행 결과 ALL PASS (Exit code 0, 12/12 정적 감사 통과, 모바일 세로/가로 실측 종횡비 1.778/1.778 일치, 콘솔 오류 0건, 스크린샷 4종 증적 확보).

### Task 7: Gate 4 위키 및 최종 완료 보고 (Master)
- [x] 7.1 `wiki/` 내 모바일 16:9 뷰포트 아키텍처 및 반응형 구조 문서화
- [x] 7.2 `graphify update .` 실행을 통한 지식 그래프 최신화
- [x] 7.3 Master 최종 작업 완료 보고 및 파이프라인 종료
  - *Evidence:* `wiki/landscape_ai_vision_upgrade.md` 갱신 완료, `graphify update .` 실행을 통한 지식 그래프 동기화, 최종 완료 보고서 작성 완료.
