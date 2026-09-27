# [작업 계획서] 4포인트 원근 보정 및 ROI 설정 자동 저장 (To-Do)

## 작업 체크리스트 (전 항목 완료)

### Task 1: 기본 `roi_config.json` 템플릿 생성 및 스키마 정의
- [x] 1.1 프로젝트 루트 및 웹앱 폴더에 표준 4개 모서리 좌표(`TL`, `TR`, `BR`, `BL`)를 담은 `roi_config.json` 생성
  - *Evidence:* `packing_jam_detector/roi_config.json` 및 `roi_config.json` 생성 완료 (버전 1.0.0, 4개 점 좌표 및 600x160 warpOutput 메타데이터 유효성 검증 완료).

### Task 2: 웹앱 4포인트 인터랙티브 캘리브레이션 UI & 상태 관리 구현
- [x] 2.1 `box_tilt.html`에 4포인트 제어 모드 버튼, 포인트 4개(TL, TR, BR, BL) 마우스/터치 드래그 인터랙션 구현
- [x] 2.2 4개 점을 연결하는 사다리꼴 폴리곤 및 15열 × 2행 원근 보간 격자선 실시간 렌더링 구현
- [x] 2.3 [초기화], [자동 맞춤], [JSON 내보내기/불러오기] 모달 및 툴바 UI 추가
  - *Evidence:* `#overlay-canvas`에 `pointer-events: auto;`, `touch-action: none;` 부여, 마우스/터치 이벤트 등록, `#warp-guide-banner` 및 `#btn-toggle-warp` 버튼 추가 완료.

### Task 3: OpenCV.js Perspective Transform & Warp 파이프라인 구현
- [x] 3.1 4개 점 좌표를 바탕으로 `cv.getPerspectiveTransform` 변환 행렬 캐싱 로직 구현
- [x] 3.2 검사 트리거 시 `cv.warpPerspective`를 수행하여 $600 \times 160$ 정규화 평면 이미지 획득 로직 구현
- [x] 3.3 정규화된 평면 이미지에서 15x2 셀을 균일하게 크롭하여 `inspect_single_box`에 전달하는 슬롯 연결
  - *Evidence:* `updatePerspectiveMatrix()` 행렬 계산 및 `inspectAll30Cells()`, `captureTemplate()` 내 `cv.warpPerspective` 적용 완료.

### Task 4: 설정값 자동 영구 저장 (`localStorage` + `roi_config.json`)
- [x] 4.1 포인트 드래그 종료 시점마다 `localStorage` 자동 세이브 및 페이지 로드 시 자동 로드 복원
- [x] 4.2 `roi_config.json` 파일 다운로드(Export) 및 파일 선택 업로드(Import) 기능 연동
  - *Evidence:* `saveRoiConfigToLocalStorage()`, `loadRoiConfig()`, `exportRoiConfigJson()`, `importRoiConfigJson()` 함수 구현 및 Playwright 자동화 테스트로 영구 저장 동작 확인.

### Task 5: 파이썬 시뮬레이터(`test_simulation.py`) 사다리꼴 왜곡 & 4점 보정 모듈 동기화
- [x] 5.1 `test_simulation.py`에 원근 왜곡된 가상 카메라 프레임 생성 및 `cv2.getPerspectiveTransform` / `cv2.warpPerspective` 검증 로직 추가
- [x] 5.2 헤드리스 자동 단위 테스트에 4포인트 원근 보정 및 15x2 정규화 검증 케이스 추가
  - *Evidence:* `python test_simulation.py --headless` 실행 결과 5개 전 항목 PASS 확인.

### Task 6: 초고속 원샷 통합 QA (Gate 3) 및 증적 수집
- [x] 6.1 원샷 검증 스크립트 작성 및 실행으로 브라우저 렌더링, 4점 조작, 15x2 왜곡 보정, JSON 입출력 증적 캡처
- [x] 6.2 `docs/04_qa_evidence/gate3_qa_report.md` 작성 및 판정
  - *Evidence:* `run_gate3_qa.py` 단일 실행 통과 (01_warp_grid_initial.png, 02_warp_point_dragged.png, 03_tilt_defect_alarm.png 증적 수집 및 종합 판정 PASS).

### Task 7: Wiki 문서화 및 지식 그래프 갱신 (Gate 4)
- [x] 7.1 `wiki/`에 4포인트 원근 보정 아키텍처 및 10초 세팅 매뉴얼 문서화
- [x] 7.2 `graphify update .` 실행
  - *Evidence:* `wiki/perspective_warp_calibration.md`, `wiki/index.md` 작성 및 `graphify update .` 실행 완료.
