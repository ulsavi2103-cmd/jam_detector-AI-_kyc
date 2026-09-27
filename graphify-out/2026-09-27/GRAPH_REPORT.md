# Graph Report - jam_detector(ai)  (2026-09-27)

## Corpus Check
- 18 files · ~46,903 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .onnx 2, (none) 1)

## Summary
- 129 nodes · 146 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `65aa7497`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_simulation.py
- inspect_box_posture
- [기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장
- MotionStateMachine
- Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)
- 2. 세부 기능 요구사항 (Functional Requirements)
- 작업 체크리스트
- 3. 핵심 모듈 및 구현 규격
- 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조
- VirtualConveyor
- [Gate 3 QA 리포트] 고속 컨베이어 및 모바일 OOM 방지 통합 QA 보고서 (QA Evaluator)
- [Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)
- graphify.md
- [Gate 2 리뷰] 고속 컨베이어 및 모바일 OOM 방지 리팩토링 교차 심사 (Reviewer)

## God Nodes (most connected - your core abstractions)
1. `작업 체크리스트` - 8 edges
2. `inspect_box_posture()` - 7 edges
3. `VirtualConveyor` - 6 edges
4. `MotionStateMachine` - 6 edges
5. `ConveyorBox` - 6 edges
6. `Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)` - 5 edges
7. `Ⅳ. 4단계 완전 자율 파이프라인 게이트` - 5 edges
8. `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조` - 5 edges
9. `2. 세부 기능 요구사항 (Functional Requirements)` - 5 edges
10. `컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처` - 5 edges

## Surprising Connections (you probably didn't know these)
- `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  TASK_AI_VISION_UPGRADE.md → test_simulation_feature1_2.py
- `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/index.md → test_simulation_feature1_2.py

## Import Cycles
- None detected.

## Communities (15 total, 2 thin omitted)

### Community 0 - "test_simulation.py"
Cohesion: 0.13
Nodes (19): argparse, cv2, http_server, json, numpy, os, playwright_sync_api, find_free_port() (+11 more)

### Community 1 - "inspect_box_posture"
Cohesion: 0.27
Nodes (7): ConveyorBox, draw_conveyor_background(), inspect_box_posture(), ndarray, [향후 코랩 MobileNetV3 ONNX 모델 장착 슬롯] - Input: 통과 구역 크롭 이미지 (numpy array, BGR) -…, run_headless_tests(), run_interactive_simulation()

### Community 2 - "[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장"
Cohesion: 0.15
Nodes (10): 기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩), 기능 3. 소박스 전도(누움) 감지 시스템 (비활성화), 시스템 위키 색인 (Wiki Index), 1. 아키텍처 개요, 2.1 Bilinear 보간 오버레이 투영 (Projective Mapping), 2.2 OpenCV.js Perspective Warp 평면 추출, 2. 핵심 알고리즘 및 엔진, 3. 설정 영구 보존 스키마 (`roi_config.json`) (+2 more)

### Community 3 - "MotionStateMachine"
Cohesion: 0.20
Nodes (8): inspect_single_box(), load_roi_config(), MotionStateMachine, ndarray, 30개 박스를 순회하며 inspect_single_box 호출 (Perspective Warp 평면 검증 포함), roi_config.json 파일에서 4개 모서리 좌표를 로드합니다., [향후 코랩 모델 장착 슬롯] - 입력: 15x2 중 개별 상자 1개의 크롭 이미지 (numpy array) - 출력:…, run_simulation()

### Community 4 - "Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)"
Cohesion: 0.20
Nodes (9): Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진), Gate 1: 기획 단계 (Spec ➔ Planning), Gate 2: 개발 단계 (Implementation ➔ Cross Review), Gate 3: 초고속 원샷 통합 QA 단계 (High-Speed One-Shot QA), Gate 4: Wiki 및 완성 단계, Ⅰ. 상태 신호 체계 (Signal Protocol), Ⅱ. 예외 처리 및 서킷 브레이커, Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule) (+1 more)

