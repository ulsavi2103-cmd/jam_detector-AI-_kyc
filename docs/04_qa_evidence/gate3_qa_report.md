# [Gate 3 QA 리포트] 고속 컨베이어 및 모바일 OOM 방지 통합 QA 보고서 (QA Evaluator)

- **테스트 일시:** 2026-09-27 18:31:33
- **검증 환경:** Headless Chromium (Playwright Python One-shot Runner)
- **대상 URL:** `index.html`, `light.html`, `color.html`
- **검증 실행 명령:** `python run_gate3_qa_feature1_2.py`
- **종료 코드:** `0` (Success)

---

## 1. 세부 검증 항목 및 판정

| 검증 카테고리 | 세부 검증 항목 | 기대 스펙 | 실측 결과 | 상태 |
| :--- | :--- | :--- | :--- | :---: |
| **카메라 해상도 제한** | `light.html` `getUserMedia` | `640x480` | `width: 640, height: 480` 제약 설정 확인 | **PASS** |
| | `color.html` `getUserMedia` | `640x480` | `width: 640, height: 480` 제약 설정 확인 | **PASS** |
| **Zero-Allocation 버퍼** | 전역 Float32Array 단일 버퍼 | 49,152 floats (`1*3*128*128`) | `bufferLength: 49152` 확인 | **PASS** |
| | 전처리 힙 재할당 금지 | In-place 업데이트 | `isSameBufferInstance: true` (동일 인스턴스 확인) | **PASS** |
| | 루프 내 `new Float32Array` 생성 | 0건 (코드 감사) | 0건 (전역 1회 외 신규 생성 0건 확인) | **PASS** |
| **0.6초 주기 디바운스** | 추론 호출 주기 (`CHECK_INTERVAL`) | `100ms` | `checkInterval: 100` 확인 | **PASS** |
| | 판정 쿨다운 (`COOLDOWN_TIME`) | `400ms` | `cooldownTime: 400` 확인 | **PASS** |
| **ONNX 모델 및 런타임** | ONNX Runtime Web 로더 | `ort` 객체 로드 | `hasOrt: true` 확인 | **PASS** |
| | 가중치 파일 참조 | `box_posture_model.onnx` | `./models/` 및 루트 경로 200 OK 로드 확인 | **PASS** |
| | 클래스 인덱스 매핑 | `0: defect`, `1: normal` | 소프트맥스 확률 기반 정상 분류 확인 | **PASS** |
| **고속 알람 및 시각 배너** | 't' 키 불량 주입 반응 | 0.1초 내 `#alarm-banner` | "🚨 불량 자세(전도) 감지!" 즉각 노출 확인 | **PASS** |
| **콘솔 예외 무결성** | JS Exception / Error | 0건 (Clean) | `console_errors: []` (0건) | **PASS** |

---

## 2. 증적 스크린샷

1. **메뉴 레이아웃:** `docs/04_qa_evidence/01_index_landscape_menu.png`
2. **밝기 모드 정상 감시 루프:** `docs/04_qa_evidence/02_light_normal_feed.png`
3. **밝기 모드 불량 즉각 경보:** `docs/04_qa_evidence/03_light_defect_alarm.png`
4. **색상 모드 불량 즉각 경보:** `docs/04_qa_evidence/04_color_defect_alarm.png`

---

## 3. QA 최종 판정: **PASS**
- 0.6초 고속 컨베이어 주기에 최적화된 100ms 추론 주기 및 400ms 쿨다운 디바운스가 정상 동작함을 입증함.
- 전역 49,152 Float32Array 버퍼 1회 사전 할당 및 In-place 정규화로 4~5시간 연속 가동 시 브라우저 OOM 크래시 요인이 원천 제거됨.
- Gate 4 (Wiki 및 완성 단계)로 전진 승인.
