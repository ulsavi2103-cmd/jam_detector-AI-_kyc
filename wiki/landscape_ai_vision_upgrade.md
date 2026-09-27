# 컨베이어 16:9 와이드 광범위 AI 비전 파이프라인 아키텍처

## 1. 개요 및 설계 의도
* **16:9 와이드 광범위 촬영 보장 (향후 학습 데이터 수집 최적화):**
  * 카메라 제약 조건에 `aspectRatio: 1.777777778` 및 1280x720 / 640x360 16:9 표준 해상도 적용.
  * 컨베이어 라인의 넓은 좌우 이동 궤적을 왜곡이나 크롭 없이 100% 온전하게 카메라 센서로부터 직접 수집.
* **모바일 반응형 뷰포트 (세로/가로 모드 완벽 분기):**
  * **세로 모드(Portrait):** 상하 2분할(`flex-direction: column`). 상단에 가로 100% 꽉 차는 16:9 전폭 뷰포트(`aspect-ratio: 16 / 9`)를 배치하고 하단에 제어 패널 배치.
  * **가로 모드(Landscape):** 좌우 2분할(`flex-direction: row`). 화면 높이를 가득 채우는 16:9 뷰포트와 우측 슬림 사이드바(220px) 배치.
  * **화각 크롭 완전 차단:** `object-fit: contain` 적용으로 센서 비율 차이로 인한 영상 잘림 방지.
* **초고속 통과(0.6초 주기) 및 연속 운용 최적화 유지:**
  * **100ms 추론 주기 & 400ms 쿨다운 디바운스:** 제품 체류(200~300ms) 순간을 놓치지 않으면서 동일 제품 중복 카운트 방지.
  * **Buffer Zero-Allocation:** 전역 고정 버퍼(`Float32Array(49,152)`) 1개만 할당하여 4~5시간 연속 운용 시 OOM/GC 정지 원천 차단.
  * **ONNX Runtime Web WASM:** MobileNetV3 가중치(`0: defect`, `1: normal`) 실시간 추론 및 폴백 체계 결합.

---

## 2. 반응형 16:9 뷰포트 아키텍처

```mermaid
flowchart TD
    Device[디바이스 방향 감지] --> Branch{화면 오리엔테이션}
    
    Branch -- 세로 모드 (Portrait) --> ColLayout[상하 분할 (flex-direction: column)]
    ColLayout --> TopVP[상단 16:9 전폭 뷰포트 (100vw, aspect-ratio: 16/9)]
    TopVP --> Hint[🔄 가로 회전 권장 안내 펄스 배지 표시]
    ColLayout --> BottomCtrl[하단 조작 패널 (ROI 슬라이더 & 실시간 로그)]
    
    Branch -- 가로 모드 (Landscape) --> RowLayout[좌우 분할 (flex-direction: row)]
    RowLayout --> LeftVP[좌측 대화면 16:9 뷰포트 (최대화)]
    RowLayout --> RightSide[우측 슬림 사이드바 (220px)]
    
    TopVP --> StreamWrap[#stream-wrapper (aspect-ratio: 16/9, contain)]
    LeftVP --> StreamWrap
    StreamWrap --> CamOut[16:9 전체 화각 100% 무손실 노출]
```

---

## 3. 핵심 구현 사양

### 3.1 16:9 카메라 제약 조건 (`getUserMedia`)
```javascript
const constraints = {
  video: {
    facingMode: { ideal: "environment" },
    width: { ideal: 1280, min: 640 },
    height: { ideal: 720, min: 360 },
    aspectRatio: { ideal: 1.777777778 }
  },
  audio: false
};
```

### 3.2 16:9 종횡비 컨테이너 및 크롭 방지 CSS
```css
/* 16:9 와이드 종횡비 고정 래퍼 */
#stream-wrapper {
  position: relative;
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
  max-width: calc(100vh * (16 / 9));
  max-height: 100%;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 화각 잘림(crop) 원천 차단: 16:9 전체 화각 100% 노출 */
video, #sim-canvas {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

/* 모바일 세로 모드(Portrait) 반응형 분기 */
@media (max-width: 768px) and (orientation: portrait), (max-width: 600px) {
  #app-container { flex-direction: column !important; }
  #viewport-area {
    flex: none !important;
    width: 100vw !important;
    height: auto !important;
    aspect-ratio: 16 / 9 !important;
    max-height: 46vh !important;
  }
  #sidebar { flex: 1 !important; width: 100vw !important; overflow-y: auto !important; }
}
```

### 3.3 Zero-Allocation 전처리 및 디바운스
```javascript
const inputTensorBuffer = new Float32Array(1 * 3 * 128 * 128); // 49,152 floats 고정
const CHECK_INTERVAL = 100; // 100ms 추론 주기
const COOLDOWN_TIME = 400;  // 400ms 판정 쿨다운 (중복 방지)
```

---

## 4. 검증 결과
* **Playwright E2E 자동화 실측치:**
  * 모바일 세로(390x844): 종횡비 1.778 (16:9 일치), 상하 분할 정상 동작, 회전 안내 배지 노출.
  * 모바일 가로(844x390): 종횡비 1.778 (16:9 일치), 좌우 분할 정상 동작, 키보드/버튼 불량 주입 즉각 경보 발령.
  * 자바스크립트 콘솔 에러: 0건.
