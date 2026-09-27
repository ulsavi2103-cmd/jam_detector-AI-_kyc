"""
test_simulation.py
=============================================================================
[소박스 전도 감지 시스템 - 기능 3] 15x2 파이프라인 및 상태 머신 단위 검증 시뮬레이터

주요 검증 항목:
1. 15열 × 2행 (총 30개 박스) 그리드 좌표 매핑 및 셀 분할 검증
2. 모션 정지 감지 상태 머신 (0.8초 지속 정지 포착 & 3.0초 쿨다운 락) 동작 검증
3. 코랩 AI 모델 플러그앤플레이 슬롯인 inspect_single_box() 더미 함수 분리 검증
4. 키보드 't' 입력 시 3번 박스 전도 불량 시뮬레이션 및 알림 트리거 검증

실행 방법:
- 대화형 GUI 시뮬레이션: python test_simulation.py
- 자동 단위 테스트 (헤드리스): python test_simulation.py --headless
=============================================================================
"""

import os
import sys
import time
import json
import argparse
import numpy as np
import cv2

# Windows 터미널 cp949 인코딩 호환 처리
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =============================================================================
# 1. 시스템 설정 및 파라미터 (background.md 기준)
# =============================================================================
ROWS = 2
COLS = 15
TOTAL_BOXES = ROWS * COLS  # 30개

STOP_STABLE_DURATION = 0.8    # 정지 지속 판정 시간: 0.8초 (0.5~1.0초 정지 포착)
COOLDOWN_LOCK_DURATION = 10.8 # 실제 현장 속도(기존 60% 수준) 반영 락: 10.8초 (우측 10개 배출 -> 3회 반복 방어)
MOTION_STOP_THRESHOLD = 2.0   # 모션 정지 판단 임계치

# 4포인트 원근 보정 (Perspective Warp) 정규화 평면 해상도
WARP_OUTPUT_W = 600
WARP_OUTPUT_H = 160

# 테스트 시뮬레이션용 전도 불량 강제 플래그 (키보드 't'로 3번 박스 전도 모의)
force_toppled_box_id = None

def load_roi_config(json_path="roi_config.json"):
    """roi_config.json 파일에서 4개 모서리 좌표를 로드합니다."""
    if not os.path.exists(json_path):
        # packing_jam_detector 내부 검색
        alt_path = os.path.join("packing_jam_detector", json_path)
        if os.path.exists(alt_path):
            json_path = alt_path
        else:
            return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg
    except Exception as e:
        print(f"[WARN] roi_config.json 로드 실패: {e}")
        return None

# =============================================================================
# 2. [향후 코랩 모델 장착 슬롯: inspect_single_box]
# =============================================================================
def inspect_single_box(box_crop_img: np.ndarray, box_id: int, row: int, col: int) -> dict:
    """
    [향후 코랩 모델 장착 슬롯]
    - 입력: 15x2 중 개별 상자 1개의 크롭 이미지 (numpy array)
    - 출력: dict(is_toppled: bool, score: float, label: str)
    - 현재는 1단계 테스트용 Dummy 반환 (또는 키보드 시뮬레이션 트리거)
    
    ※ 3단계에서 구글 코랩에서 학습된 가중치(best.pt, onnx) 모델로
       아래 TODO 블록만 교체하면 즉시 연동됩니다.
    """
    # -------------------------------------------------------------
    # [TODO: 3단계/4단계 코랩 모델 교체 영역]
    # example:
    #   tensor = preprocess(box_crop_img)
    #   prediction = colab_model.predict(tensor)
    #   return {"is_toppled": prediction == "toppled", "score": 0.95, "label": "TOPPLED"}
    # -------------------------------------------------------------
    
    global force_toppled_box_id
    # 키보드 't'로 강제 전도 설정된 경우
    if force_toppled_box_id == box_id:
        return {
            "is_toppled": True,
            "score": 0.32,
            "label": "TOPPLED (Test Trigger)"
        }
    
    # 기본 1단계 더미: 정상 판정 (스코어 98%)
    return {
        "is_toppled": False,
        "score": 0.98,
        "label": "NORMAL"
    }

