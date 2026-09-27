# [요구사항 명세서] 모바일 거치대 안정성을 위한 경보 진동 제거 및 사운드 단일화

## 1. 개요 및 배경 (Background & Objective)
- **사용자 피드백 및 현장 요구:**
  - "진동의 경우에는 거치해둔 스마트폰의 상태를 변경되게 만드므로 삭제하라. 소리만 울리도록 코드를 수정하라."
- **문제점 분석:**
  - 컨베이어 벨트 상단/측면에 스마트폰을 삼각대, 마운트 클램프로 고정하여 장시간 비전 검사를 수행하는 현장 환경에서, 불량/정체 감지 시 스마트폰 기기 자체 진동(`navigator.vibrate`)이 발생하면 미세 진동으로 인해 거치대 위치 및 각도가 틀어지는 물리적 변위(Displacement)가 발생함.
  - 이로 인해 사전에 보정한 4포인트 원근(Perspective) 및 감지 구역(ROI) 좌표계가 어긋나 오탐 및 미탐의 원인이 됨.
- **개선 목표:**
  - `light.html` 및 `color.html`의 모든 경보 발령 루틴에서 기기 진동(`navigator.vibrate`) 코드를 영구 삭제.
  - 경보 출력 수단을 **고주파/이중톤 Web Audio API 사운드 비프음**과 **시각적 경고(플래시 배너, 상태 뱃지, 실시간 이력 로그)**로 단일화하여 물리적 거치 안정성을 100% 보장.

---

## 2. 세부 기능 요구사항 (Functional Requirements)

### F-1. 기기 물리 진동 로직 완전 제거
1. `light.html`의 `soundAlert()` 내부 `if ("vibrate" in navigator) navigator.vibrate(200);` 코드 전면 삭제.
2. `color.html`의 `soundAlert()` 내부 `if ("vibrate" in navigator) navigator.vibrate(200);` 코드 전면 삭제.
3. 코드베이스 전체에서 `navigator.vibrate` 호출 잔재가 0건임을 보장.

### F-2. 사운드 및 시각 경보 무결성 유지
1. Web Audio API를 활용한 sawtooth 파형 비프음(1400Hz ➔ 800Hz 스윕) 및 볼륨 증폭 로직 정상 동작 유지.
2. 불량(전도/각도이상) 및 잼(정체) 감지 시 붉은색 플래시 배너(#alarm-banner) 및 상태 뱃지 업데이트 정상 유지.

---

## 3. 검증 기준 (Acceptance Criteria)
1. 코드 정적 검증: 소스코드 전체 대상 `grep` 검색 시 `navigator.vibrate` 0건 확인.
2. 통합 QA: `python run_gate3_qa_feature1_2.py` 실행 시 콘솔 오류 0건 및 0.1초 경보 배너 정상 동작 (ALL PASS).
3. 거치 안정성: 불량 발생 시 물리적 진동 없이 사운드와 비주얼로만 경보 발령 확인.
