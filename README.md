# 세팅 순서

이 폴더는 **완성된 Ren'Py 프로젝트가 아니다.** 런처가 만든 프로젝트 위에 얹는 뼈대다.

## 1. Ren'Py SDK 설치

renpy.org 에서 8.x 다운로드 → 압축 해제 → 런처 실행

## 2. 새 프로젝트 생성

런처 → `Create New Project` → 프로젝트 이름 입력 → 해상도 1920x1080 선택

생성된 폴더 안에 `game/` 이 있다. 그 안에 이미
`script.rpy`, `options.rpy`, `gui.rpy`, `screens.rpy` 가 들어있다.

## 3. 이 뼈대 얹기

- 이 저장소의 `game/` 안 파일들을 프로젝트 `game/` 으로 복사
- `script.rpy` 는 **덮어쓴다**
- `options.rpy`, `gui.rpy`, `screens.rpy` 는 **건드리지 않는다** (docs/GUI_TWEAKS.md 참고해서 값만 고친다)
- `CLAUDE.md` 는 프로젝트 루트에 둔다

## 4. 한글 폰트 넣기 — 안 하면 글자가 네모로 나온다

Ren'Py 기본 폰트에는 한글 글리프가 없다. 반드시 넣어야 한다.

1. Pretendard 다운로드 (github.com/orioncactus/pretendard) → `Pretendard-Regular.ttf`
2. 나눔명조 다운로드 (hangeul.naver.com) → `NanumMyeongjo.ttf`
3. 둘 다 `game/fonts/` 에 넣기
4. `docs/GUI_TWEAKS.md` 대로 `gui.rpy` 수정

두 폰트 모두 무료 상업 이용 가능 라이선스(OFL)다.

## 5. git

```
git init
git add .
git commit -m "init: 프로젝트 뼈대"
```

에이전트 붙이기 **전에** 반드시 해라. 안 하면 뭐가 부서졌는지 못 되돌린다.

## 6. 실행

런처에서 `Launch Project`.
프롤로그가 돌아가면 성공.
