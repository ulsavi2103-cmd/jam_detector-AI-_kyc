# 시스템 위키 색인 (Wiki Index)

## 기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)
- [가로 16:9 실시간 AI 자세/전도 검사기 아키텍처](landscape_ai_vision_upgrade.md)
  - 16:9 와이드 모바일 뷰 및 세로 모드 안내 오버레이
  - 1:1 역산 터치 ROI 좌표계 매핑 핸들러
  - 통과 즉시 0.05초 크롭 및 `inspect_box_posture()` 코랩 AI 연동 규격
  - 0.1초 내 붉은색 플래시 경고 및 Web Audio API 비프음 경보
  - Python OpenCV 가상 시뮬레이터 (`test_simulation_feature1_2.py`)

---

## 기능 3. 소박스 전도(누움) 감지 시스템 (비활성화)
- [4포인트 원근 보정(Perspective Warp) 및 ROI 설정 자동 저장](perspective_warp_calibration.md)
  - 대각선 앵글 사다리꼴 왜곡 보정 및 Bilinear 오버레이
  - OpenCV.js `cv.warpPerspective` 15x2 정규화 평면 추출
  - `roi_config.json` 및 `localStorage` 무설정 자동 복원
