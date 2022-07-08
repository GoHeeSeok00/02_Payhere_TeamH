# 02_Payhere_TeamH
## ✅ 서비스 개요
- 가계부를 생성하여 수입과 소비내역을 관리(작성, 수정, 삭제)할 수 있습니다. <br>
- 삭제한 내역은 언제든지 다시 복구할 수 있습니다.<br>
- 각 내역들의 금액을 합산하여 총 금액을 보여줍니다.

<br>

## 📌 과제 분석
<div>
<details>
<summary>과제소개</summary> 
<div markdown="1">
🗣고객은 본인의 소비내역을 기록/관리하고 싶습니다.<br>
아래의 요구사항을 만족하는 DB 테이블과 REST API를 만들어주세요.
</div>
</details>

<details>
<summary>요구사항</summary> 
<div markdown="1">
<ul>
  <li>고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.</li>
  <li>고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.</li>
  <li>고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다.</li>
    <ul>
      <li>가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.</li>
      <li>가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.</li>
      <li>가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.</li>
      <li>삭제한 내역은 언제든지 다시 복구 할 수 있어야 한다.</li>
      <li>가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.</li>
      <li>가계부에서 상세한 세부 내역을 볼 수 있습니다.</li>
    </ul>
  <li>로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.</li>
</ul>
</div>
</details>
</div>

#### ➡️ 분석결과
과제 요구사항을 최소한으로 충족시키려면 사용자의 가계부에 <b>소비내역</b>만을 기록, 관리할 수 있는 기능을 개발하는 것이라고 판단했습니다. <br>
하지만 저희는 <b>가계부</b>에 초점을 두고, 지출 내역만이 아닌, 수입 내역도 함께 관리하고 그에 따른 총 금액도 보여주도록 추가 기능을 개발하였습니다.

<br>

