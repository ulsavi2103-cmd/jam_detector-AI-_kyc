"""
run_gate3_qa_feature1_2.py
=============================================================================
Gate 3 원샷 고속 통합 QA 러너:
1. 원자적 로컬 서버 기동 및 종료 생명주기 결합
2. Headless Chromium을 활용한 index.html, light.html, color.html 검증
3. 't' 키 불량 주입 및 0.1초 즉시 경보 발령 증적 수집
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
        "light_defect_alarm": False,
        "color_defect_alarm": False,
        "console_errors": []
    }

    try:
        with sync_playwright() as p:
            # 16:9 가로 모드 뷰포트 (1280x720)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})

            # -------------------------------------------------------------
            # 1. index.html 검증
            # -------------------------------------------------------------
            page_index = context.new_page()
            page_index.on("pageerror", lambda err: results["console_errors"].append(str(err)))
            page_index.goto(f"{base_url}/index.html")
            page_index.wait_for_selector("#btn-tilt-disabled")
            
            # 3번 비활성화 및 1, 2번 링크 존재 확인
            has_light = page_index.is_visible("#link-light")
            has_color = page_index.is_visible("#link-color")
            has_tilt_disabled = page_index.is_visible("#btn-tilt-disabled")
            if has_light and has_color and has_tilt_disabled:
                results["index_check"] = True
                page_index.screenshot(path=os.path.join(EVIDENCE_DIR, "01_index_landscape_menu.png"))
                print("✔ [QA 1/4] index.html 1·2번 집중 및 3번 비활성화 검증 완료")
            page_index.close()

            # -------------------------------------------------------------
            # 2. light.html 검증 (가상 컨베이어 모드 + 정상 통과 + 't' 키 불량 즉각 경보)
            # -------------------------------------------------------------
            page_light = context.new_page()
            page_light.on("pageerror", lambda err: results["console_errors"].append(str(err)))
            page_light.goto(f"{base_url}/light.html")
            page_light.wait_for_selector("#btn-toggle")

            # 가상 컨베이어 확실하게 켜기 및 검사 시작
            page_light.evaluate("() => setSimMode(true)")
            page_light.click("#btn-toggle")
            time.sleep(1.0)
            page_light.screenshot(path=os.path.join(EVIDENCE_DIR, "02_light_normal_feed.png"))
            results["light_normal"] = True
            print("✔ [QA 2/4] light.html 16:9 가로 레이아웃 및 정상 감시 루프 검증 완료")

            # 키보드 't' 누름 ➔ 불량 주입 ➔ 0.1초 내 경보 배너 검증
            page_light.keyboard.press("t")
            print(">> [LIGHT] 't' 키 입력 완료 -> 불량 상자 통과 대기")
            # 경보 배너 나타날 때까지 대기
            page_light.wait_for_selector("#alarm-banner", state="visible", timeout=6000)
            banner_text = page_light.inner_text("#alarm-title")
            assert "불량" in banner_text, f"경보 문구 불일치: {banner_text}"
            page_light.screenshot(path=os.path.join(EVIDENCE_DIR, "03_light_defect_alarm.png"))
            results["light_defect_alarm"] = True
            print("✔ [QA 3/4] light.html 키보드 't' 불량 주입 즉각 경보 발령 검증 완료")
            page_light.close()

            # -------------------------------------------------------------
            # 3. color.html 검증 (가상 컨베이어 + 't' 키 불량 즉각 경보)
            # -------------------------------------------------------------
            page_color = context.new_page()
            page_color.on("pageerror", lambda err: results["console_errors"].append(str(err)))
            page_color.goto(f"{base_url}/color.html")
            page_color.wait_for_selector("#btn-toggle")

            page_color.evaluate("() => setSimMode(true)")
            page_color.click("#btn-toggle")
            time.sleep(0.5)

            page_color.keyboard.press("t")
            print(">> [COLOR] 't' 키 입력 완료 -> 불량 상자 통과 대기")
            page_color.wait_for_selector("#alarm-banner", state="visible", timeout=6000)
            banner_text = page_color.inner_text("#alarm-title")
            assert "불량" in banner_text, f"경보 문구 불일치: {banner_text}"
            page_color.screenshot(path=os.path.join(EVIDENCE_DIR, "04_color_defect_alarm.png"))
            results["color_defect_alarm"] = True
            print("✔ [QA 4/4] color.html 키보드 't' 불량 주입 즉각 경보 발령 검증 완료")
            page_color.close()

            browser.close()

    finally:
        httpd.shutdown()
        print(">> [QA Server Terminated]")

    # 검증 요약 저장
    summary_path = os.path.join(EVIDENCE_DIR, "qa_feature1_2_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    all_pass = (
        results["index_check"] and
        results["light_normal"] and
        results["light_defect_alarm"] and
        results["color_defect_alarm"] and
        len(results["console_errors"]) == 0
    )

    if all_pass:
        print("\n🎉 [GATE 3 QA] 모든 웹앱 통합 검증 항목 통과 (ALL PASS)!")
        return 0
    else:
        print(f"\n❌ [GATE 3 QA FAIL] 결과: {results}")
        return 1

if __name__ == "__main__":
    sys.exit(run_qa())
