# Git 커밋 메시지를 효율적으로 쓰는 법: 커밋 메시지 컨벤션

<img src="https://imgs.xkcd.com/comics/git_commit.png" title="" alt="" data-align="center">

```
Fix: 로그인 버그 해결 #123

- 사용자 로그인 시 발생하는 버그 수정
- 로그인 페이지에서 입력 필드의 유효성을 검사하는 로직 추가
- 버그를 해결하여 사용자 인증 과정이 원활하게 동작

Closes #120
```

## 커밋 메시지가 중요한 이유

- 코드 리뷰 시간을 단축하고 효율적으로 처리하기 위해.
- 변경 사항을 이해하는 데 도움을 주기 위해.
- "왜 이렇게 했을까?"와 같은 코드만으론 설명하기 어려운 부분을 설명하기 위해.
- 추후 작업자가 변경 사항의 이유와 방식을 이해하고 문제 해결과 디버깅을 용이하게 하기 위해.

## 커밋 메시지 구조

```
<type>[scope]: <subject>    -- 헤더, 필수

<body>                -- 본문

<footer>            -- 바닥글
```

type

필수. 변경사항의 유형

- feat : 새로운 기능 추가, 기존의 기능을 요구 사항에 맞추어 수정
- fix : 기능에 대한 버그 수정
- build : 빌드 관련 수정
- chore : 패키지 매니저 수정, 그 외 기타 수정 ex) .gitignore
- ci : CI 관련 설정 수정
- docs : 문서(주석) 수정
- style : 코드 스타일, 포맷팅에 대한 수정
- refactor : 기능의 변화가 아닌 코드 리팩터링 ex) 변수 이름 변경
- test : 테스트 코드 추가/수정
- release : 버전 릴리즈

scope

선택. 변경된 위치 표시

subject

필수. 아래에 있는 작성 원칙에 따라 써야함.

body

선택. 제목만으로는 표현할 수 없는 자세한 설명

footer

선택. 작업과 관련된 이슈 번호, 참조 링크

## Git 커밋 메시지 작성의 원칙

1. 제목과 본문은 빈 행으로 구분하라
2. 제목은 최대 50글자로 제한하라.
3. 제목의 첫 글자는 대문자로 작성하라. (영어)
4. 제목의 끝에는 마침표를 넣지 마라.
5. 제목은 명령문으로 작성하라. 과거형을 사용하지 마라.
6. 본문의 각 줄은 최대 72글자로 제한하라.
7. 설명할 때 "어떻게"보다는 "무엇을"하고 "왜"에 집중하라.
8. 설명할 때 소스코드를 보지 않고도 변경 사항이 무엇을 하는지 알 수 있도록 하라
9. 뭉뚱그리지말고, 맥락을 알 수 있게 작성하라. 
10. 한 가지 언어만 사용하라

#### 제목과 본문은 빈 행으로 구분하라

```
Fix: 로그인 버그 해결 #123

- 사용자 로그인 시 발생하는 버그 수정
- 로그인 페이지에서 입력 필드의 유효성을 검사하는 로직 추가
- 버그를 해결하여 사용자 인증 과정이 원활하게 동작

Closes #120
```

#### 제목은 명령문으로 작성하라. 과거형을 사용하지 마라

```
# 좋은 예시
InventoryBackendPool을 사용하여 재고 백엔드를 검색합니다
---
Use InventoryBackendPool to retrieve inventory backend

# 나쁜 예시
InventoryBackendPool을 사용하여 재고 백엔드를 검색했습니다
---
Used InventoryBackendPool to retrieve inventory backend
```

왜 명령형을 써야 할까?

커밋 메시지는 변경된 내용 자체가 아니라, 변경 사항이 코드에 어떤 영향을 미치는지를 설명해야하기 때문이다.

즉 변경 사항이 실제로 무엇을 하는지를 설명해야한다.

// 잘 이해가 안 가는데, 누가 설명좀

#### 설명할 때 "어떻게"보다는 "무엇을"하고 "왜"에 집중하라.

```
# 좋은 예시
InventoryBackend 자식 클래스의 메소드 이름 수정

InventoryBackend를 상속받는 클래스가 기반 클래스의 인터페이스를 따르지 않음.

Cart가 잘못된 방식으로 백엔드 구현을 호출하고 있었기 때문에 문제가 없었음.
---
Fix method name of InventoryBackend child classes

Classes derived from InventoryBackend were not
respecting the base class interface.

It worked because the cart was calling the backend implementation
incorrectly.
```

#### 설명할 때 소스코드를 보지 않고도 변경 사항이 무엇을 하는지 알 수 있도록 하라

```
# 좋은 예시
Credit 모델에 `use` 메소드 추가
---
Add `use` method to Credit model

# 나쁜 예시
`use` 메소드 추가
---
Add `use` method


# 좋은 예시
텍스트 상자와 레이아웃 프레임 사이 왼쪽 간격 늘림
---
Increase left padding between textbox and layout frame

# 나쁜 예시
CSS 조정
---
Adjust css
```

#### 뭉뚱그리지말고 맥락을 알 수 있게 작성하라

```
# 나쁜 예시
이거 고침

뭔가 고침

이제 잘 작동할거임

뭔가 변경함

CSS 조정
---
Fix this

Fix stuff

It should work now

Change stuff

Adjust css
```

많은 사람이 이렇게 커밋 메시지를 작성할 것이다. 반성하자. 일단 나부터 ㅋㅋ

#### 한 가지 언어만 사용하라

```
# 좋음
ababab Add `use` method to Credit model
efefef Use InventoryBackendPool to retrieve inventory backend
bebebe Fix method name of InventoryBackend child classes

# 좋음 (한국어 예시)
ababab Credit 모델에 `use` 메소드 추가
efefef InventoryBackendPool을 사용하여 재고 백엔드를 검색합니다
bebebe InventoryBackend 자식 클래스의 메소드 이름 수정

# 나쁨 (영어와 한국어 혼용)
ababab Credit 모델에 `use` 메소드 추가
efefef Use InventoryBackendPool to retrieve inventory backend
cdcdcd 이제 잘 작동할거임
```

프로젝트 소유자인 경우:

모든 커밋을 한 가지 언어를 사용해서 작성해야함.

코드 주석과 기본 언어 파일 (다국어 지원 프로젝트의 경우) 등 모두 같은 언어이어야 함.  

기여자의 경우:

커밋 히스토리에서 사용되고 있는 언어를 사용하여 커밋 메시지를 작성해야함.

## 출처

[xkcd: Git Commit](https://xkcd.com/1296/)

[How to Write a Git Commit Message](https://cbea.ms/git-commit/)

[commit-messages-guide/README_ko-KR.md at master · RomuloOliveira/commit-messages-guide · GitHub](https://github.com/RomuloOliveira/commit-messages-guide/blob/master/README_ko-KR.md)

[Git 커밋 메시지 컨벤션은 왜 중요할까? | 요즘IT](https://yozm.wishket.com/magazine/detail/1974/)

[[Git] Git 커밋 메시지를 효율적으로 쓰는 법: 커밋 메시지 컨벤션 :: ※뱀표_코딩※](https://baemsul.tistory.com/123)
