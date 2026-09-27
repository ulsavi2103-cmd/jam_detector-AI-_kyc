# Graph Report - jam_detector(ai)  (2026-09-27)

## Corpus Check
- 18 files · ~44,253 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 123 nodes · 143 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a86179b`
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
- 컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처
- 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조
- VirtualConveyor
- [Gate 3 QA 리포트] 1·2번 실시간 AI 자세 검사기 통합 QA 판정 보고서 (QA Evaluator)
- [Gate 1 리뷰] 기획 및 계획 검토 보고서 (Reviewer)
- graphify.md

## God Nodes (most connected - your core abstractions)
1. `inspect_box_posture()` - 11 edges
2. `작업 체크리스트` - 7 edges
3. `VirtualConveyor` - 6 edges
4. `MotionStateMachine` - 6 edges
5. `ConveyorBox` - 6 edges
6. `Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)` - 5 edges
7. `Ⅳ. 4단계 완전 자율 파이프라인 게이트` - 5 edges
8. `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조` - 5 edges
9. `2. 세부 기능 요구사항 (Functional Requirements)` - 5 edges
10. `컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처` - 5 edges

## Surprising Connections (you probably didn't know these)
- `1. 개요 및 배경 (Overview & Background)` --references--> `inspect_box_posture()`  [INFERRED]
  docs/01_request_spec.md → test_simulation_feature1_2.py
- `F-4. 파이썬 가상 시뮬레이션 및 검증 스크립트 (`test_simulation_feature1_2.py`)` --references--> `inspect_box_posture()`  [INFERRED]
  docs/01_request_spec.md → test_simulation_feature1_2.py
- `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  TASK_AI_VISION_UPGRADE.md → test_simulation_feature1_2.py
- `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/index.md → test_simulation_feature1_2.py
- `3.1 코랩 학습 모델 슬롯 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/landscape_ai_vision_upgrade.md → test_simulation_feature1_2.py

## Import Cycles
- None detected.

## Communities (14 total, 2 thin omitted)

### Community 0 - "test_simulation.py"
Cohesion: 0.15
Nodes (17): argparse, cv2, http_server, json, numpy, os, playwright_sync_api, find_free_port() (+9 more)

### Community 1 - "inspect_box_posture"
Cohesion: 0.18
Nodes (10): 1. 세부 변경 사항 대조 검증, 2. 리뷰 최종 판정, [Gate 2 리뷰] 구현 및 변경 사항 대조 검토 보고서 (Reviewer), ConveyorBox, draw_conveyor_background(), inspect_box_posture(), ndarray, [향후 코랩 MobileNetV3 ONNX 모델 장착 슬롯] - Input: 통과 구역 크롭 이미지 (numpy array, BGR) -… (+2 more)

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
Nodes (8): 1. 개요 및 배경 (Overview & Background), 2. 세부 기능 요구사항 (Functional Requirements), 3. 제약 조건 및 비기능 요구사항, F-1. 기존 레거시 코드 정리 및 3번 기능 비활성화, F-2. 스마트폰 가로 모드(Landscape, 16:9) UI/UX 최적화, F-3. 통과 즉시 판별 파이프라인 및 AI 더미 인터페이스, F-4. 파이썬 가상 시뮬레이션 및 검증 스크립트 (`test_simulation_feature1_2.py`), [요구사항 명세서] 1·2번 기능 리팩토링: 가로모드 실시간 AI 자세/전도 검사기 개조

### Community 6 - "작업 체크리스트"
Cohesion: 0.22
Nodes (8): Task 1: 레거시 코드 정리 및 3번 기능 비활성화, Task 2: 가로 모드(Landscape, 16:9) 웹 UI 레이아웃 개편 & 터치 매핑, Task 3: 통과 즉시 판별 파이프라인 및 더미 함수 구축, Task 4: 가상 시뮬레이션 검증 스크립트 작성 (`test_simulation_feature1_2.py`), Task 5: Gate 3 초고속 원샷 통합 QA 및 증적 수집, Task 6: Wiki 문서화 및 세션 종료 (Gate 4), [작업 계획서] 1·2번 기능 리팩토링: 가로모드 실시간 AI 자세/전도 검사기 (To-Do), 작업 체크리스트

### Community 7 - "컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처"
Cohesion: 0.22
Nodes (9): 1. 개요 및 설계 의도, 2. 핵심 아키텍처 파이프라인, 3.1 코랩 학습 모델 슬롯 (`inspect_box_posture`), 3.2 1:1 터치 좌표계 매핑, 3. 주요 모듈 및 인터페이스 규격, 4.1 가상 시뮬레이터 실행 (Python), 4.2 웹 애플리케이션 실행, 4. 검증 및 테스트 가이드 (+1 more)

### Community 8 - "📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조"
Cohesion: 0.25
Nodes (7): 1. 개요 및 전환 배경, ① 통과선 기반 즉시 검사 메커니즘, 2. 모바일 구동 환경 요구사항 (★ 가로 모드 필수 반영), ② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`), 3. 감지 대상 및 판별 규칙, 4. 핵심 아키텍처 및 파이프라인 요구사항, 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조

### Community 9 - "VirtualConveyor"
Cohesion: 0.38
Nodes (3): calculate_grid_boxes(), 화면 해상도에 맞춰 15열 x 2단의 Bounding Box (x, y, w, h)를 계산합니다., VirtualConveyor

### Community 10 - "[Gate 3 QA 리포트] 1·2번 실시간 AI 자세 검사기 통합 QA 판정 보고서 (QA Evaluator)"
Cohesion: 0.40
Nodes (4): 1. 자동화 검증 항목 및 판정 (Assertions), 2. 생성 증적(Screenshots) 판독, 3. QA 최종 판정 신호: **PASS**, [Gate 3 QA 리포트] 1·2번 실시간 AI 자세 검사기 통합 QA 판정 보고서 (QA Evaluator)

### Community 11 - "[Gate 1 리뷰] 기획 및 계획 검토 보고서 (Reviewer)"
Cohesion: 0.50
Nodes (3): 1. 요구사항 대비 계획 적합성 검토, 2. 리뷰 최종 판정, [Gate 1 리뷰] 기획 및 계획 검토 보고서 (Reviewer)

## Knowledge Gaps
- **39 isolated node(s):** `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커`, `Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule)`, `Gate 1: 기획 단계 (Spec ➔ Planning)` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 66 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `inspect_box_posture()` connect `inspect_box_posture` to `test_simulation.py`, `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장`, `2. 세부 기능 요구사항 (Functional Requirements)`, `컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처`, `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조`?**
  _High betweenness centrality (0.373) - this node is a cross-community bridge._
- **Why does `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` connect `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장` to `inspect_box_posture`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `inspect_box_posture()` (e.g. with `1. 개요 및 배경 (Overview & Background)` and `F-4. 파이썬 가상 시뮬레이션 및 검증 스크립트 (`test_simulation_feature1_2.py`)`) actually correct?**
  _`inspect_box_posture()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_simulation.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14736842105263157 - nodes in this community are weakly interconnected._