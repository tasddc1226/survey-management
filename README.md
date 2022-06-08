## open-gallery-2022

### 프로젝트 목표
- 설문지 CRUD 관리자 페이지
- 특정 설문지에 대한 사용자 페이지

### 프로젝트 사용 기술
- ES6
- Django

### 요구사항 분석
- 새로운 설문지 추가
    - [x] 제목, 원하는 유형의 문항을 원하는 개수만큼 생성
    - [x] 특정 문항을 삭제할 수 있도록
    - [x] 각 문항은 제목과 두 개 이상의 선택지 작성
    - [x] 문항의 유형(type)은 Checkbox(1개 이상), Radio(1개), Select(1개) 중 하나
    
- 기존 설문지 수정
    - 새로운 설문지를 추가하는 UI/UX와 동일하게 구현
    - [x] 설문지가 비활성화 상태인 경우에만 수정할 수 있도록 구현

- 관리자 페이지
    - 설문지 목록 페이지
        - [x] 모든 설문지의 정보를 테이블 형식으로 조회
        - [x] 각 설문지의 제목, 문항 수, 응답자 수 등을 조회
            - 특정 설문지에 대한 detail 페이지에서 확인 가능
        - [x] 특정 설문지를 수정 혹은 삭제하는 버튼 구현
        - [x] 사용자에게 보낼 링크를 복사하는 버튼 구현
            - 특정 설문지에 대한 detail 페이지에서 url 확인 가능
        - [x] 삭제 버튼 클릭 시 경고(alert)와 함께 삭제 후 Refresh
        - (추가로) 설문지의 제목 or 설문지의 질문을 기준으로 키워드 검색 기능 + 페이지네이션 기능

    - 설문지 상세 페이지
        - [x]] 각 문항의 선택지 별 응답 비율과 같은 통계 정보 조회
        - (추가로) 특정 설문지의 정보를 CSV 파일로 저장할 수 있는 기능

- 사용자 페이지
    - [x] 특정 설문지를 대상으로 설문을 진행
    - [] 각 항목에 응답 후, 전화번호를 입력한 후 제출
        - User 및 인증, 인가 불필요, admin만 사용
    
