# [요구사항 명세서] 4포인트 원근 왜곡 보정(Perspective Warp) 및 ROI 설정 자동 저장

## 1. 개요 및 배경
- **현장 설치 환경 특성:** 현장 카메라가 컨베이어 벨트 작업대 상부 대각선에서 비스듬히 내려다보는 앵글로 설치되어, 15열 × 2행(총 30개) 소박스 묶음이 직사각형이 아닌 사다리꼴 형태(원근 투영 왜곡, Perspective Distortion)로 촬영됨.
- **기존 한계:** 기존 정렬 방식은 직교 2D 축 기준 Axis-Aligned Bounding Box (AABB) 형태여서, 비스듬한 앵글에서는 각 상자의 실제 위치와 격자가 어긋나 전도 검사 및 템플릿 매칭의 정확도가 급격히 저하됨.
- **해결 목표:** 현장 엔지니어가 단 10초 만에 4개의 꼭짓점(좌상, 우상, 우하, 좌하)을 터치/드래그하여 원근 왜곡을 평면 직사각형으로 정규화(Unwarp)하고, 해당 캘리브레이션 좌표를 `roi_config.json` 및 `localStorage`로 영구 자동 저장하여 재부팅 시에도 즉각 복원되는 현장 최적화 파이프라인 구축.

---

## 2. 세부 기능 요구사항 (Functional Requirements)

### F-1. 4포인트 원근 왜곡 보정(Perspective Warp) 캘리브레이션
1. **4개 제어점(Control Points) UI/UX:**
   - 30개 박스 묶음의 네 모서리:
     - `TL` (Top-Left, 좌상단)
     - `TR` (Top-Right, 우상단)
     - `BR` (Bottom-Right, 우하단)
     - `BL` (Bottom-Left, 좌하단)
   - 모바일/터치 및 마우스 드래그를 지원하는 직관적인 핸들러(지름 18px의 고대비 링 & 번호 배지) 제공.
   - 핸들러 드래그 또는 '모서리 순차 클릭 캘리브레이션 모드' 지원.
2. **원근 격자(Warped Grid) 실시간 투영 오버레이:**
   - 4개 점을 잇는 볼록 다각형 외곽선 렌더링.
   - 4개 점 사이의 원근 투영(Bilinear Interpolation / Projective Mapping)을 통해 15열 × 2행의 내부 격자선 30개 구역을 원근 왜곡된 카메라 원본 화면 상에 실시간으로 왜곡 보정된 형태로 오버레이.
3. **OpenCV.js 기반 원근 변환(Perspective Warp) 엔진:**
   - 입력 소스 프레임에서 4점을 `srcCoords`로 취하고, 정규화된 직사각형 크기(예: `WARP_W = 600, WARP_H = 160`)를 `dstCoords`로 지정.
   - `cv.getPerspectiveTransform(srcTri, dstTri)`로 $3 \times 3$ 호모그래피 변환 행렬($M$) 계산.
   - `cv.warpPerspective`를 수행하여 왜곡 없는 반듯한 평면 이미지($W \times H$) 추출.
   - 평면 이미지 상에서 균등한 15x2 그리드로 분할하여 `inspect_single_box`를 호출함으로써 왜곡 없이 정밀한 전도 판별 수행.

### F-2. ROI 설정값 영구 자동 저장 및 복원 (Persistence)
1. **브라우저 자동 영구 보관 (Local Storage):**
   - 4개 꼭짓점 이동 시 즉시 `localStorage`에 자동 동기화 (`key: box_tilt_roi_4points`).
   - 페이지 새로고침 또는 브라우저 재실행 시 저장된 4점 좌표가 1초 내 자동 로드되어 즉각 적용.
2. **`roi_config.json` 파일 저장 및 내보내기/가져오기 (Export/Import):**
   - [💾 설정 저장(JSON 다운로드)] 버튼 제공: 현재 4개 모서리 좌표 및 캔버스 해상도 메타데이터를 담은 `roi_config.json` 파일 생성 및 저장.
   - [📂 설정 불러오기(JSON 업로드)] 버튼 제공: 백업된 `roi_config.json`을 업로드하여 즉각 4개 지점 복원.
   - 프로젝트 디렉토리에 기본 `roi_config.json` 파일을 생성해두어 초기 세팅 기본값으로 활용.

---

## 3. 제약 조건 및 비기능 요구사항
- **성능:** 초당 30fps 비디오 루프에서 매 프레임 변환 행렬 재계산이 아닌, 4점 변경 시에만 행렬을 캐싱하여 렌더링 딜레이 0 유지.
- **호환성:** 가로/세로 모드 및 시뮬레이션 모드/웹캠 모드 모두 100% 호환.
- **안정성:** 메모리 누수 방지를 위해 OpenCV `cv.Mat` 객체들은 `delete()`로 적절히 해제 관리.
