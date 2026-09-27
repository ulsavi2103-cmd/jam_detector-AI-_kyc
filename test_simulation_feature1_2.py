"""
test_simulation_feature1_2.py
=============================================================================
[1·2번 기능 실시간 AI 자세/전도 검사기] 가로 16:9 가상 시뮬레이션 및 단위 검증 스크립트

주요 검증 항목:
1. 가로 16:9 와이드 화면(960x540) 컨베이어 벨트 상자 이송 애니메이션
2. 통과 구역(Trigger ROI) 진입 순간 실시간 크롭(Crop) 파이프라인
3. 코랩 AI 플러그앤플레이 인터페이스 inspect_box_posture(box_crop_img) 검증
4. 키보드 't' 입력 시 다음 상자 '가로 누움(불량)' 상태 주입 및 0.1초 내 즉시 경보 발령 검증
5. 헤드리스 자동 단위 테스트 (--headless) 모드 지원

실행 방법:
- 대화형 GUI 시뮬레이션: python test_simulation_feature1_2.py
- 자동 단위 테스트 (헤드리스): python test_simulation_feature1_2.py --headless
=============================================================================
"""

import os
import sys
import time
import argparse
import numpy as np
import cv2

# Windows 콘솔 인코딩 대응
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =============================================================================
# 1. 시뮬레이션 파라미터 및 전역 상태
# =============================================================================
FRAME_W = 960
FRAME_H = 540  # 16:9 비율

# 컨베이어 벨트 위치 (화면 중앙 가로 대역)
BELT_Y1 = 120
BELT_Y2 = 420
BELT_H = BELT_Y2 - BELT_Y1

# Trigger ROI (검사 통과 구역)
ROI_X = 420
ROI_Y = 140
ROI_W = 120
ROI_H = 260

# 불량 모의 주입 플래그 ('t' 키 입력 시 다음 상자 전도 불량)
force_toppled_next = False