### Community 5 - "2. 세부 기능 요구사항 (Functional Requirements)"
Cohesion: 0.22
Nodes (8): 1. 개요 및 배경 (Background & Objective), 2. 세부 기능 요구사항 (Functional Requirements), 3. 검증 기준 (Acceptance Criteria), F-1. 카메라 해상도 제한 (`getUserMedia`), F-2. 메모리 누수 방지 (Buffer Zero-Allocation 전처리), F-3. 고속 통과(0.6초) 추론 주기 및 중복 방지(Debounce), F-4. 모델 파라미터 및 ONNX 런타임 규격, [요구사항 명세서] 고속 컨베이어(0.6s) 및 4~5시간 연속 운용 최적화 비전 파이프라인 리팩토링

### Community 6 - "작업 체크리스트"
Cohesion: 0.20
Nodes (9): Task 1: 카메라 해상도 640x480 제한 (Implementation), Task 2: Buffer Zero-Allocation 전처리 파이프라인 (Implementation), Task 3: 고속 통과(0.6초) 주기 및 쿨다운 디바운스 로직 (Implementation), Task 4: ONNX 모델 파라미터 및 런타임 연동 (Implementation), Task 5: Gate 2 교차 리뷰 및 승인 (Reviewer), Task 6: Gate 3 원샷 자동화 QA 및 증적 수집 (QA Evaluator), Task 7: Gate 4 위키 및 최종 완료 보고 (Master), [작업 계획서] 고속 컨베이어 및 장시간 스마트폰 연속 운용 최적화 (To-Do) (+1 more)

### Community 7 - "3. 핵심 모듈 및 구현 규격"
Cohesion: 0.18
Nodes (11): 1. 개요 및 설계 의도, 2. 실시간 AI 비전 파이프라인, 3.1 카메라 해상도 제한 (`getUserMedia`), 3.2 Buffer Zero-Allocation 및 ImageNet NCHW 전처리, 3.3 0.6초 주기 대응 100ms 주기 / 400ms 디바운스 쿨다운, 3.4 ONNX Runtime Web WASM 및 클래스 인덱스 매핑, 3. 핵심 모듈 및 구현 규격, 4.1 원샷 자동화 통합 QA (Playwright) (+3 more)

### Community 8 - "📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조"
Cohesion: 0.25
Nodes (7): 1. 개요 및 전환 배경, ① 통과선 기반 즉시 검사 메커니즘, 2. 모바일 구동 환경 요구사항 (★ 가로 모드 필수 반영), ② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`), 3. 감지 대상 및 판별 규칙, 4. 핵심 아키텍처 및 파이프라인 요구사항, 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조

### Community 9 - "VirtualConveyor"
Cohesion: 0.38
Nodes (3): calculate_grid_boxes(), 화면 해상도에 맞춰 15열 x 2단의 Bounding Box (x, y, w, h)를 계산합니다., VirtualConveyor

### Community 10 - "[Gate 3 QA 리포트] 고속 컨베이어 및 모바일 OOM 방지 통합 QA 보고서 (QA Evaluator)"
Cohesion: 0.40
Nodes (4): 1. 세부 검증 항목 및 판정, 2. 증적 스크린샷, 3. QA 최종 판정: **PASS**, [Gate 3 QA 리포트] 고속 컨베이어 및 모바일 OOM 방지 통합 QA 보고서 (QA Evaluator)

### Community 11 - "[Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)"
Cohesion: 0.50
Nodes (3): 1. 적합성 검토 결과, 2. 최종 판정, [Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)

### Community 14 - "[Gate 2 리뷰] 고속 컨베이어 및 모바일 OOM 방지 리팩토링 교차 심사 (Reviewer)"
Cohesion: 0.40
Nodes (4): 1. 코드 변경 사항 대조 심사 (Diff Audit), 2. 부작용 및 안정성 평가, 3. 최종 판정, [Gate 2 리뷰] 고속 컨베이어 및 모바일 OOM 방지 리팩토링 교차 심사 (Reviewer)

## Knowledge Gaps
- **47 isolated node(s):** `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커`, `Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule)`, `Gate 1: 기획 단계 (Spec ➔ Planning)` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 75 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `inspect_box_posture()` connect `inspect_box_posture` to `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조`, `test_simulation.py`, `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장`?**
  _High betweenness centrality (0.229) - this node is a cross-community bridge._
- **Why does `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` connect `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장` to `inspect_box_posture`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `inspect_box_posture()` (e.g. with `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` and `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)`) actually correct?**
  _`inspect_box_posture()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_simulation.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._