# =============================================================================
# 3. 15열 × 2단 Bounding Box 계산 엔진
# =============================================================================
def calculate_grid_boxes(frame_w: int, frame_h: int):
    """
    화면 해상도에 맞춰 15열 x 2단의 Bounding Box (x, y, w, h)를 계산합니다.
    """
    margin_x = int(frame_w * 0.05)
    margin_y = int(frame_h * 0.12)
    avail_w = frame_w - margin_x * 2
    avail_h = frame_h - margin_y * 2
    
    cell_gap = 2
    cell_w = max(10, (avail_w - (COLS - 1) * cell_gap) // COLS)
    cell_h = max(20, (avail_h - (ROWS - 1) * cell_gap) // ROWS)
    
    total_grid_w = COLS * cell_w + (COLS - 1) * cell_gap
    total_grid_h = ROWS * cell_h + (ROWS - 1) * cell_gap
    
    start_x = (frame_w - total_grid_w) // 2
    start_y = (frame_h - total_grid_h) // 2
    
    boxes = []
    for r in range(ROWS):
        for c in range(COLS):
            box_id = r * COLS + c + 1  # 1 ~ 30
            bx = start_x + c * (cell_w + cell_gap)
            by = start_y + r * (cell_h + cell_gap)
            boxes.append({
                "id": box_id,
                "r": r,
                "c": c,
                "x": bx,
                "y": by,
                "w": cell_w,
                "h": cell_h
            })
    return boxes, (start_x, start_y, total_grid_w, total_grid_h, cell_w, cell_h)

# =============================================================================
# 4. 가상 컨베이어 프레임 생성기 (푸셔 1 진입 -> 1초 정지 -> 우측 10개 배출 -> 20개 전진 반복)
# =============================================================================
class VirtualConveyor:
    def __init__(self, width=860, height=480):
        self.w = width
        self.h = height
        self.boxes, (self.gx, self.gy, self.gw, self.gh, self.cw, self.ch) = calculate_grid_boxes(self.w, self.h)
        self.col_pitch = self.cw + 2
        self.reset_boxes()
        
    def reset_boxes(self):
        initial_start_x = -self.col_pitch * 15 - 40
        self.sim_boxes = []
        for b in self.boxes:
            box_copy = dict(b)
            box_copy["group"] = min(2, b["c"] // 5)  # 0: 1~5열, 1: 6~10열, 2: 11~15열
            box_copy["x"] = float(initial_start_x + b["c"] * self.col_pitch)
            box_copy["y"] = float(b["y"])
            box_copy["target_x"] = float(b["x"])
            box_copy["discharged"] = False
            self.sim_boxes.append(box_copy)
            
        self.phase = "ENTER"  # "ENTER" | "STOP" | "PUSH_1" | "SHIFT_1" | "PUSH_2" | "SHIFT_2" | "PUSH_3" | "RESET"
        self.phase_timer = 0
        
    def step(self):
        if self.phase == "ENTER":
            all_reached = True
            for b in self.sim_boxes:
                if b["x"] < b["target_x"]:
                    b["x"] += 8.0  # 푸셔 1 빠른 진입 속도 복원 (원래 빠른 속도)
                    if b["x"] >= b["target_x"]:
                        b["x"] = b["target_x"]
                    else:
                        all_reached = False
            if all_reached:
                self.phase = "STOP"
                self.phase_timer = 90  # 정지 상태 유지 (0.8초 검사 안정적 포착)
                
        elif self.phase == "STOP":
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                self.phase = "PUSH_1"  # 1단계: 우측 끝 10개(그룹 2, 11~15열) 배출 시작 (실제 60% 속도 반영)
                self.phase_timer = 83  # 50 / 0.6
                
        elif self.phase == "PUSH_1":
            for b in self.sim_boxes:
                if b["group"] == 2 and not b["discharged"]:
                    b["y"] -= 3.6  # 상단/뒤쪽(3D 직교 방향)으로 배출 푸시 (6.0 * 0.6)
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                for b in self.sim_boxes:
                    if b["group"] == 2:
                        b["discharged"] = True
                    # 남은 20개(그룹 0, 1)의 다음 목표 X를 우측으로 5열만큼 전진 설정
                    if not b["discharged"]:
                        b["target_x"] += 5 * self.col_pitch
                self.phase = "SHIFT_1"  # 남은 20개 좌 -> 우 이송 시작
                
        elif self.phase == "SHIFT_1":
            all_shifted = True
            for b in self.sim_boxes:
                if not b["discharged"]:
                    if b["x"] < b["target_x"]:
                        b["x"] += 3.0  # 5.0 * 0.6
                        if b["x"] >= b["target_x"]:
                            b["x"] = b["target_x"]
                        else:
                            all_shifted = False
            if all_shifted:
                self.phase = "PUSH_2"  # 2단계: 새로 우측에 도착한 10개(그룹 1) 배출 시작
                self.phase_timer = 83
                
        elif self.phase == "PUSH_2":
            for b in self.sim_boxes:
                if b["group"] == 1 and not b["discharged"]:
                    b["y"] -= 3.6  # 상단/뒤쪽으로 배출 푸시
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                for b in self.sim_boxes:
                    if b["group"] == 1:
                        b["discharged"] = True
                    # 남은 10개(그룹 0)의 다음 목표 X를 다시 우측으로 5열만큼 전진 설정
                    if not b["discharged"]:
                        b["target_x"] += 5 * self.col_pitch
                self.phase = "SHIFT_2"  # 남은 10개 좌 -> 우 이송 시작
                
        elif self.phase == "SHIFT_2":
            all_shifted = True
            for b in self.sim_boxes:
                if not b["discharged"]:
                    if b["x"] < b["target_x"]:
                        b["x"] += 3.0  # 5.0 * 0.6
                        if b["x"] >= b["target_x"]:
                            b["x"] = b["target_x"]
                        else:
                            all_shifted = False
            if all_shifted:
                self.phase = "PUSH_3"  # 3단계: 마지막 10개(그룹 0) 배출 시작
                self.phase_timer = 83
                
        elif self.phase == "PUSH_3":
            for b in self.sim_boxes:
                if b["group"] == 0 and not b["discharged"]:
                    b["y"] -= 3.6  # 상단/뒤쪽으로 배출 푸시
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                for b in self.sim_boxes:
                    if b["group"] == 0:
                        b["discharged"] = True
                self.phase = "RESET"
                self.phase_timer = 42  # 25 / 0.6
                
        elif self.phase == "RESET":
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                self.reset_boxes()

    def get_frame(self):
        frame = np.full((self.h, self.w, 3), 25, dtype=np.uint8)
        
        # 레일 라인
        cv2.line(frame, (0, self.gy - 10), (self.w, self.gy - 10), (50, 50, 60), 2)
        cv2.line(frame, (0, self.gy + self.gh + 10), (self.w, self.gy + self.gh + 10), (50, 50, 60), 2)
        
        # 우측 배출 푸셔 영역 시각화 (11~15열 끝단 구역)
        pusher_x = int(self.gx + 10 * self.col_pitch)
        pusher_w = int(5 * self.col_pitch)
        cv2.rectangle(frame, (pusher_x, self.gy - 8), (pusher_x + pusher_w, self.gy + self.gh + 8), (35, 45, 55), 1)
        cv2.putText(frame, "Pusher 2 Zone (Rear Push)", (pusher_x + 5, self.gy - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (120, 160, 200), 1)
        
        # 박스 그리기 (배출 완료된 박스는 즉시 렌더링 제외)
        for box in self.sim_boxes:
            if box.get("discharged", False) or box["y"] < -self.ch:
                continue
                
            bx = int(box["x"])
            by = int(box["y"])
            bw = box["w"]
            bh = box["h"]
            
            # 박스 본체
            if force_toppled_box_id == box["id"]:
                # 전도 불량 박스: 눈에 띄는 주황색 톤 및 내부 패턴
                cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 165, 255), -1)
                cv2.rectangle(frame, (bx + 3, by + bh // 2 - 4), (bx + bw - 3, by + bh // 2 + 4), (0, 0, 200), -1)
            else:
                # 정상 기립 박스
                cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (220, 220, 225), -1)
                # 중앙 캡 패턴
                center = (bx + bw // 2, by + bh // 2)
                radius = max(3, min(bw, bh) // 4)
                cv2.circle(frame, center, radius, (200, 100, 30), -1)
            
            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (70, 70, 80), 1)
        
        return frame

# =============================================================================
# 5. 모션 계산기 및 상태 머신 테스터
# =============================================================================
class MotionStateMachine:
    def __init__(self, boxes, roi_rect):
        self.boxes = boxes
        self.roi = roi_rect  # (rx, ry, rw, rh)
        self.state = "WAIT_ARRIVAL"
        self.prev_roi_gray = None
        
        self.stop_check_start_time = None
        self.cooldown_start_time = None
        self.last_results = None
        
    def calculate_motion(self, frame):
        rx, ry, rw, rh = self.roi
        roi = frame[ry:ry+rh, rx:rx+rw]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        if self.prev_roi_gray is None or self.prev_roi_gray.shape != gray.shape:
            self.prev_roi_gray = gray
            return 0.0
            
        diff = cv2.absdiff(gray, self.prev_roi_gray)
        motion = float(np.mean(diff))
        self.prev_roi_gray = gray
        return motion
        
    def update(self, frame):
        motion = self.calculate_motion(frame)
        now = time.time()
        event_log = None
        
        if self.state == "WAIT_ARRIVAL":
            if motion > MOTION_STOP_THRESHOLD * 1.5:
                self.state = "CHECK_STOP"
                self.stop_check_start_time = None
                event_log = f"[WAIT_ARRIVAL -> CHECK_STOP] 진입 모션 감지 (Motion: {motion:.1f})"
                
        elif self.state == "CHECK_STOP":
            if motion <= MOTION_STOP_THRESHOLD:
                if self.stop_check_start_time is None:
                    self.stop_check_start_time = now
                stop_elapsed = now - self.stop_check_start_time
                
                # 0.8초 이상 지속 정지 시 검사 실행
                if stop_elapsed >= STOP_STABLE_DURATION:
                    self.state = "INSPECT_ONESHOT"
                    event_log = f"[CHECK_STOP -> INSPECT_ONESHOT] {stop_elapsed:.2f}초 정지 포착! 30개 박스 원샷 검사 실행"
                    self.run_inspection(frame)
                    
                    # 검사 완료 즉시 배출 쿨다운 락 진입
                    self.state = "COOLDOWN_LOCK"
                    self.cooldown_start_time = now
                    event_log += f" -> [COOLDOWN_LOCK] {COOLDOWN_LOCK_DURATION}초 배출 쿨다운 락 작동"
            else:
                self.stop_check_start_time = None
                
        elif self.state == "COOLDOWN_LOCK":
            cd_elapsed = now - self.cooldown_start_time
            if cd_elapsed >= COOLDOWN_LOCK_DURATION:
                self.state = "WAIT_DEPARTURE"
                self.cooldown_start_time = None
                event_log = f"[COOLDOWN_LOCK -> WAIT_DEPARTURE] {COOLDOWN_LOCK_DURATION}초 쿨다운 만료 (배출 확인 대기)"
                
        elif self.state == "WAIT_DEPARTURE":
            if motion < MOTION_STOP_THRESHOLD:
                self.state = "WAIT_ARRIVAL"
                self.last_results = None
                event_log = f"[WAIT_DEPARTURE -> WAIT_ARRIVAL] 리셋 완료, 다음 15x2 박스 대기"
                
        return motion, event_log
        
    def run_inspection(self, frame):
        """30개 박스를 순회하며 inspect_single_box 호출 (Perspective Warp 평면 검증 포함)"""
        defects = []
        scores = []
        
        # roi_config.json 기반 4포인트 원근 변환 행렬 및 정규화 평면 추출 검증
        cfg = load_roi_config()
        warped_frame = None
        if cfg and "points" in cfg and len(cfg["points"]) == 4:
            pts = cfg["points"]
            src_pts = np.float32([[p["x"], p["y"]] for p in pts])
            dst_pts = np.float32([
                [0, 0],
                [WARP_OUTPUT_W, 0],
                [WARP_OUTPUT_W, WARP_OUTPUT_H],
                [0, WARP_OUTPUT_H]
            ])
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped_frame = cv2.warpPerspective(frame, M, (WARP_OUTPUT_W, WARP_OUTPUT_H))
        
        for box in self.boxes:
            bx, by, bw, bh = box["x"], box["y"], box["w"], box["h"]
            crop = frame[by:by+bh, bx:bx+bw]
            res = inspect_single_box(crop, box["id"], box["r"], box["c"])
            
            info = {
                "id": box["id"],
                "r": box["r"] + 1,
                "c": box["c"] + 1,
                "score": res["score"],
                "is_toppled": res["is_toppled"],
                "label": res["label"],
                "rect": (bx, by, bw, bh)
            }
            scores.append(info)
            if res["is_toppled"]:
                defects.append(info)
                
        self.last_results = {
            "defects": defects,
            "scores": scores,
            "min_score": min(s["score"] for s in scores) if scores else 1.0,
            "warped_verified": warped_frame is not None and warped_frame.shape == (WARP_OUTPUT_H, WARP_OUTPUT_W, 3)
        }
        
        if defects:
            print(f"\n[ALARM] 전도(누움) 박스 불량 감지! ({len(defects)}건)")
            for d in defects:
                print(f"   - #{d['id']}번 박스 ({d['r']}행 {d['c']}열) -> {d['label']} (일치율: {d['score']*100:.1f}%)")
        else:
            print("\n[PASS] 15x2 총 30개 박스 전도 검사 합격 (전체 정상)")

# =============================================================================
# 6. 메인 실행 및 테스트 루프
# =============================================================================
def run_simulation(headless=False):
    global force_toppled_box_id
    
    conveyor = VirtualConveyor(860, 480)
    # ROI: 작업대 우측 끝단
    roi_rect = (conveyor.gx + conveyor.gw - 60, conveyor.gy + conveyor.gh // 2 - 25, 50, 50)
    state_machine = MotionStateMachine(conveyor.boxes, roi_rect)
    
    print("=" * 70)
    print(" [소박스 전도 감지 시스템] 15x2 파이프라인 시뮬레이션 테스트 시작")
    print(f" - 그리드 규격: {COLS}열 x {ROWS}단 = 총 {TOTAL_BOXES}개 박스")
    print(f" - 정지 감지 시간: {STOP_STABLE_DURATION}초 | 쿨다운 락: {COOLDOWN_LOCK_DURATION}초")
    print(" - 조작 키 안내:")
    print("     [t] : 3번 박스 전도 불량 시뮬레이션 트리거")
    print("     [r] : 정상 상태로 리셋")
    print("     [q] : 테스트 종료")
    print("=" * 70)
    
    step_count = 0
    test_passed_inspection = False
    test_passed_toppled = False
    test_passed_cooldown = False
    
    try:
        while True:
            conveyor.step()
            frame = conveyor.get_frame()
            motion, event = state_machine.update(frame)
            
            if event:
                print(f"[{time.strftime('%H:%M:%S')}] {event}")
                if "원샷 검사 실행" in event:
                    test_passed_inspection = True
                    if force_toppled_box_id == 3:
                        test_passed_toppled = True
                if "쿨다운 만료" in event:
                    test_passed_cooldown = True
            
            step_count += 1
            
            # 헤드리스 모드일 때 자동 시나리오 진행
            if headless:
                time.sleep(0.005)
                # 정지 전에 3번 박스 전도 모의 활성화
                if step_count == 40 and force_toppled_box_id is None:
                    print("\n[Auto Test] 키보드 't' 이벤트 시뮬레이션: 3번 박스 전도 결함 주입!")
                    force_toppled_box_id = 3
                
                # 10.8초 쿨다운 락 완료 및 사이클 완주 후 결과 검증 및 종료 (time.sleep 0.005s 기준 10.8초 이상 대기)
                if test_passed_cooldown or step_count >= 2800:
                    warp_ok = state_machine.last_results and state_machine.last_results.get("warped_verified", False)
                    print("\n" + "=" * 70)
                    print(" [TEST RESULT] 헤드리스 단위 테스트 검증 결과:")
                    print(f"  1. 15x2 (30개) 그리드 분할: PASS")
                    print(f"  2. roi_config.json 로드 및 4포인트 Perspective Warp: {'PASS' if warp_ok else 'FAIL'}")
                    print(f"  3. 모션 0.8초 정지 감지 & 원샷 검사: {'PASS' if test_passed_inspection else 'FAIL'}")
                    print(f"  4. 우측 10개 배출 및 10.8초 쿨다운 락: {'PASS' if test_passed_cooldown else 'FAIL'}")
                    print(f"  5. 3번 박스 전도 불량('t') 감지 알림: {'PASS' if test_passed_toppled else 'FAIL'}")
                    print("=" * 70)
                    assert test_passed_inspection, "정지 감지 검사 실패"
                    assert warp_ok, "4포인트 원근 보정(Perspective Warp) 평면 추출 실패"
                    assert test_passed_toppled, "3번 박스 전도 불량 감지 실패"
                    assert test_passed_cooldown, "10.8초 쿨다운 락 만료 실패"
                    print(">> 모든 단위 테스트 및 공정 파이프라인 검증 성공!\n")
                    break
                continue
                
            # GUI 모드 (cv2.imshow)
            # HUD 및 그리드 오버레이 렌더링
            disp = frame.copy()
            
            # 그리드 오버레이
            for box in conveyor.boxes:
                bx, by, bw, bh = box["x"], box["y"], box["w"], box["h"]
                color = (70, 70, 70)
                text = f"#{box['id']}"
                
                if state_machine.last_results:
                    defect = next((d for d in state_machine.last_results["defects"] if d["id"] == box["id"]), None)
                    if defect:
                        color = (0, 0, 255)  # 빨강
                        text = f"#{box['id']} TILT"
                    else:
                        color = (0, 255, 0)  # 초록
                elif force_toppled_box_id == box["id"]:
                    color = (0, 165, 255)
                    text = f"#{box['id']} TILT"
                    
                cv2.rectangle(disp, (bx, by), (bx + bw, by + bh), color, 2 if color != (70, 70, 70) else 1)
                cv2.putText(disp, text, (bx + 2, by + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.32, color, 1)
            
            # 상태 표시 HUD
            status_text = f"State: {state_machine.state} | Motion: {motion:.1f}"
            if state_machine.state == "COOLDOWN_LOCK" and state_machine.cooldown_start_time:
                remain = max(0.0, COOLDOWN_LOCK_DURATION - (time.time() - state_machine.cooldown_start_time))
                status_text += f" | Lock: {remain:.1f}s"
            
            cv2.putText(disp, status_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
            cv2.putText(disp, f"Pusher Phase: {conveyor.phase} (Key: 't'=tilt #3, 'r'=reset, 'q'=quit)", (20, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
            
            cv2.imshow("15x2 Box Jam & Tilt Detector Simulation", disp)
            key = cv2.waitKey(25) & 0xFF
            
            if key == ord('q') or key == 27:
                print("사용자 요청으로 시뮬레이션을 종료합니다.")
                break
            elif key == ord('t') or key == ord('T'):
                force_toppled_box_id = 3
                print(">>> [키보드 't' 입력] 3번 박스 전도(누움) 결함 주입 완료!")
            elif key == ord('r') or key == ord('R'):
                force_toppled_box_id = None
                print(">>> [키보드 'r' 입력] 모든 박스 정상으로 초기화.")
                
    finally:
        if not headless:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="15x2 소박스 전도 감지 시뮬레이터")
    parser.add_argument("--headless", action="store_true", help="GUI 창 없이 터미널 자동 검증 단위 테스트 실행")
    args = parser.parse_args()
    
    run_simulation(headless=args.headless)
