# 2023-2-OSSP1-CrashLandingOnYou-6
2023년 2학기, 공개SW프로젝트, 01분반, 사랑의 불시착 팀, 6조

# 공개SW프로젝트_01 - 사랑의 불시착

# 🤹‍♀️ 팀 구성원

### 👨‍💻 임사랑 @milevol

### 👨‍💻 곽시헌 @kkhoney

### 👨‍💻 전희연 @2rayija

### 👨‍💻 남민지 @SouthMinji

# 📌기존 프로젝트 소개

- 1인가구 레시피 추천 웹, 혼자서도 잘해요리

- 이 프로젝트는 사용자들이 레시피를 찾고, 공유하며, 소통할 수 있는 웹 기반 플랫폼입니다. 

- 주요 기능으로는 회원가입 및 로그인, 레시피 조회, 레시피 작성, 레시피 추천, 레시피 댓글 및 상호작용, 그리고 마이 페이지 관리가 있습니다. 

- 레시피 추천시 재료와 조리 과정을 함께 고려한 이중 추천 시스템을 이용하여 레시피 추천의 다양성과 정확성을 제공합니다.

# 📌기술스택

## 백엔드

<div style="display:flex">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">
</div>

## 프론트엔드

<div style="display:flex">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">
</div>

## 데이터베이스

<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white">

## 기존 프로젝트 기능 요약
![혼자서도 잘해요리 메인1](https://user-images.githubusercontent.com/61997714/185313870-7d35923f-d6a4-4e83-8cbe-67ff324f760f.gif)
![혼자서도잘해요리 상세페이지](https://user-images.githubusercontent.com/61997714/185320540-e293b468-3841-4a1e-b921-8ad669055f42.gif)
![혼자서도 잘해요리 나만의레시피](https://user-images.githubusercontent.com/61997714/185320657-c82b5f27-4073-4e2c-811b-42ed471f9195.gif)
![혼자서도잘해요리 댓글](https://user-images.githubusercontent.com/61997714/185320720-9170f77e-0825-4ec9-8640-cf80724738a4.gif)

# 📌프로젝트 구조

## 프로젝트 아키텍쳐

- 혼자서도 잘해요리는 서버 사이드 렌더링으로 EC2를 통하여 프론트와 백엔드가 모두 한 번에 구현되었습니다.

## 서비스 플로우

### 회원기능

- 사용자는 사이트 자체에서 회원가입과 로그인을 사용하여 웹에 접근할 수 있습니다.
- 회원가입은 아이디, 비밀번호, 닉네임을 기입하여 회원가입 버튼을 클릭해서 회원 데이터를 저장합니다.

### 레시피 조회

- 사용자는 작성된 레시피의 목록을 조회하고, 목록 중 원하는 레시피 카드를 클릭하여 레시피의 상세 내용을 볼 수 있습니다.
- 사용자는 조회한 레시피의 재료 및 조리시간, 난이도, 조리순서 등을 확인할 수 있습니다.
- 사용자는 검색, 정렬, 필터 기능을 사용하여 원하는 레시피를 찾아서 확인할 수 있습니다.
- 2000여개에 달하는 레시피를 서버 부하를 줄이며 보여주기 위해 장고 페이지네이션 기능을 사용했습니다.

### 레시피 작성

- 로그인 한 사용자는 이미지를 포함한 레시피를 작성할 수 있습니다

### 레시피 추천
-  사용자가 관련된 레시피를 추천받기를 원하는 레시피를 클릭하면 5개의 재료기반, 조리 과정 기반 추천 레시피를 제공합니다.

### 레시피 댓글 작성

- 로그인 한 사용자는 다른이용자가 작성한 게시물에 댓글을 작성 할 수 있으며, 좋아요도 달 수 있습니다

### 마이페이지

- 내가 작성한 글, 댓글, 북마크한 요리를 모아볼 수 있습니다
  
# 📌프로젝트 알고리즘 작동 방식 개선
![메인서브](https://github.com/CSID-DGU/2023-2-OSSP1-CrashLandingOnYou-6/assets/92575773/41d72ff8-c5ed-4899-b099-d752cde68067)
![추천](https://github.com/CSID-DGU/2023-2-OSSP1-CrashLandingOnYou-6/assets/92575773/9cd7974e-1483-4c5d-b238-4ce06b3a221d)

- 프로젝트의 알고리즘 작동 방식은 데이터베이스 관리 및 사용자 입력 처리에 초점을 맞추고 있습니다.

- 데이터베이스에는 레시피 정보를 저장하는 테이블이 존재하며, 이 테이블은 레시피의 고유 번호(id), 이름(title), 이미지 URL(img_url), 조리 시간(timecost), 난이도(difficulty), 조리 단계(cookstep), 작성자 ID(author_id), 생성 및 업데이트 날짜(created_at, updated_at) 그리고 메인 및 서브 재료(main_ingredients, sub_ingredients) 등을 포함합니다. 이 데이터는 레시피 식별, 분류 및 추천에 활용됩니다.

- 사용된 데이터는 '만개의 레시피' 웹사이트에서 크롤링한 것으로, 특히 조리 방법별 레시피 데이터에 중점을 두고 분석합니다. 사용자 입력 데이터는 레시피명, 조리 시간, 난이도, 조리 과정, 이미지 및 재료 정보를 포함하며, 이를 통해 레시피를 자동으로 분류하고 정규화합니다.

### 추천 알고리즘
- 추천 알고리즘은 두 단계로 구성됩니다.
  
- 첫 번째 단계에서는 유사한 재료를 사용하는 레시피를 추천하며, 메인 재료와 서브 재료의 유사도에 따라 추천 순위를 결정합니다.

- 두 번째 단계에서는 첫 번째 단계의 단점을 보완하여 조리 분류(classification)를 고려한 레시피 추천을 진행합니다.

- '조리 분류 유사 레시피 추천 알고리즘'은 기존 레시피 데이터에서 동사와 조리 분류 간의 관계를 분석하고, 각 조리 분류별로 동사의 출현 빈도를 계산하여 조건부 확률을 도출합니다. 이 확률은 특정 동사가 주어졌을 때, 그 동사가 특정 조리 과정에 속할 확률을 나타냅니다.

- TF-IDF 기법을 사용하여 빈도가 낮은 동사의 문제를 해결하고, 데이터의 표준편차 역수를 이용해 가중치를 계산합니다.

이를 통해 조건부 확률과 TF-IDF를 통합하는 가중평균을 구하며, 이를 기반으로 각 조리 분류별 상위 100개의 동사 리스트를 생성합니다.

- 식재료 사전은 사용자 입력의 정규화를 위해 구축되며, 식재료의 다양한 표현을 표준화합니다.

이 사전은 식품명, 품종, 종류, 가공형태 등 다양한 열로 구성되어 있으며, 사용자 입력의 다양성에 대응하기 위해 사용됩니다. 

이 사전을 사용하여 메인재료와 서브재료를 정규화하며, 정규화된 결과는 데이터베이스의 정규화 열에 저장됩니다.

- 마지막으로, 재료 기반 유사 레시피 추천을 위해 메인 재료와 조리 과정을 겹치는 레시피를 추출하고, 이 중에서 서브 재료가 가장 많이 겹치는 순서로 레시피를 추천합다.


# 📌[Starting Assignment](https://github.com/tunEmvegnomb/cook_alone/wiki/Project-Starting-Assignment)
