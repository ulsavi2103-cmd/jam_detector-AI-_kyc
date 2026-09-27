# Graph Report - jam_detector(ai)  (2026-09-27)

## Corpus Check
- 20 files · ~53,732 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .onnx 2, (none) 1)

## Summary
- 134 nodes · 161 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `17f89eed`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_gate3_qa_feature1_2.py
- test_simulation.py
- [기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장
- MotionStateMachine
- Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)
- 2. 세부 기능 요구사항 (Functional Requirements)
- 작업 체크리스트
- 컨베이어 16:9 와이드 광범위 AI 비전 파이프라인 아키텍처
- 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조
- VirtualConveyor
- [Gate 3 QA 판정 보고서] 16:9 광범위 뷰포트 및 반응형 최적화 자동화 검증
- [Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)
- graphify.md
- [Gate 2 교차 검토 보고서] 모바일 16:9 광범위 뷰포트 정상화 및 반응형 최적화

## God Nodes (most connected - your core abstractions)
1. `작업 체크리스트` - 8 edges
2. `inspect_box_posture()` - 7 edges
3. `VirtualConveyor` - 6 edges
4. `MotionStateMachine` - 6 edges
5. `ConveyorBox` - 6 edges
6. `[Gate 3 QA 판정 보고서] 16:9 광범위 뷰포트 및 반응형 최적화 자동화 검증` - 6 edges
7. `Antigravity Production Protocol (초고속 완전 자율 워크플로우 엔진)` - 5 edges
8. `Ⅳ. 4단계 완전 자율 파이프라인 게이트` - 5 edges
9. `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조` - 5 edges
10. `2. 세부 기능 요구사항 (Functional Requirements)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` --references--> `inspect_box_posture()`  [INFERRED]
  TASK_AI_VISION_UPGRADE.md → test_simulation_feature1_2.py
- `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` --references--> `inspect_box_posture()`  [INFERRED]
  wiki/index.md → test_simulation_feature1_2.py

## Import Cycles
- None detected.

## Communities (15 total, 2 thin omitted)

### Community 0 - "run_gate3_qa_feature1_2.py"
Cohesion: 0.16
Nodes (17): http_server, json, playwright_sync_api, find_free_port(), run_gate3_qa_feature1_2.py…, 정적 코드 검증: 해상도 제한, Zero-allocation 버퍼, 0:defect / 1:normal 매핑, run_qa(), verify_static_code() (+9 more)

### Community 1 - "test_simulation.py"
Cohesion: 0.17
Nodes (14): argparse, cv2, numpy, os, sys, ConveyorBox, draw_conveyor_background(), inspect_box_posture() (+6 more)

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
Nodes (8): 1. 결함 원인 분석 (Root Cause Analysis), 2. 세부 기능 요구사항 (Functional Requirements), 3. 검증 기준 (Acceptance Criteria), F-1. 카메라 16:9 광범위 스트림 제약 조건 (`getUserMedia`), F-2. 모바일 반응형 16:9 뷰포트 레이아웃 (세로/가로 모드 완벽 분기), F-3. 비디오/캔버스 16:9 왜곡 및 잘림(Crop) 방지, F-4. 적용 대상 엔드포인트, [요구사항 명세서] 모바일 16:9 광범위 카메라 촬영 뷰포트 정상화 및 반응형 최적화

### Community 6 - "작업 체크리스트"
Cohesion: 0.20
Nodes (9): Task 1: 카메라 16:9 광범위 스트림 제약 조건 적용 (Implementation), Task 2: 모바일 반응형 16:9 뷰포트 레이아웃 구현 (Implementation), Task 3: 비디오 및 캔버스 16:9 잘림(Crop) 방지 및 터치 좌표 정합 (Implementation), Task 4: 사용자 UX 개선 및 가로 회전 권장 안내 HUD (Implementation), Task 5: Gate 2 교차 리뷰 및 승인 (Reviewer), Task 6: Gate 3 원샷 자동화 QA 및 증적 수집 (QA Evaluator), Task 7: Gate 4 위키 및 최종 완료 보고 (Master), [작업 계획서] 모바일 16:9 광범위 카메라 뷰포트 정상화 및 반응형 최적화 (To-Do) (+1 more)

