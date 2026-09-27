# Graph Report - jam_detector(ai)  (2026-09-27)

## Corpus Check
- 18 files · ~43,818 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 1 file(s) not represented in the graph (top: (none) 1)

## Summary
- 119 nodes · 136 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ccc9cbaa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_gate3_qa_feature1_2.py
- test_simulation_feature1_2.py
- [기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장
- test_simulation.py
- Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)
- [요구사항 명세서] 모바일 거치대 안정성을 위한 경보 진동 제거 및 사운드 단일화
- 작업 체크리스트
- 컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처
- 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조
- VirtualConveyor
- [Gate 3 QA 리포트] 경보 진동 제거 및 오디오 경보 단일화 통합 QA 보고서 (QA Evaluator)
- [Gate 1 리뷰] 경보 진동 제거 및 사운드 단일화 기획 검토 (Reviewer)
- graphify.md
- [Gate 2 리뷰] 진동 코드 제거 및 사운드 무결성 교차 심사 (Reviewer)

## God Nodes (most connected - your core abstractions)
1. `inspect_box_posture()` - 8 edges
2. `VirtualConveyor` - 6 edges
3. `MotionStateMachine` - 6 edges
4. `ConveyorBox` - 6 edges
5. `Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)` - 5 edges
6. `Ⅳ. 4단계 완전 자율 파이프라인 게이트` - 5 edges
7. `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조` - 5 edges
8. `작업 체크리스트` - 5 edges
9. `컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처` - 5 edges
10. `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장` - 5 edges

## Surprising Connections (you probably didn't know these)
- `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  TASK_AI_VISION_UPGRADE.md → test_simulation_feature1_2.py
- `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/index.md → test_simulation_feature1_2.py
- `3.1 코랩 학습 모델 슬롯 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/landscape_ai_vision_upgrade.md → test_simulation_feature1_2.py

## Import Cycles
- None detected.

## Communities (15 total, 2 thin omitted)

### Community 0 - "run_gate3_qa_feature1_2.py"
Cohesion: 0.17
Nodes (12): http_server, json, os, playwright_sync_api, find_free_port(), run_gate3_qa_feature1_2.py…, run_qa(), socket (+4 more)

### Community 1 - "test_simulation_feature1_2.py"
Cohesion: 0.22
Nodes (10): cv2, numpy, ConveyorBox, draw_conveyor_background(), inspect_box_posture(), ndarray, test_simulation_feature1_2.py…, [향후 코랩 MobileNetV3 ONNX 모델 장착 슬롯] - Input: 통과 구역 크롭 이미지 (numpy array, BGR) -… (+2 more)

### Community 2 - "[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장"
Cohesion: 0.15
Nodes (10): 기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩), 기능 3. 소박스 전도(누움) 감지 시스템 (비활성화), 시스템 위키 색인 (Wiki Index), 1. 아키텍처 개요, 2.1 Bilinear 보간 오버레이 투영 (Projective Mapping), 2.2 OpenCV.js Perspective Warp 평면 추출, 2. 핵심 알고리즘 및 엔진, 3. 설정 영구 보존 스키마 (`roi_config.json`) (+2 more)

### Community 3 - "test_simulation.py"
Cohesion: 0.18
Nodes (10): argparse, inspect_single_box(), load_roi_config(), MotionStateMachine, ndarray, test_simulation.py…, 30개 박스를 순회하며 inspect_single_box 호출 (Perspective Warp 평면 검증 포함), roi_config.json 파일에서 4개 모서리 좌표를 로드합니다. (+2 more)

### Community 4 - "Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)"
Cohesion: 0.20
Nodes (9): Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진), Gate 1: 기획 단계 (Spec ➔ Planning), Gate 2: 개발 단계 (Implementation ➔ Cross Review), Gate 3: 초고속 원샷 통합 QA 단계 (High-Speed One-Shot QA), Gate 4: Wiki 및 완성 단계, Ⅰ. 상태 신호 체계 (Signal Protocol), Ⅱ. 예외 처리 및 서킷 브레이커, Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule) (+1 more)

### Community 5 - "[요구사항 명세서] 모바일 거치대 안정성을 위한 경보 진동 제거 및 사운드 단일화"
Cohesion: 0.29
Nodes (6): 1. 개요 및 배경 (Background & Objective), 2. 세부 기능 요구사항 (Functional Requirements), 3. 검증 기준 (Acceptance Criteria), F-1. 기기 물리 진동 로직 완전 제거, F-2. 사운드 및 시각 경보 무결성 유지, [요구사항 명세서] 모바일 거치대 안정성을 위한 경보 진동 제거 및 사운드 단일화

### Community 6 - "작업 체크리스트"
Cohesion: 0.29
Nodes (6): Task 1: 진동 로직 완전 제거 (Implementation), Task 2: 교차 리뷰 및 Gate 2 승인 (Reviewer), Task 3: 원샷 자동화 QA 및 증적 수집 (Gate 3), Task 4: 위키 및 최종 완료 보고 (Gate 4), [작업 계획서] 경보 진동 제거 및 오디오 경보 단일화 (To-Do), 작업 체크리스트

### Community 7 - "컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처"
Cohesion: 0.22
Nodes (9): 1. 개요 및 설계 의도, 2. 핵심 아키텍처 파이프라인, 3.1 코랩 학습 모델 슬롯 (`inspect_box_posture`), 3.2 1:1 터치 좌표계 매핑, 3. 주요 모듈 및 인터페이스 규격, 4.1 가상 시뮬레이터 실행 (Python), 4.2 웹 애플리케이션 실행, 4. 검증 및 테스트 가이드 (+1 more)

### Community 8 - "📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조"
Cohesion: 0.25
Nodes (7): 1. 개요 및 전환 배경, ① 통과선 기반 즉시 검사 메커니즘, 2. 모바일 구동 환경 요구사항 (★ 가로 모드 필수 반영), ② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`), 3. 감지 대상 및 판별 규칙, 4. 핵심 아키텍처 및 파이프라인 요구사항, 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조

