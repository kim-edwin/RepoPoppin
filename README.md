# :pushpin: poppin
![팝핀 로고](https://github.com/limmyou/poppin/assets/145823967/3b759ff6-3757-4474-a767-b29cb5459d8b)

\# 팝핀

"팝핀"은 **팝업 스토어 데이터를 한 곳에 모아 검색 및 저장**하고, 저장된 팝업스토어를 기반으로 **새로운 팝업 스토어를 추천**받을 수 있는 `팝업 스토어 정보 저장 & 추천 모바일 웹 서비스`입니다

[:arrow_right:팝핀 바로가기](https://pop-pin.store/) 

:family: **TEAM**
---
|[:crown:김현우](https://github.com/kim-edwin)|[:smiley_cat:강희림](https://github.com/limmyou) |[:hatching_chick:장경민](https://github.com/wkdrudals)|[:rabbit:이윤아](https://github.com/YoooonaLee)|[:pizza:최민환](https://github.com/Hwannni)|
|:---:|:---:|:---:|:---:|:---:|
|![남자미모티콘](https://github.com/limmyou/poppin/assets/145823967/de192276-80e5-43e6-962e-25f906ad28d6)|![여자미모티콘](https://github.com/limmyou/poppin/assets/145823967/cb38a500-5672-40cc-a331-e518697b66aa)|![여자미모티콘](https://github.com/limmyou/poppin/assets/145823967/cb38a500-5672-40cc-a331-e518697b66aa)|![여자미모티콘](https://github.com/limmyou/poppin/assets/145823967/cb38a500-5672-40cc-a331-e518697b66aa)|![남자미모티콘](https://github.com/limmyou/poppin/assets/145823967/de192276-80e5-43e6-962e-25f906ad28d6)|
|`배포`, `Front-end`, `Back-end`|`Data Cleansing`|`Back-end`|`Back-end`|`Back-end`|
|`Render`, `React`, `Django`, `AWS`|`MariaDB`|`Airflow`|` `|` `|

**:calendar: 프로젝트 기간**
---
> 2024년 2월 19일 ~ 2024년 3월 22일

**:page_facing_up: 목차**
---

- [1. 프로젝트 개요](#1.-프로젝트-개요)
  - [프로젝트 시나리오](#프로젝트-시나리오)
  - [주요 기능](#주요-기능)
  - [기획 과정](#기획-과정)
 
- [2. 요구사항 정의](#2.-요구사항-정의)
  - [시나리오](#시나리오)
  - [요구사항 정의서](#요구사항-정의서)
    
- [3. 개발](#3.-개발)
  - [기술스택](#기술스택)
  - [UI](#ui)
  - [API](#api)

- [5. 회고](#5.-회고)
  - [한계점](#한계점)
  - [느낀점](#느낀점)

## 1. 프로젝트 개요
  ### 프로젝트 시나리오
<details><summary>프로젝트 시나리오</summary>
  
<div align="center">팝업스토어 키워드 검색량 추이</div>
<img width="1100" alt="팝업스토어 검색량 추이" src="https://github.com/limmyou/poppin/assets/145823967/8cb61201-1cd6-4915-a5ca-776ae2f7d681">

[현황]
>~~최근 팝업스토어가 새로운 마케팅 트렌드로 주목받고 있다. 이에 따라 고객들이 팝업 스토어를 찾는 수요가 증가하고 있다.~~

[한계]
>~~고객(개인)은 원하는 팝업 스토어를 찾기 위해 직접 웹사이트나 SNS를 탐색해야 한다. 또한, 고객(기업)은 뉴스나 소규모 SNS 마케팅 채널에 의존하여 팝업스토어를 홍보해야 한다.~~

[솔루션]
>~~팝업 스토어에 대한 종합적인 정보를 제공하고 추천하는 모바일 웹 서비스 구축함으로써, 고객들이 원하는 팝업 스토어를 손쉽게 찾을 수 있도록 지원하며, 개인화된 추천 시스템을 통해 고객들의 취향과 관심사에 맞는 새로운 팝업 스토어를 발견할 수 있도록 한다.~~  

</details>

  ### 주요 기능
<details><summary>주요 기능</summary><br>

**:circus_tent:팝업 스토어 정보 확인**  
```
현재 진행중인 팝업 스토어 
향후 예정 팝업 스토어 
지난 팝업 스토어 
```
**:mag_right:팝업 스토어 상세 정보 확인** 
```
팝업 스토어 상세 정보 & 원문 기사 
PIN 기능 → 위시리스트 
리뷰 + 평점 
URL 공유 
```
**:part_alternation_mark:팝업 스토어 추천 기능** 
```
아이템 기반 추천 
→ 팝업스토어 간의 유사도로 추천 

사용자 기반 추천 
→ 사용자의 조회이력, 패턴 등을 분석하여 예측하고 추천 
```
**:triangular_flag_on_post:팝업 스토어 지도 기능** 
```
팝업 스토어의 위치 보여주기 
```
**:hearts:위시리스트** 
```
좋아요 한 스토어 보기 
```
</details>

  ### 기획 과정
<details><summary>기획 과정</summary><br>
  
1. Notion 문서 [바로가기](https://www.notion.so/bad6778516b340408f10a3f7def106a8?pvs=4)
![노션](https://github.com/kim-edwin/RepoHeart/assets/145823967/f1d5fa4b-fb96-41c5-8584-a5e47983c907)

2. WBS [바로가기](https://docs.google.com/spreadsheets/d/1B9ElpTqgXPPfNXbQ8e2fhkwKi8PkeVj9/edit#gid=1081654881)
<img width="755" alt="WBS" src="https://github.com/limmyou/poppin/assets/145823967/fb2bdbd4-bb63-4102-b4ce-1920d1e76e87">

</details>

## 2. 요구사항 정의
  ### 시나리오
<details><summary>시나리오</summary>

:raising_hand:**우리 서비스를 이용할 유저들**
```
연인과의 데이트 또는 친구들과 시간을 보낼 곳을 찾는 유저
모바일 접속 유저
```
1) 장소와 시간이 결정되지 않은 유저 → :bulb:**현재 오픈 중인 팝업스토어를 탐색할 수 있는 기능** 필요
  → 카테고리제이션을 통한 목록 탐색,  현재 실시간 인기 많은 팝업스토어 노출, 가장 최신 팝업스토어 노출

3) 장소와 시간이 결정된 유저 → :bulb:**이들을 위해 장소, 시간, 키워드 검색 기능** 필요
   
:heavy_exclamation_mark:**이에 따라, 유저들이 우리 사이트에 기대할 필수적인 요소**
1. 진행중인 팝업스토어 목록 조회
2. 팝업스토어의 정보와 방문 후기
3. 링크 공유 

:heavy_exclamation_mark:**추가적으로, 유저들이 우리사이트에서 발견하고 좋다고 느낄만한 내용**

1. (상세페이지) 현재 조회 중인 팝업스토어와 유사한 팝업스토어 추천받기
2. 위시리스트
  
</details>

  ### 요구사항 정의서
<details><summary>요구사항 정의서</summary>

요구사항 정의서 [바로가기](https://repeated-sidewalk-fe0.notion.site/bad6778516b340408f10a3f7def106a8)

</details>

## 3. 개발
  ### 기술스택
<details><summary>기술스택</summary>

기술스택

</details>

  ### UI
<details><summary>UI</summary>

![팝핀 UI1](https://github.com/limmyou/poppin/assets/145823967/0d4d81dc-6c6c-4d3d-a4bd-890a1db157a5)
![팝핀 UI2](https://github.com/limmyou/poppin/assets/145823967/427b6756-8f5f-4b4c-b821-75d944179a09)

</details>

  ### API
<details><summary>API</summary>

API

</details>

## 4. 회고
 ### 한계점
<details><summary>한계점</summary>

:crown:김현우 : 

:smiley_cat:강희림 : 

:hatching_chick:장경민 : 

:rabbit:이윤아 : 

:pizza:최민환 : 

</details>

 ### 느낀점
<details><summary>느낀점</summary>

:crown:김현우 : 

:smiley_cat:강희림 : 

:hatching_chick:장경민 : 

:rabbit:이윤아 : 

:pizza:최민환 : 

</details>
