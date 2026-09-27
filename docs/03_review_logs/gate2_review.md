# [Gate 2 리뷰] 고속 컨베이어 및 모바일 OOM 방지 리팩토링 교차 심사 (Reviewer)

- **검토 일시:** 2026-09-27 18:31
- **검토 대상:** `light.html`, `color.html`, `docs/02_todo.md`
- **검토 기준:**
  1. 카메라 해상도 제한 (640x480)
  2. Buffer Zero-Allocation (Float32Array 49,152 고정 버퍼 In-place, ImageNet NCHW 정규화)
  3. 0.6초 주기 대응 `CHECK_INTERVAL = 100ms`, `COOLDOWN_TIME = 400ms` 디바운스
  4. ONNX 모델 경로(`box_posture_model.onnx`), 클래스 매핑(`0: defect`, `1: normal`), `ort` WASM 프로바이더 적용

## 1. 코드 변경 사항 대조 심사 (Diff Audit)

1. **카메라 해상도 제한 (`getUserMedia`):**
   - `light.html` 및 `color.html` 모두 최우선 constraints 객체에 `width: { ideal: 640 }, height: { ideal: 480 }`가 정확히 설정됨.
   - 모바일 기기의 고해상도(FHD/4K) 입력으로 인한 다운스케일링 연산 렉 및 기기 발열 요인이 원천 차단됨.

2. **메모리 누수 방지 (Buffer Zero-Allocation):**
   - 전처리 함수 내부에서 매 루프마다 `new Float32Array()`를 생성하던 GC 유발 요인이 제거됨.
   - 전역 스코프에 `const inputTensorBuffer = new Float32Array(1 * 3 * 128 * 128);` (49,152 floats) 1개만 할당.
   - 단일 `prepCanvas`와 `prepCtx`를 재사용하여 In-place로 버퍼 값을 갱신.
   - 정규화 공식 검증: ImageNet Mean `[0.485, 0.456, 0.406]`, Std `[0.229, 0.224, 0.225]` 및 NCHW(R-G-B 채널 분리) 레이아웃 순서가 엄격히 준수됨.

3. **고속 통과(0.6초) 추론 주기 및 중복 방지(Debounce):**
   - 제품 유효 화면 체류 시간(약 200~300ms)을 놓치지 않도록 `CHECK_INTERVAL = 100` (100ms) 설정 확인.
   - 판정 발생 시 `COOLDOWN_TIME = 400` (400ms) 동안 `isCooldown = true`로 잠금 플래그를 두어 제품당 1회만 카운트 및 알람 처리 확인.
   - 0.6초 주기로 다음 제품 도달 시점에는 400ms 쿨다운이 자동 해제되어 연속 검사 무결성이 보장됨.

4. **모델 파라미터 및 런타임 점검:**
   - CDN을 통한 `ort.min.js` 탑재 및 `models/box_posture_model.onnx` (루트 `box_posture_model.onnx` 폴백 포함) 참조 확인.
   - 모바일 안정성을 위한 `executionProviders: ['wasm']` 우선 적용 확인.
   - 모델 출력 텐서의 소프트맥스 결과 기준 `0: defect` (자세 불량), `1: normal` (정상 직립) 인덱스 매핑 확인.
   - 모델 미로드 시에도 가상 컨베이어 및 테스트 모드가 안전하게 동작하는 Fallback 안전망 구비 확인.

## 2. 부작용 및 안정성 평가
- 스마트폰 4~5시간 연속 가동 시 힙 메모리 급증(OOM Crash)의 핵심 원인이 완전히 제거됨.
- 기존 가로형 16:9 반응형 UI, 터치 ROI 드래그 좌표계, 비프음 사운드 경보 파이프라인의 기존 동작 흐름이 100% 보존됨.

## 3. 최종 판정
- **판정 신호:** **PASS**
- **조치 사항:** Gate 3 (원샷 통합 QA 단계)로 즉시 전진 승인.
