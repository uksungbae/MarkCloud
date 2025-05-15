# MarkCloud

마크클라우드 백엔드 개발자 과제 - 상표 검색 API 서비스

## 1. API 사용법 및 실행 방법

### 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt


# 환경 변수 설정 (.env 파일 생성)

```

### 서버 실행

```bash
uvicorn main:app --reload
```

### API 엔드포인트

- **상표 상세 조회**: `/products/{product_id}` (GET)
- **상표 필터링 검색**: `/products/filter` (GET)
- **유사 키워드 검색**: `/products/search/similar` (GET)
- **상표 상태별 카운트**: `/products/status/counts` (GET)

### API 문서

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 2. 구현된 기능 설명

### 상표 데이터 조회
- **ID 기반 조회**: 특정 상표 ID로 상세 정보 조회
- **필터링 검색**: 전체 필드를 기준으로 필터링

### 유사 키워드 검색
- **유사 키워드 검색**: MongoDB Atlas Search를 활용한 퍼지 검색 구현
  - 오타 허용 (최대 2글자까지 편집 거리 허용)
  - 첫 글자 일치 요구 (prefixLength=1)
  - 관련성 점수 기반 정렬
  - 최소 점수 필터링으로 품질 관리

### 데이터 집계
- **상태별 카운트**: 상표 등록 상태별 개수 집계 API

## 3. 기술적 의사결정에 대한 설명

### 기술 스택 선택
- **FastAPI**: 비동기 처리와 자동 문서화 기능을 활용하기 위해 선택
- **MongoDB**: 상표 데이터의 유연한 스키마와 Atlas Search 기능을 활용하기 위해 선택
- **Motor**: 비동기 MongoDB 드라이버로 FastAPI와의 호환성 확보

### 아키텍처 설계
- **계층 분리**: API 라우트, CRUD 로직, 데이터 모델을 분리
- **비동기 처리**: 모든 데이터베이스 I/O 작업을 비동기로 구현하여 성능 최적화
- **Pydantic 모델**: 요청 및 응답 데이터 검증을 위한 스키마 정의

### 유사 키워드 검색 구현
- **Atlas Search**: 텍스트 검색을 위한 MongoDB Atlas Search 인덱스 활용
- **복합 검색 전략**: 여러 검색 조건을 조합하여 정확도와 다양성 확보
- **가중치 부여**: 검색 조건별 중요도에 따라 가중치 차등 적용

## 4. 문제 해결 과정 및 개선점

### 해결한 문제들
- **무한 재귀 오류**: 함수 이름 충돌로 인한 무한 재귀 문제 해결 (별칭 사용)
- **응답 검증 오류**: Pydantic 모델에 필수 필드 추가 (total 필드)

### 개선하고 싶은 부분(대량 데이터 처리 중점으로..)
- **Elasticsearch 도입**: 대용량 데이터 처리를 위한 검색 인덱스 구축
- **캐싱 시스템**: 자주 요청되는 검색 결과에 대한 캐싱 도입
- **페이지네이션 개선**: 페이지네이션으로 대용량 데이터 처리 효율화
- **API 버전 관리**: API 버전 관리 체계 도입으로 안정적인 업데이트 지원

### 확장 가능성
- **사용자 맞춤형 추천**: 사용자 검색 패턴 기반 상표 추천 시스템
