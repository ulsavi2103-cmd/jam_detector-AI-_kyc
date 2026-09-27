# [요구사항 명세서] 고속 컨베이어(0.6s) 및 4~5시간 연속 운용 최적화 비전 파이프라인 리팩토링

## 1. 개요 및 배경 (Background & Objective)
- **현장 운용 환경:**
  - 0.6초 주기로 제품이 빠르게 통과하는 고속 컨베이어 라인 (제품당 카메라 시야 내 유효 체류 시간: 약 200~300ms).
  - 스마트폰을 거치대에 고정하여 4~5시간 동안 중단 없이 실시간 검사를 수행하는 현장 환경.
- **기존 구조의 잠재적 리스크 및 개선 필요성:**
  1. **고해상도 입력에 의한 발열 및 렉:** 스마트폰 기본 카메라의 FHD/4K 스트림 유입 시 다운스케일링 부하로 인한 프레임 드랍 및 기기 과열 발생.
  2. **가비지 컬렉터(GC) 부하 및 OOM:** 매 프레임/추론마다 전처리 버퍼(`new Float32Array`)를 생성하면 4~5시간 가동 시 메모리 단편화 및 브라우저 크래시 유발.
  3. **고속 통과 제품의 누락 및 중복 카운팅:** 통과 순간(200~300ms)을 놓치지 않으면서 동일 제품에 대해 중복 알람/카운트가 발생하지 않도록 정밀한 디바운스/쿨다운 타이밍 필요.
  4. **ONNX 모델 연동 및 런타임 표준화:** 코랩에서 학습된 가중치(`box_posture_model.onnx`) 탑재 슬롯을 구체화하고, 모바일 WASM 런타임 및 클래스 매핑(0: defect, 1: normal)을 체계화.

---

## 2. 세부 기능 요구사항 (Functional Requirements)

### F-1. 카메라 해상도 제한 (`getUserMedia`)
- 비디오 스트림 제약 조건을 640x480으로 제한하여 다운스케일링 부하 및 발열 차단:
```javascript
const constraints = {
  video: {
    facingMode: { ideal: "environment" },
    width: { ideal: 640 },
    height: { ideal: 480 }
  },
  audio: false
};
```
- 모바일 디바이스 지원을 위한 폴백 체인 구성 유지.

### F-2. 메모리 누수 방지 (Buffer Zero-Allocation 전처리)
- 전처리 함수 내부에서 매 루프마다 `new Float32Array()`를 신규 생성하지 않고, 전역/모듈 스코프에 고정 버퍼 1개만 사전 할당:
  - 형상: `[1, 3, 128, 128]` (크기: 49,152개 원소)
  - `const inputTensorBuffer = new Float32Array(1 * 3 * 128 * 128);`
- NCHW 레이아웃 순서 준수 (R 평면 ➔ G 평면 ➔ B 평면).
- ImageNet 정규화 공식 엄격 적용:
  - Mean: `[0.485, 0.456, 0.406]`
  - Std: `[0.229, 0.224, 0.225]`
  - 수식: `buffer[idx] = (channel_val / 255.0 - mean) / std`

### F-3. 고속 통과(0.6초) 추론 주기 및 중복 방지(Debounce)
- 제품 유효 화면 체류 시간(200~300ms) 포착 및 중복 방지:
  - 추론 호출 주기: `const CHECK_INTERVAL = 100;` (100ms)
  - 판정 쿨다운: `const COOLDOWN_TIME = 400;` (400ms)
- 판정 발생 시 쿨다운 플래그 활성화 ➔ 400ms 동안 추가 판정 잠금(Lock)을 통해 동일 제품당 1회만 카운트 및 알람 발령.
- 0.6초 후 다음 제품 도달 시점에는 쿨다운이 자동으로 해제되어 정상 검사 재개.

### F-4. 모델 파라미터 및 ONNX 런타임 규격
- 가중치 파일명: `box_posture_model.onnx` (기본 경로 `./models/box_posture_model.onnx` 및 `./box_posture_model.onnx` 참조).
- 클래스 인덱스 매핑: `0: defect` (자세 불량/전도), `1: normal` (정상 직립).
- ONNX Runtime Web 로더 탑재:
  - `ort.InferenceSession.create(modelPath, { executionProviders: ['wasm'] })` 우선 적용.
- 모델 파일 미로딩/네트워크 단절 시에도 가상 컨베이어 모드 및 테스트 모드가 안전하게 동작하도록 우아한 폴백(Graceful Fallback) 보장.

---

## 3. 검증 기준 (Acceptance Criteria)
1. **코드 정적 분석:**
   - `getUserMedia` 제약 조건 640x480 적용 여부.
   - 루프 내부 `new Float32Array` 미생성 및 전역 49,152 Float32 고정 버퍼 In-place 갱신 확인.
   - NCHW 순서 및 ImageNet mean/std 정규화 수식 일치 확인.
   - `CHECK_INTERVAL = 100`, `COOLDOWN_TIME = 400` 상수 및 디바운스 로직 검증.
   - `ort` WASM 프로바이더 및 0: defect, 1: normal 클래스 매핑 로직 확인.
2. **원샷 통합 QA:**
   - Headless 기반 `run_gate3_qa_feature1_2.py` 실행 시 ALL PASS 및 JS Exception 0건 유지.