## 🛠 사용 기술
- API<br>
![python badge](https://img.shields.io/badge/Python-3.9-%233776AB?&logo=python&logoColor=white)
![django badge](https://img.shields.io/badge/Django-4.0.6-%23092E20?&logo=Django&logoColor=white)
- DB<br>
![mysql badge](https://img.shields.io/badge/MySQL-8.0.29-%234479A1?&logo=MySQL&logoColor=white)

- 배포<br>
![aws badge](https://img.shields.io/badge/AWS-EC2-%23FF9900?&logo=Amazon%20EC2&logoColor=white)
![docker badge](https://img.shields.io/badge/Docker-20.10.17-%232496ED?&logo=Docker&logoColor=white)
![nginx badge](https://img.shields.io/badge/Nginx-1.23.0-%23009639?logo=NGINX&locoColor=white)
![gunicorn badge](https://img.shields.io/badge/Gunicorn-20.1.0-%23499848?logo=Gunicorn&locoColor=white)
- ETC<br>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white"/>
  <img src="https://img.shields.io/badge/Github action-2088FF?style=flat&logo=Github%20Actions&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jira-0052CC?style=flat&logo=Jira&logoColor=white"/>

<br>

## :black_nib: 이슈 관리
<img width="1419" alt="image" src="https://user-images.githubusercontent.com/95380638/177978324-bfa68bc2-1f9b-418c-9236-ab9760c364f4.png">

<br>

## 🌟 API 명세서
<img width="1008" alt="스크린샷 2022-07-08 오후 7 03 34" src="https://user-images.githubusercontent.com/76423946/177969327-b359e65d-47f6-406e-b465-57b719ee6edd.png">

❗️ '/api/v1/accountbooks' api 호출시, 가계부 목록과, 각 가계부에 기록된 내역들을 함께 보여줍니다. <br>
❗️ '/api/v1/accountbooks' api에 <b>status=delete</b>파라미터를 추가하면 삭제된 가계부 목록을 보여줍니다.<br>
❗️ '/api/v1/accountbooks' api를 `POST`로 요청 시, 가계부를 생성합니다.<br>
❗️ 가계부 목록, 가계부 단건 조회할 때, 가계부에 기록된 금액은 <b>balance</b>, 해당 일자까지의 금액을 합산한 값은 <b>total_balance</b>필드를 생성하여 보여줍니다. <br>
❗️ 가계부, 가계부 기록 삭제 api의 http 메소드가 `PATCH`인 이유는 <b>soft delete</b>하기 위함입니다. <br>
&nbsp; &nbsp; &nbsp; 삭제된 내역은 언제든지 복구할 수 있어야 하기 때문에 DB에서 실제로 데이터를 삭제하는것이 아닌, 각 모델의 <b>is_deleted</b>필드를 False 에서 True로 수정하게 됩니다. <br>
❗️ 가계부 단건 및 가계부 기록 단건 복구 시, <b>recovery</b>를 붙여 구분합니다.<br>
❗️ 가계부, 가계부 기록 수정 api의 메소드는 `PUT`이지만 코드상 <b>partial</b> 옵션을 주어 부분적 수정도 가능합니다.<br>
❗️ 가계부, 가계부 기록은 is_deleted 필드가 False인 것만(삭제되지 않은 것만)유저에게 보여줍니다. <br>



<details>
<summary>Postman 테스트 결과</summary> 
<div markdown="1">
<ul>
  <li>
    <p>회원가입</p>
    <img width="828" alt="스크린샷 2022-07-08 오후 7 07 46" src="https://user-images.githubusercontent.com/76423946/177971406-9225e64c-bf9a-4e66-a72e-95edad7cc086.png">
  </li>
  <li>
    <p>로그인</p>
    <img width="828" alt="image" src="https://user-images.githubusercontent.com/95380638/177974085-0fdb702b-3db3-40a7-a1ef-66fa1976abe1.png">
  </li>
  <li>
    <p>가계부 목록 조회</p>
    <img width="888" alt="image" src="https://user-images.githubusercontent.com/95380638/177975927-e4fe4030-36ae-4676-bda5-331b92d05b0f.png">
  </li>
  <li>
    <p>삭제된 가계부 목록 조회</p>
    <img width="897" alt="image" src="https://user-images.githubusercontent.com/95380638/177976069-3324a7f8-a56b-4390-af1c-345fea52ab1d.png">
  </li>
  <li>
    <p>가계부 생성</p>
    <img width="828" alt="image" src="https://user-images.githubusercontent.com/95380638/177974294-501d9934-c5f0-4fe7-8b70-3f32283fa011.png">
  </li>
  <li>
    <p>가계부 조회</p>
    <img width="876" alt="image" src="https://user-images.githubusercontent.com/95380638/177974570-beb1771c-2c75-4c2f-b176-6cf5a12a91e8.png">
  </li>
  <li>
    <p>가계부 수정</p>
    <img width="871" alt="image" src="https://user-images.githubusercontent.com/95380638/177974449-38854e04-8890-4d0d-9b67-dbbed903901b.png">
  </li>
  <li>
    <p>가계부 삭제</p>
    <img width="871" alt="image" src="https://user-images.githubusercontent.com/95380638/177974627-2cb6b140-80a6-42c8-a38d-a1f1ba1524c8.png">
  </li>
  <li>
    <p>가계부 복구</p>
    <img width="877" alt="image" src="https://user-images.githubusercontent.com/95380638/177974744-f4525881-9a90-49cb-811c-617cbf5621a5.png">
    </li>
  <li>
    <p>가계부 기록 생성</p>
    <img width="877" alt="image" src="https://user-images.githubusercontent.com/95380638/177974825-4f15f3de-c781-45aa-a79f-c3532de8efb1.png">
  </li>
  <li>
    <p>가계부 기록 조회</p>
    <img width="881" alt="image" src="https://user-images.githubusercontent.com/95380638/177974942-6ba78e84-ac37-4e5d-b18a-2f33f9c132d5.png">
  </li>
  <li>
    <p>가계부 기록 수정</p>
    <img width="868" alt="image" src="https://user-images.githubusercontent.com/95380638/177975005-5eed224a-63d0-46b8-adbf-fbe226e242d7.png">
  </li>
  <li>
    <p>가계부 기록 삭제</p>
    <img width="874" alt="image" src="https://user-images.githubusercontent.com/95380638/177975062-35706646-c89a-4081-8d4b-580de38a1702.png">
  </li>
  <li>
    <p>가계부 기록 복구</p>
    <img width="875" alt="image" src="https://user-images.githubusercontent.com/95380638/177975102-a0e5433d-3759-4ac8-9a15-6197b35d287b.png">
  </li>
</ul>
</div>
</details>

<br>

## 📋 ERD
<img width="802" alt="erd" src="https://user-images.githubusercontent.com/76423946/177966917-96fa08b7-8849-4443-ae4f-d67421e19dc1.png">

- User : 유저 정보를 저장합니다.
- AccountBook : 가계부 정보를 저장합니다.
- AccountBookRecord : 각 가계부에 수입, 지출 내역을 저장합니다.

❗️ User 모델은 장고의 기본 User 모델을 그대로 사용하지 않고 커스텀하였습니다. <br>
❗️ 한 명의 유저는 여러개의 가계부를 관리할 수 있도록 User 모델과 AccountBook(가계부)모델은 1:N 관계입니다. <br>
❗️ AccountBook 모델과 AccountBookRecord 모델은 1:N 관계로, 한 개의 가계부에 여러 내역을 기록할 수 있습니다. <br>

<br>

## 🌎 배포
Docker, NginX, Gunicorn을 사용하여 EC2 서버에 배포하였습니다. <br>
#### ➡️ [기본 URL](http://54.180.109.16/) <br>
기본 URL은 404 페이지 입니다. <br>
❗️ 현재 비용의 문제로 서버 접속은 불가능합니다.

<br>

## ✔️ Test Case 
서비스하는 모든 API에 대한 TESTCASE 작성 및 수행
![image](https://user-images.githubusercontent.com/89897944/177983110-f846cef3-589e-49ca-b3cf-5a314d4b8cf2.png)

<br>

## 👋 TeamH Members
|Name|Task|Github|
|-----|----|-------|
|고희석|모델링, 가계부 관련 API 개발|https://github.com/GoHeeSeok00| 
|김민지|배포|https://github.com/my970524|
|김상백|가계부 관련 API 개발|https://github.com/tkdqor|
|김훈희|테스트 케이스 작성|https://github.com/nmdkims| 
|이정석|개발환경 셋팅, 유저 관련 API 개발|https://github.com/sxxk2|

➡️ [Payhere 과제 노션 페이지](https://www.notion.so/fa0128e74291482fb103695f735f1d0a)

