# [작업 계획서] 고속 컨베이어 및 장시간 스마트폰 연속 운용 최적화 (To-Do)

## 작업 체크리스트

### Task 1: 카메라 해상도 640x480 제한 (Implementation)
- [x] 1.1 `light.html`: `getUserMedia` constraints에 `width: { ideal: 640 }, height: { ideal: 480 }` 적용
- [x] 1.2 `color.html`: `getUserMedia` constraints에 `width: { ideal: 640 }, height: { ideal: 480 }` 적용
  - *Evidence:* `light.html` 및 `color.html` 내 `getUserMedia` 제약 조건에 `constraints = { video: { facingMode: { ideal: "environment" }, width: { ideal: 640 }, height: { ideal: 480 } }, audio: false }` 적용 완료. 모바일 기기의 고해상도(FHD/4K) 입력으로 인한 다운스케일링 연산 렉 및 발열 원천 차단.

### Task 2: Buffer Zero-Allocation 전처리 파이프라인 (Implementation)
- [x] 2.1 `light.html`: 전역 `new Float32Array(1 * 3 * 128 * 128)` 고정 버퍼 할당 및 In-place ImageNet NCHW 전처리 함수 구현
- [x] 2.2 `color.html`: 전역 `new Float32Array(1 * 3 * 128 * 128)` 고정 버퍼 할당 및 In-place ImageNet NCHW 전처리 함수 구현
- [x] 2.3 루프 내부 `new Float32Array` 생성 완전 배제 확인 (정적 코드 감사)
  - *Evidence:* 전역 스코프에 `const inputTensorBuffer = new Float32Array(1 * 3 * 128 * 128);` (49,152 floats) 1회만 사전 할당. `preprocessCropToBuffer` 내부에서 매 루프 힙 할당 없이 ImageNet 정규화(Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225])와 NCHW 순서로 In-place 덮어쓰기 수행. 정적 감사 결과 루프 내부 `new Float32Array` 0건 확인. 런타임 `isSameBufferInstance: true` 검증 완료.

### Task 3: 고속 통과(0.6초) 주기 및 쿨다운 디바운스 로직 (Implementation)
- [x] 3.1 `light.html`: `CHECK_INTERVAL = 100ms`, `COOLDOWN_TIME = 400ms` 및 판정 잠금(Lock) 디바운스 구현
- [x] 3.2 `color.html`: `CHECK_INTERVAL = 100ms`, `COOLDOWN_TIME = 400ms` 및 판정 잠금(Lock) 디바운스 구현
  - *Evidence:* 제품 화면 체류 시간(약 200~300ms)을 놓치지 않도록 `CHECK_INTERVAL = 100ms` 설정. 판정 발생 시 `COOLDOWN_TIME = 400ms` 동안 판정 잠금 플래그(`isCooldown = true`)를 적용하여 동일 제품당 1회만 카운트 및 알람 처리 완료. 0.6초 주기 다음 제품 진입 시점에는 자동 잠금 해제.

### Task 4: ONNX 모델 파라미터 및 런타임 연동 (Implementation)
- [x] 4.1 ONNX Runtime Web (`ort.min.js`) 스크립트 참조 추가
- [x] 4.2 `box_posture_model.onnx` 비동기 세션 초기화 (`executionProviders: ['wasm']`)
- [x] 4.3 클래스 인덱스 매핑 (`0: defect`, `1: normal`) 판정 로직 및 우아한 폴백(Mock/Sim) 결합
  - *Evidence:* `<script src="https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js"></script>` 추가, `ort.InferenceSession.create(MODEL_PATH, { executionProviders: ['wasm'] })` 연동. 출력 텐서의 소프트맥스 확률 기준 `0: defect`, `1: normal` 클래스 매핑 완료. 가중치 파일 미로드 시에도 시뮬레이션/더미 모드로 무장애 폴백 지원.

### Task 5: Gate 2 교차 리뷰 및 승인 (Reviewer)
- [x] 5.1 Worker의 Diff 근거 검증 및 안정성/부작용 검토
- [x] 5.2 `docs/03_review_logs/gate2_review.md` 작성 및 PASS 발행
  - *Evidence:* `docs/03_review_logs/gate2_review.md` 작성 및 Diff 전수 검토 완료. 4대 요구사항 적합성 확인 및 PASS 발행.

### Task 6: Gate 3 원샷 자동화 QA 및 증적 수집 (QA Evaluator)
- [x] 6.1 `run_gate3_qa_feature1_2.py` 실행을 통한 고속 통과 및 알람/콘솔 무결성 검증
- [x] 6.2 `docs/04_qa_evidence/gate3_qa_report.md` 작성 및 PASS 판독
  - *Evidence:* `run_gate3_qa_feature1_2.py` 원샷 자동화 실행 결과 ALL PASS (Exit code 0, 10/10 정적 감사 통과, 런타임 버퍼 49,152 / 100ms / 400ms 스펙 통과, 콘솔 에러 0건).

### Task 7: Gate 4 위키 및 최종 완료 보고 (Master)
- [x] 7.1 `wiki/` 내 고속 컨베이어 및 모바일 OOM 방지 아키텍처 문서화
- [x] 7.2 `graphify update .` 실행을 통한 지식 그래프 최신화
- [x] 7.3 Master 최종 작업 완료 보고 및 파이프라인 종료
  - *Evidence:* `wiki/landscape_ai_vision_upgrade.md` 갱신 완료, `graphify update .` 실행을 통한 지식 그래프 최신화, 최종 완료 보고서 작성 완료.