### Community 9 - "VirtualConveyor"
Cohesion: 0.38
Nodes (3): calculate_grid_boxes(), 화면 해상도에 맞춰 15열 x 2단의 Bounding Box (x, y, w, h)를 계산합니다., VirtualConveyor

### Community 10 - "[Gate 3 QA 리포트] 경보 진동 제거 및 오디오 경보 단일화 통합 QA 보고서 (QA Evaluator)"
Cohesion: 0.50
Nodes (3): 1. 자동화 검증 항목 및 판정, 2. QA 최종 판정: **PASS**, [Gate 3 QA 리포트] 경보 진동 제거 및 오디오 경보 단일화 통합 QA 보고서 (QA Evaluator)

### Community 11 - "[Gate 1 리뷰] 경보 진동 제거 및 사운드 단일화 기획 검토 (Reviewer)"
Cohesion: 0.50
Nodes (3): 1. 적합성 검토, 2. 최종 판정, [Gate 1 리뷰] 경보 진동 제거 및 사운드 단일화 기획 검토 (Reviewer)

### Community 14 - "[Gate 2 리뷰] 진동 코드 제거 및 사운드 무결성 교차 심사 (Reviewer)"
Cohesion: 0.40
Nodes (4): 1. 코드 변경 사항 대조 심사 (Diff Audit), 2. 부작용(Side-effect) 및 안정성 평가, 3. 최종 판정, [Gate 2 리뷰] 진동 코드 제거 및 사운드 무결성 교차 심사 (Reviewer)

## Knowledge Gaps
- **38 isolated node(s):** `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커`, `Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule)`, `Gate 1: 기획 단계 (Spec ➔ Planning)` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 65 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `inspect_box_posture()` connect `test_simulation_feature1_2.py` to `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조`, `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장`, `컨베이어 가로모드(16:9) 실시간 AI 자세/전도 검사기 아키텍처`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Why does `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` connect `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장` to `test_simulation_feature1_2.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `inspect_box_posture()` (e.g. with `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` and `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)`) actually correct?**
  _`inspect_box_posture()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._