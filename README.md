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

## API 명세서

| URL| HTTP Method | 논리적 이름 | 물리적 이름 | Permission | parameter | 
|------|----------------|-------------|-------------|-------------|----------------|
|/api/v1/accountbooks|`GET`|가계부 목록 조회|account_book|IsOwner|?status=delete|
|/api/v1/accountbooks|`POST`|가계부 생성|account_book|IsOwner||
|/api/v1/accountbooks/<obj_id>|`GET`|가계부 단건 조회|account_book_detail|IsOwner||
|/api/v1/accountbooks/<obj_id>|`PUT`|가계부 단건 수정, 삭제|account_book_detail|IsOwner||
|/api/v1/accountbooks/<obj_id>/records|`POST`|가계부 기록 생성|record|IsOwner||
|/api/v1/accountbooks/records/<obj_id>|`GET`|가계부 기록 단건 상세 조회|record_detail|IsOwner||
|/api/v1/accountbooks/records/<obj_id>|`PUT`|가계부 기록 단건 수정, 삭제|record_detail|IsOwner||
|/api/v1/users/signup|`POST`|회원가입|signup|Allowany||
|/api/v1/users/signin|`POST`|로그인|siginin|Allowany||

❗️ '/api/v1/accountbooks' api 호출시, 가계부 목록과, 각 가계부에 기록된 내역들을 함께 보여줍니다. <br>
❗️ '/api/v1/accountbooks' api에 <b>status=delete</b>파라미터를 추가하면 삭제된 가계부 목록을 보여줍니다.<br>
❗️ 가계부 목록, 가계부 단건 조회할 때, 가계부에 기록된 내역들의 금액을 합산한 값은 <b>total_balance</b>필드를 생성하여 보여줍니다. <br>
❗️ 가계부, 가계부 기록 삭제 api의 http 메소드가 `PUT`인 이유는 <b>soft delete</b>하기 위함입니다. <br>
&nbsp; &nbsp; &nbsp; 삭제된 내역은 언제든지 복구할 수 있어야 하기 때문에 DB에서 실제로 데이터를 삭제하는것이 아닌, 각 모델의 <b>is_deleted</b>필드를 False 에서 True로 &nbsp; &nbsp; &nbsp; &nbsp; 수정하게 됩니다. <br>
❗️ 가계부, 가계부 기록은 is_deleted 필드가 False인 것만(삭제되지 않은 것만)유저에게 보여줍니다. <br>

➡️ [스웨거 링크]()

<details>
<summary>Postman 테스트 결과</summary> 
<div markdown="1">
이 부분은 리팩토링 후에 첨부할 예정입니다. 스웨거 작성이 잘 되어있다면, 스웨거 캡쳐본으로 대신해도 될것 같습니다.
</div>
</details>

<br>

## 📋 ERD
![erd](https://user-images.githubusercontent.com/76423946/177769143-5ce7e3c0-1767-4d9f-869c-107e8f9e32d0.png)
- User : 유저 정보를 저장합니다.
- AccountBook : 가계부 정보를 저장합니다.
- AccountBookRecord : 각 가계부에 수입, 지출 내역을 저장합니다.

❗️ User 모델은 장고의 기본 User 모델을 그대로 사용하지 않고 커스텀하였습니다. <br>
(혹시 커스텀한 이유에 대해 멋지게 풀어내실 수 있으면 내용 추가해주시면 감사하겠습니다! 제가 잘 써보려고 했는데 어렵네요,,ㅠ)<br>
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
훈희님께서 내용 채워주시면 좋을것 같아요 :)

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

