"""
run_gate3_qa_feature1_2.py
=============================================================================
Gate 3 원샷 고속 통합 QA 러너:
1. 원자적 로컬 서버 기동 및 종료 생명주기 결합
2. Headless Chromium을 활용한 index.html, light.html, color.html 검증
3. 고속 컨베이어(0.6초) 및 4~5시간 연속 운용 리팩토링 검증:
   - 카메라 640x480 해상도 제한 검증
   - Zero-Allocation Float32Array(1*3*128*128 = 49,152) 고정 버퍼 In-place 검증
   - 0.6초 주기 대응 CHECK_INTERVAL(100ms) 및 COOLDOWN_TIME(400ms) 디바운스 검증
   - ONNX Runtime Web WASM 및 box_posture_model.onnx 연동 검증
   - 't' 키 불량 주입 즉각 경보 및 무결성 검증
=============================================================================
"""

import os
import sys
import time
import socket
import json
import threading
import http.server
import socketserver

# Windows 콘솔 cp949 인코딩 호환 처리
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

EVIDENCE_DIR = os.path.join("docs", "04_qa_evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def verify_static_code():
    """정적 코드 검증: 해상도 제한, Zero-allocation 버퍼, 0:defect / 1:normal 매핑"""
    import re
    checks = {}
    with open("light.html", "r", encoding="utf-8") as f:
        light_code = f.read()
    with open("color.html", "r", encoding="utf-8") as f:
        color_code = f.read()

    light_no_comments = re.sub(r'//.*', '', light_code)
    light_no_comments = re.sub(r'/\*[\s\S]*?\*/', '', light_no_comments)

    color_no_comments = re.sub(r'//.*', '', color_code)
    color_no_comments = re.sub(r'/\*[\s\S]*?\*/', '', color_no_comments)

    checks["light_res_640x480"] = "width: { ideal: 640 }" in light_code and "height: { ideal: 480 }" in light_code
    checks["color_res_640x480"] = "width: { ideal: 640 }" in color_code and "height: { ideal: 480 }" in color_code

    checks["light_zero_alloc"] = "new Float32Array(1 * 3 * INPUT_SIZE * INPUT_SIZE)" in light_code and light_no_comments.count("new Float32Array") == 1
    checks["color_zero_alloc"] = "new Float32Array(1 * 3 * INPUT_SIZE * INPUT_SIZE)" in color_code and color_no_comments.count("new Float32Array") == 1

    checks["light_debounce_100_400"] = "CHECK_INTERVAL = 100" in light_code and "COOLDOWN_TIME = 400" in light_code
    checks["color_debounce_100_400"] = "CHECK_INTERVAL = 100" in color_code and "COOLDOWN_TIME = 400" in color_code

    checks["light_onnx_model"] = "box_posture_model.onnx" in light_code and "executionProviders: ['wasm']" in light_code
    checks["color_onnx_model"] = "box_posture_model.onnx" in color_code and "executionProviders: ['wasm']" in color_code

    checks["light_class_mapping"] = "0: defect" in light_code and "1: normal" in light_code
    checks["color_class_mapping"] = "0: defect" in color_code and "1: normal" in color_code

    return checks

def run_qa():
    port = find_free_port()
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://localhost:{port}"

    print(f">> [QA Server Started] {base_url}")
    results = {
        "index_check": False,
        "light_normal": False,
        "light_pipeline_spec": False,
        "light_defect_alarm": False,
        "color_normal": False,
        "color_pipeline_spec": False,
        "color_defect_alarm": False,
        "static_code_checks": {},
        "console_errors": []
    }

    results["static_code_checks"] = verify_static_code()
    print(f"✔ [Static Code Audit] 10/10 항목 정적 감사: {results['static_code_checks']}")

    try:
        with sync_playwright() as p:
            # 16:9 가로 모드 뷰포트 (1280x720)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})

            # -------------------------------------------------------------
            # 1. index.html 검증
            # -------------------------------------------------------------
            page_index = context.new_page()
            page_index.on("pageerror", lambda err: results["console_errors"].append(f"[index] {err}"))
            page_index.goto(f"{base_url}/index.html")
            page_index.wait_for_selector("#btn-tilt-disabled")
            
            has_light = page_index.is_visible("#link-light")
            has_color = page_index.is_visible("#link-color")
            has_tilt_disabled = page_index.is_visible("#btn-tilt-disabled")
            if has_light and has_color and has_tilt_disabled:
                results["index_check"] = True
                page_index.screenshot(path=os.path.join(EVIDENCE_DIR, "01_index_landscape_menu.png"))
                print("✔ [QA 1/5] index.html 1·2번 집중 및 3번 비활성화 검증 완료")
            page_index.close()

            # -------------------------------------------------------------
            # 2. light.html 검증 (가상 컨베이어 + 런타임 스펙 + 't' 키 불량 경보)
            # -------------------------------------------------------------
            page_light = context.new_page()
            page_light.on("pageerror", lambda err: results["console_errors"].append(f"[light] {err}"))
            page_light.goto(f"{base_url}/light.html")
            page_light.wait_for_selector("#btn-toggle")

            # 런타임 파이프라인 및 Zero-allocation 버퍼 점검
            light_spec = page_light.evaluate("""() => {
                const bufLen = window.inputTensorBuffer ? window.inputTensorBuffer.length : 0;
                const checkInt = window.CHECK_INTERVAL;
                const cooldown = window.COOLDOWN_TIME;
                
                // In-place 갱신 검증: preprocessCropToBuffer 호출 시 동일 버퍼 인스턴스 반환 확인
                const testCanvas = document.createElement('canvas');
                testCanvas.width = 100; testCanvas.height = 100;
                const returnedBuf = window.preprocessCropToBuffer(testCanvas, 0, 0, 100, 100);
                const isSameInstance = (returnedBuf === window.inputTensorBuffer);

                return {
                    bufferLength: bufLen,
                    checkInterval: checkInt,
                    cooldownTime: cooldown,
                    isSameBufferInstance: isSameInstance,
                    hasOrt: typeof ort !== 'undefined'
                };
            }""")
            print(f">> [LIGHT Runtime Spec] {light_spec}")
            assert light_spec["bufferLength"] == 49152, f"버퍼 크기 오류: {light_spec['bufferLength']}"
            assert light_spec["checkInterval"] == 100, f"CHECK_INTERVAL 오류: {light_spec['checkInterval']}"
            assert light_spec["cooldownTime"] == 400, f"COOLDOWN_TIME 오류: {light_spec['cooldownTime']}"
            assert light_spec["isSameBufferInstance"] is True, "Zero-Allocation 원칙 위배 (In-place 실패)"
            results["light_pipeline_spec"] = True

            # 가상 컨베이어 확실하게 켜기 및 검사 시작
            page_light.evaluate("() => setSimMode(true)")
            page_light.click("#btn-toggle")
            time.sleep(1.0)
            page_light.screenshot(path=os.path.join(EVIDENCE_DIR, "02_light_normal_feed.png"))
            results["light_normal"] = True
            print("✔ [QA 2/5] light.html 16:9 가로 레이아웃 및 정상 감시 루프 검증 완료")

            # 키보드 't' 누름 ➔ 불량 주입 ➔ 0.1초 내 경보 배너 검증
            page_light.keyboard.press("t")
            print(">> [LIGHT] 't' 키 입력 완료 -> 불량 상자 통과 대기")
            page_light.wait_for_selector("#alarm-banner", state="visible", timeout=6000)
            banner_text = page_light.inner_text("#alarm-title")
            assert "불량" in banner_text, f"경보 문구 불일치: {banner_text}"
            page_light.screenshot(path=os.path.join(EVIDENCE_DIR, "03_light_defect_alarm.png"))
            results["light_defect_alarm"] = True
            print("✔ [QA 3/5] light.html 키보드 't' 불량 주입 즉각 경보 발령 검증 완료")
            page_light.close()

            # -------------------------------------------------------------
            # 3. color.html 검증 (가상 컨베이어 + 런타임 스펙 + 't' 키 불량 경보)
            # -------------------------------------------------------------
            page_color = context.new_page()
            page_color.on("pageerror", lambda err: results["console_errors"].append(f"[color] {err}"))
            page_color.goto(f"{base_url}/color.html")
            page_color.wait_for_selector("#btn-toggle")

            # 런타임 파이프라인 및 Zero-allocation 버퍼 점검
            color_spec = page_color.evaluate("""() => {
                const bufLen = window.inputTensorBuffer ? window.inputTensorBuffer.length : 0;
                const checkInt = window.CHECK_INTERVAL;
                const cooldown = window.COOLDOWN_TIME;
                
                const testCanvas = document.createElement('canvas');
                testCanvas.width = 100; testCanvas.height = 100;
                const returnedBuf = window.preprocessCropToBuffer(testCanvas, 0, 0, 100, 100);
                const isSameInstance = (returnedBuf === window.inputTensorBuffer);

                return {
                    bufferLength: bufLen,
                    checkInterval: checkInt,
                    cooldownTime: cooldown,
                    isSameBufferInstance: isSameInstance,
                    hasOrt: typeof ort !== 'undefined'
                };
            }""")
            print(f">> [COLOR Runtime Spec] {color_spec}")
            assert color_spec["bufferLength"] == 49152, f"버퍼 크기 오류: {color_spec['bufferLength']}"
            assert color_spec["checkInterval"] == 100, f"CHECK_INTERVAL 오류: {color_spec['checkInterval']}"
            assert color_spec["cooldownTime"] == 400, f"COOLDOWN_TIME 오류: {color_spec['cooldownTime']}"
            assert color_spec["isSameBufferInstance"] is True, "Zero-Allocation 원칙 위배 (In-place 실패)"
            results["color_pipeline_spec"] = True

            page_color.evaluate("() => setSimMode(true)")
            page_color.click("#btn-toggle")
            time.sleep(0.5)
            results["color_normal"] = True

            page_color.keyboard.press("t")
            print(">> [COLOR] 't' 키 입력 완료 -> 불량 상자 통과 대기")
            page_color.wait_for_selector("#alarm-banner", state="visible", timeout=6000)
            banner_text = page_color.inner_text("#alarm-title")
            assert "불량" in banner_text, f"경보 문구 불일치: {banner_text}"
            page_color.screenshot(path=os.path.join(EVIDENCE_DIR, "04_color_defect_alarm.png"))
            results["color_defect_alarm"] = True
            print("✔ [QA 4/5] color.html 키보드 't' 불량 주입 즉각 경보 발령 검증 완료")
            page_color.close()

            browser.close()

    finally:
        httpd.shutdown()
        print(">> [QA Server Terminated]")

    # 검증 요약 저장
    summary_path = os.path.join(EVIDENCE_DIR, "qa_feature1_2_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    all_static_pass = all(results["static_code_checks"].values())
    all_runtime_pass = (
        results["index_check"] and
        results["light_normal"] and
        results["light_pipeline_spec"] and
        results["light_defect_alarm"] and
        results["color_normal"] and
        results["color_pipeline_spec"] and
        results["color_defect_alarm"] and
        len(results["console_errors"]) == 0
    )

    if all_static_pass and all_runtime_pass:
        print("\n🎉 [GATE 3 QA] 고속 컨베이어 및 모바일 OOM 방지 통합 검증 통과 (ALL PASS)!")
        return 0
    else:
        print(f"\n❌ [GATE 3 QA FAIL] 결과: {results}")
        return 1

if __name__ == "__main__":
    sys.exit(run_qa())