### Community 7 - "컨베이어 16:9 와이드 광범위 AI 비전 파이프라인 아키텍처"
Cohesion: 0.25
Nodes (8): 1. 개요 및 설계 의도, 2. 반응형 16:9 뷰포트 아키텍처, 3.1 16:9 카메라 제약 조건 (`getUserMedia`), 3.2 16:9 종횡비 컨테이너 및 크롭 방지 CSS, 3.3 Zero-Allocation 전처리 및 디바운스, 3. 핵심 구현 사양, 4. 검증 결과, 컨베이어 16:9 와이드 광범위 AI 비전 파이프라인 아키텍처

### Community 8 - "📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조"
Cohesion: 0.25
Nodes (7): 1. 개요 및 전환 배경, ① 통과선 기반 즉시 검사 메커니즘, 2. 모바일 구동 환경 요구사항 (★ 가로 모드 필수 반영), ② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`), 3. 감지 대상 및 판별 규칙, 4. 핵심 아키텍처 및 파이프라인 요구사항, 📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조

### Community 9 - "VirtualConveyor"
Cohesion: 0.38
Nodes (3): calculate_grid_boxes(), 화면 해상도에 맞춰 15열 x 2단의 Bounding Box (x, y, w, h)를 계산합니다., VirtualConveyor

### Community 10 - "[Gate 3 QA 판정 보고서] 16:9 광범위 뷰포트 및 반응형 최적화 자동화 검증"
Cohesion: 0.29
Nodes (6): 1. 개요 및 테스트 환경, 2. 12대 정적 코드 감사 (Static Code Audit) 결과, 3. 런타임 뷰포트 정합성 및 반응형 메트릭 실측치, 4. 증적 캡처 (Evidence), 5. 결론, [Gate 3 QA 판정 보고서] 16:9 광범위 뷰포트 및 반응형 최적화 자동화 검증

### Community 11 - "[Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)"
Cohesion: 0.50
Nodes (3): 1. 적합성 검토 결과, 2. 최종 판정, [Gate 1 리뷰] 고속 컨베이어 및 모바일 연속 운용 리팩토링 기획 검토 (Reviewer)

### Community 14 - "[Gate 2 교차 검토 보고서] 모바일 16:9 광범위 뷰포트 정상화 및 반응형 최적화"
Cohesion: 0.40
Nodes (4): 1. 심사 개요, 2. 세부 검토 항목 및 결과, 3. Reviewer 종합 판정 및 결론, [Gate 2 교차 검토 보고서] 모바일 16:9 광범위 뷰포트 정상화 및 반응형 최적화

## Knowledge Gaps
- **47 isolated node(s):** `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커`, `Ⅲ. 증거 기반 개발 원칙 (Evidence-based Rule)`, `Gate 1: 기획 단계 (Spec ➔ Planning)` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 72 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `inspect_box_posture()` connect `test_simulation.py` to `📌 [TASK] 1·2번 기능 리팩토링: 단순 정체 감지기 → 가로모드 실시간 AI 자세/전도 검사기 개조`, `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장`?**
  _High betweenness centrality (0.213) - this node is a cross-community bridge._
- **Why does `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)` connect `[기술 위키] 4포인트 원근 보정(Perspective Warp) 캘리브레이션 및 ROI 설정 자동 저장` to `test_simulation.py`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `inspect_box_posture()` (e.g. with `② 추상화된 더미 추론 인터페이스 (`inspect_box_posture`)` and `기능 1·2. 가로모드 실시간 AI 자세/전도 검사기 (신규 리빌딩)`) actually correct?**
  _`inspect_box_posture()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Ⅰ. 상태 신호 체계 (Signal Protocol)`, `Ⅱ. 예외 처리 및 서킷 브레이커` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._