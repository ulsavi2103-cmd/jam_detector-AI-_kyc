# 컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처

## 1. 개요 및 설계 의도
* **전환 목적:** 
  * 기존 수 초 단위의 지연 시간을 갖는 '시간 누적 차영상 루프'를 폐기하고, 상자가 통과하는 순간 **0.05초 만에 자세 불량(가로 누움/비정상 회전)을 판별하는 실시간 AI 비전 검사기**로 전환.
  * 3번 기능(30개 박스 묶음 정지 감지)은 비활성화하고 1·2번 단품 통과 라인 검사기에 역량을 집중.
* **환경 기준:**
  * 가로(수평)로 길게 이어지는 컨베이어 라인 특성을 고려하여 **스마트폰 가로 모드(Landscape, 16:9 와이드)**를 기본 구동 규격으로 설정.
  * 세로 모드로 기기를 들었을 경우 `@media (orientation: portrait)` 안내 오버레이를 통해 기기 회전을 유도.

---

## 2. 핵심 아키텍처 파이프라인

```
[카메라 / 가상 컨베이어 스트림 (16:9)]
                 │
                 ▼
[Trigger ROI 통과선 모니터링]
  - 밝기 모드 (light.html): 휘도(Luma) 차분 진입 감지
  - 색상 모드 (color.html): RGB 및 에지 픽셀 델타 감지
                 │
                 ▼ (진입 포착: 0ms)
[ROI 구역 프레임 즉시 크롭 (Crop)]
                 │
                 ▼
[코랩 AI 플러그앤플레이 인터페이스: inspect_box_posture()]
  - Input: 통과 구역 크롭 캔버스/이미지
  - Output: { is_defect: bool, label: str, confidence: float }
  - 지연시간: < 0.05s
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
[정상 직립 (NORMAL)]   [가로 누움 불량 (TOPPLED)]
- 실시간 로그 기록       - 0.1초 내 붉은색 플래시 배너 발령
- 초록색 인디케이터      - Web Audio API 이중톤 비프음 경보
```

---

## 3. 주요 모듈 및 인터페이스 규격

### 3.1 코랩 학습 모델 슬롯 (`inspect_box_posture`)
```javascript
function inspect_box_posture(box_crop_canvas) {
  // [향후 구글 코랩 MobileNetV3 ONNX 모델 탑재 슬롯]
  if (window.testDefectTrigger) {
    window.testDefectTrigger = false;
    return { is_defect: true, label: "TOPPLED (가로 누움 불량)", confidence: 0.98 };
  }
  return { is_defect: false, label: "NORMAL (정상 직립)", confidence: 0.99 };
}
```

### 3.2 1:1 터치 좌표계 매핑
```javascript
function getTouchPos(e) {
  const rect = overlay.getBoundingClientRect();
  const scaleX = BASE_W / rect.width;
  const scaleY = BASE_H / rect.height;
  return {
    x: (clientX - rect.left) * scaleX,
    y: (clientY - rect.top) * scaleY
  };
}
```

---

## 4. 검증 및 테스트 가이드

### 4.1 가상 시뮬레이터 실행 (Python)
* **대화형 GUI 모드:**
  ```bash
  python test_simulation_feature1_2.py
  ```
  * 키 조작: `t` (가로 누움 불량 상자 주입), `q` (종료)
* **헤드리스 단위 테스트:**
  ```bash
  python test_simulation_feature1_2.py --headless
  ```

### 4.2 웹 애플리케이션 실행
* 로컬 HTTP 서버 실행:
  ```bash
  python -m http.server 8000
  ```
* 브라우저에서 `http://localhost:8000/` 접속 후 가로 모드로 1번(밝기) 또는 2번(색상) 검사기 선택.
* `🎮 가상 컨베이어 모드: ON` 버튼 클릭 후 `t` 키를 누르면 즉시 불량 주입 및 실시간 경보가 동작함.