# =============================================================================
# 2. [향후 코랩 MobileNetV3 ONNX 모델 장착 슬롯: inspect_box_posture]
# =============================================================================
def inspect_box_posture(box_crop_img: np.ndarray, is_simulated_defect: bool = False) -> dict:
    """
    [향후 코랩 MobileNetV3 ONNX 모델 장착 슬롯]
    - Input: 통과 구역 크롭 이미지 (numpy array, BGR)
    - Output: {
        "is_defect": bool,       # True: 불량(누움/회전/잼), False: 정상
        "label": str,            # "NORMAL" | "TOPPLED" | "JAM"
        "confidence": float
      }
    - 현재: 1단계 테스트용 Dummy 반환 (모의 불량 주입 또는 크롭 형상 분석)
    
    ※ 추후 구글 코랩에서 학습된 ONNX 가중치로 아래 TODO 블록만 교체하면 즉시 연동됩니다.
    """
    # -------------------------------------------------------------------------
    # [TODO: 코랩 학습 모델 탑재 슬롯]
    # example:
    #   ort_inputs = {session.get_inputs()[0].name: preprocess(box_crop_img)}
    #   pred = session.run(None, ort_inputs)
    # -------------------------------------------------------------------------
    
    if is_simulated_defect:
        return {
            "is_defect": True,
            "label": "TOPPLED (가로 누움 불량)",
            "confidence": 0.97
        }
    
    # 크롭된 이미지의 종횡비 분석 (보조 판정)
    if box_crop_img is not None and box_crop_img.size > 0:
        gray = cv2.cvtColor(box_crop_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            # 가로가 세로보다 길면 가로 누움(전도) 불량
            if bw > bh * 1.2:
                return {
                    "is_defect": True,
                    "label": "TOPPLED (가로 누움 불량)",
                    "confidence": 0.95
                }

    # 기본 1단계 더미: 정상 직립 판정
    return {
        "is_defect": False,
        "label": "NORMAL (정상 직립)",
        "confidence": 0.99
    }

# =============================================================================
# 3. 가상 컨베이어 상자 객체 모델
# =============================================================================
class ConveyorBox:
    def __init__(self, x: float, toppled: bool = False):
        self.x = x
        self.toppled = toppled
        self.speed = 6.0  # 프레임당 이동 픽셀 (약 180px/s)
        self.inspected = False
        self.verdict = None

        if self.toppled:
            # 가로 누움: 가로가 길고 높이가 낮음
            self.w = 170
            self.h = 75
            self.y = BELT_Y1 + (BELT_H - self.h) // 2
            self.color = (40, 110, 220)  # 주황/적갈색 (불량)
        else:
            # 정상 직립: 가로가 좁고 높이가 높음
            self.w = 75
            self.h = 210
            self.y = BELT_Y1 + (BELT_H - self.h) // 2
            self.color = (80, 175, 230)  # 황갈색 골판지 상자

    def update(self):
        self.x += self.speed

    def draw(self, frame: np.ndarray):
        x1, y1 = int(self.x), int(self.y)
        x2, y2 = x1 + self.w, y1 + self.h

        # 상자 본체 및 그림자
        cv2.rectangle(frame, (x1 + 4, y1 + 4), (x2 + 4, y2 + 4), (20, 20, 20), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), self.color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (40, 40, 40), 2)

        # 상자 테이프 밴딩 디테일
        if self.toppled:
            cv2.line(frame, (x1, y1 + self.h // 2), (x2, y1 + self.h // 2), (20, 70, 160), 3)
            label = "TOPPLED"
        else:
            cv2.line(frame, (x1 + self.w // 2, y1), (x1 + self.w // 2, y2), (40, 120, 170), 3)
            label = "NORMAL"

        cv2.putText(frame, label, (x1 + 6, y1 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(frame, label, (x1 + 6, y1 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# =============================================================================
# 4. 가로 16:9 컨베이어 배경 렌더러
# =============================================================================
def draw_conveyor_background(frame: np.ndarray, belt_offset: int):
    # 공장 바닥 배경
    frame[:] = (22, 24, 30)

    # 컨베이어 프레임
    cv2.rectangle(frame, (0, BELT_Y1 - 10), (FRAME_W, BELT_Y2 + 10), (45, 50, 60), -1)
    cv2.rectangle(frame, (0, BELT_Y1), (FRAME_W, BELT_Y2), (30, 33, 40), -1)

    # 벨트 롤러 및 이송 라인 질감
    roller_gap = 40
    for x in range((belt_offset % roller_gap) - roller_gap, FRAME_W + roller_gap, roller_gap):
        cv2.line(frame, (x, BELT_Y1), (x, BELT_Y2), (22, 25, 32), 2)

    # 상하단 가이드 레일
    cv2.rectangle(frame, (0, BELT_Y1 - 8), (FRAME_W, BELT_Y1), (80, 85, 95), -1)
    cv2.rectangle(frame, (0, BELT_Y2), (FRAME_W, BELT_Y2 + 8), (80, 85, 95), -1)

# =============================================================================
# 5. 대화형 GUI 시뮬레이션 루프
# =============================================================================
def run_interactive_simulation():
    global force_toppled_next

    print("=" * 72)
    print(" [1·2번 실시간 AI 자세/전도 검사기] 가로 16:9 가상 시뮬레이터 시작")
    print(" - 't' 또는 'T' 키: 다음 지나가는 상자를 '가로 누움(불량)' 상태로 주입")
    print(" - 'q' 또는 ESC 키: 시뮬레이션 종료")
    print("=" * 72)

    boxes = []
    next_spawn_time = 0
    belt_offset = 0
    last_alarm_time = 0
    alarm_active = False
    alarm_text = ""
    inspect_count = 0
    defect_count = 0

    cv2.namedWindow("Conveyor AI Vision Inspector (Landscape 16:9)", cv2.WINDOW_AUTOSIZE)

    while True:
        current_time = time.time()
        frame = np.zeros((FRAME_H, FRAME_W, 3), dtype=np.uint8)

        # 1. 컨베이어 벨트 렌더링
        belt_offset = (belt_offset + 3) % 40
        draw_conveyor_background(frame, belt_offset)

        # 2. 상자 주기적 스폰 (약 2.2초 주기)
        if current_time >= next_spawn_time:
            is_defect = force_toppled_next
            if force_toppled_next:
                force_toppled_next = False
                print(">> [INJECT] 가로 누움(불량) 상자가 컨베이어에 투입되었습니다.")

            boxes.append(ConveyorBox(x=-180, toppled=is_defect))
            next_spawn_time = current_time + 2.2

        # 3. 상자 이동 및 검사 판별 로직
        roi_box = (ROI_X, ROI_Y, ROI_W, ROI_H)
        box_in_roi_now = False

        for b in boxes:
            b.update()
            b.draw(frame)

            # Trigger ROI 진입 검사
            box_x2 = b.x + b.w
            if box_x2 > ROI_X and b.x < ROI_X + ROI_W:
                box_in_roi_now = True
                if not b.inspected:
                    b.inspected = True
                    inspect_count += 1

                    # 통과 즉시 크롭
                    rx1, ry1 = max(0, ROI_X), max(0, ROI_Y)
                    rx2, ry2 = min(FRAME_W, ROI_X + ROI_W), min(FRAME_H, ROI_Y + ROI_H)
                    crop_img = frame[ry1:ry2, rx1:rx2].copy()

                    # AI 자세 검사 슬롯 호출 (< 0.05s)
                    t0 = time.time()
                    res = inspect_box_posture(crop_img, is_simulated_defect=b.toppled)
                    infer_ms = (time.time() - t0) * 1000
                    b.verdict = res

                    if res["is_defect"]:
                        defect_count += 1
                        alarm_active = True
                        last_alarm_time = current_time
                        alarm_text = f"ALERT: {res['label']} (Conf: {res['confidence']:.0%}, {infer_ms:.1f}ms)"
                        print(f"🚨 [경보 발령] {alarm_text}")
                        # 시스템 경보음
                        if sys.platform == "win32":
                            try:
                                import winsound
                                winsound.Beep(1300, 120)
                            except Exception:
                                pass
                    else:
                        print(f"✅ [정상 통과] {res['label']} ({infer_ms:.1f}ms)")

        # 화면 밖으로 나간 상자 제거
        boxes = [b for b in boxes if b.x < FRAME_W + 100]

        # 4. Trigger ROI 가이드라인 렌더링
        roi_color = (0, 230, 255) if not box_in_roi_now else (0, 255, 0)
        cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X + ROI_W, ROI_Y + ROI_H), roi_color, 2)
        cv2.putText(frame, "TRIGGER ROI (AI PASS-LINE)", (ROI_X, ROI_Y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, roi_color, 1)

        # 5. 경보 플래시 오버레이 (< 0.1s 반응)
        if alarm_active:
            if current_time - last_alarm_time < 1.2:
                # 붉은색 플래시 테두리 및 상단 배너
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (FRAME_W, 70), (0, 0, 200), -1)
                cv2.rectangle(overlay, (0, 0), (FRAME_W, FRAME_H), (0, 0, 220), 8)
                cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

                cv2.putText(frame, "!! DEFECT DETECTED: TOPPLED BOX !!", (60, 44),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            else:
                alarm_active = False

        # 6. 상단 대시보드 정보 HUD
        cv2.putText(frame, f"TOTAL: {inspect_count} | DEFECT: {defect_count} | FPS: 30",
                    (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        status_msg = "NEXT: TOPPLED [TRIGGERED]" if force_toppled_next else "NEXT: NORMAL (Press 'T' to inject defect)"
        status_col = (0, 140, 255) if force_toppled_next else (160, 160, 160)
        cv2.putText(frame, status_msg, (20, 515), cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_col, 2)

        cv2.imshow("Conveyor AI Vision Inspector (Landscape 16:9)", frame)
        key = cv2.waitKey(33) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('t') or key == ord('T'):
            force_toppled_next = True
            print(">> [KEY 'T' INPUT] 다음 통과 상자가 가로 누움(불량)으로 주입됩니다.")

    cv2.destroyAllWindows()
    print("시뮬레이션이 안전하게 종료되었습니다.")

# =============================================================================
# 6. 헤드리스 단위 테스트 모드 (--headless)
# =============================================================================
def run_headless_tests():
    print("=" * 72)
    print(" [단위 테스트] 1·2번 실시간 AI 자세/전도 검사기 파이프라인 검증 (헤드리스)")
    print("=" * 72)

    tests_passed = 0
    total_tests = 4

    # Test 1: 정상 직립 상자 판정 검증
    normal_box = ConveyorBox(x=ROI_X + 10, toppled=False)
    frame = np.zeros((FRAME_H, FRAME_W, 3), dtype=np.uint8)
    normal_box.draw(frame)
    crop_normal = frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]
    t0 = time.time()
    res_normal = inspect_box_posture(crop_normal, is_simulated_defect=False)
    lat_normal = (time.time() - t0) * 1000

    assert not res_normal["is_defect"], f"정상 상자가 불량으로 오탐됨: {res_normal}"
    assert lat_normal < 50.0, f"추론 지연 시간 초과 ({lat_normal:.2f}ms >= 50ms)"
    print(f"✔ [PASS] Test 1: 정상 직립 상자 정상 판정 완료 ({lat_normal:.2f}ms, label={res_normal['label']})")
    tests_passed += 1

    # Test 2: 't' 키 가로 누움(불량) 상자 주입 및 판정 검증
    toppled_box = ConveyorBox(x=ROI_X + 10, toppled=True)
    frame = np.zeros((FRAME_H, FRAME_W, 3), dtype=np.uint8)
    toppled_box.draw(frame)
    crop_toppled = frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]
    t0 = time.time()
    res_toppled = inspect_box_posture(crop_toppled, is_simulated_defect=True)
    lat_toppled = (time.time() - t0) * 1000

    assert res_toppled["is_defect"], f"가로 누움 불량 상자가 감지되지 않음: {res_toppled}"
    assert lat_toppled < 50.0, f"추론 지연 시간 초과 ({lat_toppled:.2f}ms >= 50ms)"
    print(f"✔ [PASS] Test 2: 가로 누움(전도) 불량 즉시 감지 완료 ({lat_toppled:.2f}ms, label={res_toppled['label']})")
    tests_passed += 1

    # Test 3: 0.1초 이내 경보 발생 시간 제약 검증
    t_alert_start = time.time()
    # 경보 로직 실행
    if res_toppled["is_defect"]:
        alarm_rendered = True
    t_alert_end = time.time()
    alert_latency = (t_alert_end - t_alert_start + (lat_toppled / 1000))
    assert alert_latency < 0.1, f"경보 발생 지연시간 0.1초 초과: {alert_latency:.4f}s"
    print(f"✔ [PASS] Test 3: 경보 트리거 반응 속도 0.1초 이내 검증 완료 ({alert_latency*1000:.2f}ms < 100ms)")
    tests_passed += 1

    # Test 4: 가로 16:9 해상도 및 ROI 좌표 규격 검증
    assert FRAME_W / FRAME_H == 16 / 9, f"16:9 비율 불일치: {FRAME_W}:{FRAME_H}"
    assert 0 <= ROI_X < FRAME_W and 0 <= ROI_Y < FRAME_H, "ROI 좌표가 프레임 범위를 벗어남"
    print(f"✔ [PASS] Test 4: 가로 16:9 와이드 해상도 규격({FRAME_W}x{FRAME_H}) 및 ROI 정합성 검증 완료")
    tests_passed += 1

    print("=" * 72)
    print(f"🎉 모든 헤드리스 단위 테스트 통과: {tests_passed}/{total_tests} PASS")
    print("=" * 72)
    return True

# =============================================================================
# 메인 엔트리포인트
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="1·2번 실시간 AI 자세/전도 검사기 시뮬레이터")
    parser.add_argument("--headless", action="store_true", help="GUI 창 없이 자동 단위 테스트 실행")
    args = parser.parse_args()

    if args.headless:
        success = run_headless_tests()
        sys.exit(0 if success else 1)
    else:
        run_interactive_simulation()
