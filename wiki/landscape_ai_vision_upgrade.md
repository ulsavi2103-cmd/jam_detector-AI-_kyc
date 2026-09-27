# 컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처

## 1. 개요 및 설계 의도
* **고속 컨베이어 라인(0.6초 주기):**
  * 제품 1개당 카메라 유효 시야 내 체류 시간이 약 200~300ms인 초고속 이송 환경.
  * 진입 순간을 놓치지 않도록 **100ms 추론 주기(`CHECK_INTERVAL = 100`)**와 동일 제품 중복 카운트/알람을 방지하는 **400ms 판정 쿨다운 잠금(`COOLDOWN_TIME = 400`)** 디바운스 메커니즘 구축.
* **스마트폰 4~5시간 연속 운용 안정성:**
  * **해상도 제한:** `getUserMedia` 비디오 스트림을 640x480으로 제한하여 기기 발열 및 4K/FHD 다운스케일링 렉 원천 차단.
  * **Buffer Zero-Allocation:** 전처리 루프에서 `new Float32Array`를 신규 생성하지 않고, 전역에 고정된 1개 버퍼(`Float32Array(1 * 3 * 128 * 128) = 49,152 floats`)에 In-place로 덮어써 가비지 컬렉터(GC) 부하 및 브라우저 OOM 크래시 방지.
  * **ONNX Runtime Web WASM 표준화:** `ort.InferenceSession.create('models/box_posture_model.onnx', { executionProviders: ['wasm'] })` 연동 및 클래스 인덱스 매핑(`0: defect`, `1: normal`) 체계화.

---

## 2. 실시간 AI 비전 파이프라인

```mermaid
flowchart TD
    Cam[스마트폰 카메라 / 가상 컨베이어 (640x480)] --> CheckInt[100ms 주기 검사 루프 (CHECK_INTERVAL)]
    CheckInt --> Detect[Trigger ROI 통과선 진입 감지]
    
    Detect --> CooldownCheck{쿨다운 상태인가? (COOLDOWN_TIME=400ms)}
    CooldownCheck -- 예 (중복 방지) --> Skip[판정 건너뜀 (동일 제품 1회 판정 보장)]
    CooldownCheck -- 아니오 --> ZeroAlloc[Zero-Allocation 전처리 (In-place NCHW)]
    
    ZeroAlloc --> Model[ONNX Runtime Web WASM (box_posture_model.onnx)]
    Model --> Softmax[클래스 확률 산출 (0: defect, 1: normal)]
    
    Softmax --> Decision{0: defect vs 1: normal}
    Decision -- 0: defect (불량) --> Alarm[0.1초 즉시 경보 (사운드 비프음 + 붉은색 플래시)]
    Decision -- 1: normal (정상) --> Log[정상 통과 실시간 카운트/로그 기록]
    
    Alarm --> Lock[400ms 쿨다운 잠금 활성화]
    Log --> Lock
    Lock --> Next[0.6초 후 다음 제품 도착 시 자동 잠금 해제]
```

---

## 3. 핵심 모듈 및 구현 규격

### 3.1 카메라 해상도 제한 (`getUserMedia`)
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

### 3.2 Buffer Zero-Allocation 및 ImageNet NCHW 전처리
```javascript
// 전역 스코프에 1회만 할당 (매 프레임 재할당 0건)
const inputTensorBuffer = new Float32Array(1 * 3 * 128 * 128); // 49,152 floats
const prepCanvas = document.createElement('canvas');
prepCanvas.width = 128; prepCanvas.height = 128;
const prepCtx = prepCanvas.getContext('2d', { willReadFrequently: true });

function preprocessCropToBuffer(source, cropX, cropY, cropW, cropH) {
  prepCtx.drawImage(source, cropX, cropY, cropW, cropH, 0, 0, 128, 128);
  const data = prepCtx.getImageData(0, 0, 128, 128).data;
  const pixels = 128 * 128;

  // NCHW 레이아웃 + ImageNet Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225]
  for (let i = 0; i < pixels; i++) {
    const px = i * 4;
    inputTensorBuffer[i] = (data[px] / 255.0 - 0.485) / 0.229;                // R
    inputTensorBuffer[pixels + i] = (data[px + 1] / 255.0 - 0.456) / 0.224;   // G
    inputTensorBuffer[pixels * 2 + i] = (data[px + 2] / 255.0 - 0.406) / 0.225; // B
  }
  return inputTensorBuffer;
}
```

### 3.3 0.6초 주기 대응 100ms 주기 / 400ms 디바운스 쿨다운
```javascript
const CHECK_INTERVAL = 100; // 추론 호출 주기 (100ms)
const COOLDOWN_TIME = 400;  // 판정 쿨다운 잠금 (400ms)

// 400ms 경과 시 쿨다운 해제
if (isCooldown && (now - lastJudgmentTime >= COOLDOWN_TIME)) {
  isCooldown = false;
}

if (isRunning && (now - lastCheckTime >= CHECK_INTERVAL)) {
  lastCheckTime = now;
  if (presentNow && !isCooldown && !isInferring) {
    isInferring = true;
    isCooldown = true;
    lastJudgmentTime = now;
    // 1회 판정 수행
  }
}
```

### 3.4 ONNX Runtime Web WASM 및 클래스 인덱스 매핑
* **가중치 파일:** `models/box_posture_model.onnx` (루트 `box_posture_model.onnx` 폴백).
* **엔진:** `ort.InferenceSession.create(MODEL_PATH, { executionProviders: ['wasm'] })`.
* **클래스 매핑:**
  * `0`: `DEFECT` (가로 누움/자세 전도 불량) ➔ 경보 발령
  * `1`: `NORMAL` (정상 직립 통과) ➔ 통과 수 카운트

---

## 4. 검증 및 테스트 가이드

### 4.1 원샷 자동화 통합 QA (Playwright)
```bash
python run_gate3_qa_feature1_2.py
```
* **검증 내용:** 10대 정적 코드 감사 + Chromium 브라우저 런타임 버퍼(49,152)/스펙/키보드 't' 불량 주입 및 0.1초 경보 발령 ALL PASS.

### 4.2 웹 애플리케이션 수동 실행
```bash
python -m http.server 8000
```
* 브라우저에서 `http://localhost:8000/` 접속 후 가로 모드로 1번(밝기) 또는 2번(색상) 검사기 선택.
* `🎮 가상 컨베이어 모드: ON` 버튼 클릭 후 `t` 키를 누르면 불량 상자 통과 및 실시간 경보가 동작함.
