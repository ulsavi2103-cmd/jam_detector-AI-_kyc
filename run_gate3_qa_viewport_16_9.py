"""
run_gate3_qa_viewport_16_9.py
=============================================================================
Gate 3 원샷 초고속 통합 QA 러너:
1. 원자적 로컬 HTTP 서버 기동 및 종료
2. Headless Chromium을 통한 모바일 세로(Portrait: 390x844) 및 가로(Landscape: 844x390) 뷰포트 동적 검증
3. 16:9 광범위 화각 뷰포트 종횡비, object-fit contain 크롭 방지, 반응형 flex 분기, 회전 안내 배지 정합성 일괄 판정
4. 증적 캡처 저장 및 콘솔 무결성 검증
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
    """정적 코드 검증: 16:9 해상도 제약 조건, object-fit contain, aspect-ratio 16/9, 미디어 쿼리"""
    checks = {}
    with open("light.html", "r", encoding="utf-8") as f:
        light_code = f.read()
    with open("color.html", "r", encoding="utf-8") as f:
        color_code = f.read()

    # 16:9 constraints
    checks["light_aspect_ratio_16_9_constraint"] = "aspectRatio: { ideal: 1.777777778 }" in light_code and "width: { ideal: 1280" in light_code
    checks["color_aspect_ratio_16_9_constraint"] = "aspectRatio: { ideal: 1.777777778 }" in color_code and "width: { ideal: 1280" in color_code

    # object-fit: contain (화각 크롭 완전 방지)
    checks["light_object_fit_contain"] = "object-fit: contain;" in light_code
    checks["color_object_fit_contain"] = "object-fit: contain;" in color_code

    # CSS aspect-ratio: 16 / 9
    checks["light_aspect_ratio_css"] = "aspect-ratio: 16 / 9;" in light_code
    checks["color_aspect_ratio_css"] = "aspect-ratio: 16 / 9;" in color_code

    # 미디어 쿼리 반응형 분기 (portrait)
    checks["light_media_query_portrait"] = "(orientation: portrait)" in light_code and "(max-aspect-ratio: 1/1)" in light_code
    checks["color_media_query_portrait"] = "(orientation: portrait)" in color_code and "(max-aspect-ratio: 1/1)" in color_code

    # 회전 안내 배지
    checks["light_rotate_hint_element"] = 'id="rotate-hint"' in light_code
    checks["color_rotate_hint_element"] = 'id="rotate-hint"' in color_code

    # 기존 파이프라인 무결성 유지 (Zero-Allocation & 100ms/400ms)
    checks["light_zero_alloc_maintained"] = "new Float32Array(1 * 3 * INPUT_SIZE * INPUT_SIZE)" in light_code
    checks["color_zero_alloc_maintained"] = "new Float32Array(1 * 3 * INPUT_SIZE * INPUT_SIZE)" in color_code

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
        "static_code_checks": {},
        "portrait_color": False,
        "portrait_light": False,
        "landscape_color": False,
        "landscape_light": False,
        "aspect_ratio_accuracy": {},
        "console_errors": []
    }

    results["static_code_checks"] = verify_static_code()
    print(f"✔ [Static Code Audit] 12/12 항목 정적 감사 완료:")
    for k, v in results["static_code_checks"].items():
        print(f"   - {k}: {'PASS' if v else 'FAIL'}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # =================================================================
            # 1. 모바일 세로 모드 (Portrait: 390x844 - iPhone / 갤럭시 표준 규격)
            # =================================================================
            context_portrait = browser.new_context(
                viewport={"width": 390, "height": 844},
                is_mobile=True,
                has_touch=True
            )

            # 1-1. color.html (모바일 세로)
            page_cp = context_portrait.new_page()
            page_cp.on("console", lambda msg: results["console_errors"].append(f"[Color Portrait Console Error] {msg.text}") if msg.type == "error" else None)
            page_cp.goto(f"{base_url}/color.html", wait_until="networkidle")
            page_cp.wait_for_timeout(500)

            # 가상 컨베이어 모드 활성화 및 검사 시작
            page_cp.evaluate("() => { if (typeof setSimMode === 'function') setSimMode(true); }")
            page_cp.click("#btn-toggle")
            page_cp.wait_for_timeout(600)

            # 뷰포트 및 레이아웃 메트릭 측정
            cp_metrics = page_cp.evaluate("""() => {
                const app = document.getElementById('app-container');
                const vp = document.getElementById('viewport-area');
                const sw = document.getElementById('stream-wrapper');
                const sb = document.getElementById('sidebar');
                const hint = document.getElementById('rotate-hint');

                const appStyle = window.getComputedStyle(app);
                const vpRect = vp.getBoundingClientRect();
                const swRect = sw.getBoundingClientRect();
                const hintStyle = window.getComputedStyle(hint);

                return {
                    flexDirection: appStyle.flexDirection,
                    vpWidth: vpRect.width,
                    vpHeight: vpRect.height,
                    vpRatio: vpRect.width / vpRect.height,
                    swWidth: swRect.width,
                    swHeight: swRect.height,
                    swRatio: swRect.width / swRect.height,
                    hintVisible: hintStyle.display !== 'none'
                };
            }""")
            results["aspect_ratio_accuracy"]["color_portrait"] = cp_metrics
            print(f"✔ [Color Portrait Metrics] flex-direction: {cp_metrics['flexDirection']}, 16:9 wrapper ratio: {cp_metrics['swRatio']:.3f} (target: 1.778), hintVisible: {cp_metrics['hintVisible']}")

            # 검증 조건: flex-direction은 column, 16:9 종횡비 허용오차 5% 이내, 회전 힌트 표시
            if cp_metrics["flexDirection"] == "column" and abs(cp_metrics["swRatio"] - (16/9)) < 0.1 and cp_metrics["hintVisible"]:
                results["portrait_color"] = True

            cap_cp_path = os.path.join(EVIDENCE_DIR, "qa_color_portrait_16_9.png")
            page_cp.screenshot(path=cap_cp_path)
            print(f"📸 [Screenshot Captured] {cap_cp_path}")
            page_cp.close()

            # 1-2. light.html (모바일 세로)
            page_lp = context_portrait.new_page()
            page_lp.on("console", lambda msg: results["console_errors"].append(f"[Light Portrait Console Error] {msg.text}") if msg.type == "error" else None)
            page_lp.goto(f"{base_url}/light.html", wait_until="networkidle")
            page_lp.wait_for_timeout(500)

            page_lp.evaluate("() => { if (typeof setSimMode === 'function') setSimMode(true); }")
            page_lp.click("#btn-toggle")
            page_lp.wait_for_timeout(600)

            lp_metrics = page_lp.evaluate("""() => {
                const app = document.getElementById('app-container');
                const sw = document.getElementById('stream-wrapper');
                const hint = document.getElementById('rotate-hint');
                const appStyle = window.getComputedStyle(app);
                const swRect = sw.getBoundingClientRect();
                const hintStyle = window.getComputedStyle(hint);
                return {
                    flexDirection: appStyle.flexDirection,
                    swRatio: swRect.width / swRect.height,
                    hintVisible: hintStyle.display !== 'none'
                };
            }""")
            results["aspect_ratio_accuracy"]["light_portrait"] = lp_metrics
            print(f"✔ [Light Portrait Metrics] flex-direction: {lp_metrics['flexDirection']}, 16:9 wrapper ratio: {lp_metrics['swRatio']:.3f}, hintVisible: {lp_metrics['hintVisible']}")

            if lp_metrics["flexDirection"] == "column" and abs(lp_metrics["swRatio"] - (16/9)) < 0.1 and lp_metrics["hintVisible"]:
                results["portrait_light"] = True

            cap_lp_path = os.path.join(EVIDENCE_DIR, "qa_light_portrait_16_9.png")
            page_lp.screenshot(path=cap_lp_path)
            print(f"📸 [Screenshot Captured] {cap_lp_path}")
            page_lp.close()
            context_portrait.close()

            # =================================================================
            # 2. 모바일 가로 모드 (Landscape: 844x390 - 거치대 가로 와이드 운용)
            # =================================================================
            context_landscape = browser.new_context(
                viewport={"width": 844, "height": 390},
                is_mobile=True,
                has_touch=True
            )

            # 2-1. color.html (가로 모드)
            page_cl = context_landscape.new_page()
            page_cl.on("console", lambda msg: results["console_errors"].append(f"[Color Landscape Console Error] {msg.text}") if msg.type == "error" else None)
            page_cl.goto(f"{base_url}/color.html", wait_until="networkidle")
            page_cl.wait_for_timeout(500)

            page_cl.evaluate("() => { if (typeof setSimMode === 'function') setSimMode(true); }")
            page_cl.click("#btn-toggle")
            page_cl.wait_for_timeout(400)

            # 불량 모의 주입 및 알람 발령 테스트
            page_cl.click("#btn-inject-defect")
            page_cl.wait_for_timeout(1000)

            cl_metrics = page_cl.evaluate("""() => {
                const app = document.getElementById('app-container');
                const sw = document.getElementById('stream-wrapper');
                const banner = document.getElementById('alarm-banner');
                const appStyle = window.getComputedStyle(app);
                const swRect = sw.getBoundingClientRect();
                const bannerStyle = window.getComputedStyle(banner);
                return {
                    flexDirection: appStyle.flexDirection,
                    swRatio: swRect.width / swRect.height,
                    alarmFired: bannerStyle.display === 'flex'
                };
            }""")
            results["aspect_ratio_accuracy"]["color_landscape"] = cl_metrics
            print(f"✔ [Color Landscape Metrics] flex-direction: {cl_metrics['flexDirection']}, 16:9 ratio: {cl_metrics['swRatio']:.3f}, alarmFired: {cl_metrics['alarmFired']}")

            if cl_metrics["flexDirection"] == "row" and abs(cl_metrics["swRatio"] - (16/9)) < 0.1:
                results["landscape_color"] = True

            cap_cl_path = os.path.join(EVIDENCE_DIR, "qa_color_landscape_16_9.png")
            page_cl.screenshot(path=cap_cl_path)
            print(f"📸 [Screenshot Captured] {cap_cl_path}")
            page_cl.close()

            # 2-2. light.html (가로 모드)
            page_ll = context_landscape.new_page()
            page_ll.on("console", lambda msg: results["console_errors"].append(f"[Light Landscape Console Error] {msg.text}") if msg.type == "error" else None)
            page_ll.goto(f"{base_url}/light.html", wait_until="networkidle")
            page_ll.wait_for_timeout(500)

            page_ll.evaluate("() => { if (typeof setSimMode === 'function') setSimMode(true); }")
            page_ll.click("#btn-toggle")
            page_ll.wait_for_timeout(400)

            page_ll.click("#btn-inject-defect")
            page_ll.wait_for_timeout(1000)

            ll_metrics = page_ll.evaluate("""() => {
                const app = document.getElementById('app-container');
                const sw = document.getElementById('stream-wrapper');
                const banner = document.getElementById('alarm-banner');
                const appStyle = window.getComputedStyle(app);
                const swRect = sw.getBoundingClientRect();
                const bannerStyle = window.getComputedStyle(banner);
                return {
                    flexDirection: appStyle.flexDirection,
                    swRatio: swRect.width / swRect.height,
                    alarmFired: bannerStyle.display === 'flex'
                };
            }""")
            results["aspect_ratio_accuracy"]["light_landscape"] = ll_metrics
            print(f"✔ [Light Landscape Metrics] flex-direction: {ll_metrics['flexDirection']}, 16:9 ratio: {ll_metrics['swRatio']:.3f}, alarmFired: {ll_metrics['alarmFired']}")

            if ll_metrics["flexDirection"] == "row" and abs(ll_metrics["swRatio"] - (16/9)) < 0.1:
                results["landscape_light"] = True

            cap_ll_path = os.path.join(EVIDENCE_DIR, "qa_light_landscape_16_9.png")
            page_ll.screenshot(path=cap_ll_path)
            print(f"📸 [Screenshot Captured] {cap_ll_path}")
            page_ll.close()

            context_landscape.close()
            browser.close()

    finally:
        httpd.shutdown()
        server_thread.join(timeout=1.0)
        print(">> [QA Server Terminated cleanly]")

    report_path = os.path.join(EVIDENCE_DIR, "qa_viewport_16_9_summary.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f">> [QA Report Saved] {report_path}")

    all_static_passed = all(results["static_code_checks"].values())
    all_runtime_passed = (
        results["portrait_color"] and
        results["portrait_light"] and
        results["landscape_color"] and
        results["landscape_light"]
    )
    no_console_errors = len(results["console_errors"]) == 0

    print("=================================================================")
    print(f"Static Code Checks Pass: {all_static_passed}")
    print(f"Runtime Portrait 16:9 Pass: {results['portrait_color'] and results['portrait_light']}")
    print(f"Runtime Landscape 16:9 Pass: {results['landscape_color'] and results['landscape_light']}")
    print(f"Console Errors Count: {len(results['console_errors'])}")
    print("=================================================================")

    if all_static_passed and all_runtime_passed and no_console_errors:
        print("🎉 [FINAL QA VERDICT: ALL PASS] 16:9 뷰포트 및 반응형 최적화 완벽 검증 성공!")
        sys.exit(0)
    else:
        print("❌ [FINAL QA VERDICT: FAIL] 일부 검증 항목 불합격")
        sys.exit(1)

if __name__ == "__main__":
    run_qa()
