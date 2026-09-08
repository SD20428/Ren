################################################################################
# 게임 상태 — 플래그 / 단서 / 엔딩 판정
#
# 주의: 여기 있는 default 변수의 "이름"을 바꾸면 기존 세이브가 깨진다.
#       추가는 안전. 이름 변경/삭제는 위험.
################################################################################

# --- 진행 플래그 --------------------------------------------------------------
default f_saw_photo    = False   # 서랍 속 사진을 봤는가
default f_opened_door  = False   # 지하실 문을 열었는가
default f_told_truth   = False   # 지혜에게 사실대로 말했는가

# --- 수치 -------------------------------------------------------------------
default trust_jihye = 0          # -3 ~ +3
default sanity      = 5          # 0 이 되면 강제 배드엔딩

# --- 챕터 단위 상태 ----------------------------------------------------------
# 챕터가 바뀔 때 begin_chapter() 가 초기화한다. 직접 건드리지 말 것.
default current_chapter  = 0
default jump_scare_used  = False

# --- 단서 -------------------------------------------------------------------
default clues = set()

# 엔딩 해금은 플레이스루가 아니라 설치본 단위로 남아야 한다.
# 그래서 default 가 아니라 persistent 를 쓴다. 아래 init python 에서 초기화한다.


# --- 단서 DB -----------------------------------------------------------------
# 단서 수첩에 표시되는 내용. 이름과 설명만.
init python:

    clue_db = {
        "clue_burnt_letter": (
            "탄 편지",
            "가장자리가 그을렸다. 남은 글자는 세 개뿐이다.",
        ),
        "clue_photo": (
            "사진",
            "네 명이 찍혔는데, 한 명의 얼굴만 긁혀 있다.",
        ),
        "clue_key": (
            "작은 열쇠",
            "지하실 문에는 맞지 않는다.",
        ),
    }


    def add_clue(cid):
        """단서 획득. 중복 호출해도 안전하다."""
        if cid not in clue_db:
            raise Exception("정의되지 않은 단서 ID: %s" % cid)
        if cid not in clues:
            clues.add(cid)
            renpy.notify("단서를 얻었다 — %s" % clue_db[cid][0])


    def has_clue(cid):
        return cid in clues


    def clue_count():
        return len(clues)


    if persistent.unlocked_endings is None:
        persistent.unlocked_endings = set()


    def begin_chapter(n):
        """
        챕터 시작 첫 줄에서 호출한다. 챕터 단위 상태를 초기화한다.
            $ begin_chapter(2)
        """
        store.current_chapter = n
        store.jump_scare_used = False


    def use_jump_scare():
        """
        점프 스케어 사용권. 챕터당 첫 호출만 True.
        OUTLINE 호러 규칙 1(챕터당 최대 1회)을 코드로 강제한다.
            if use_jump_scare():
                $ shake_screen(3)
        """
        if store.jump_scare_used:
            return False
        store.jump_scare_used = True
        return True


    def unlock_ending(name):
        """엔딩 해금. 새 게임을 시작해도 유지된다."""
        if persistent.unlocked_endings is None:
            persistent.unlocked_endings = set()
        persistent.unlocked_endings.add(name)


    def ending_unlocked(name):
        return name in (persistent.unlocked_endings or set())


    def ending_count():
        return len(persistent.unlocked_endings or set())


    def decide_ending():
        """
        엔딩 판정. script.rpy 의 ending_router 에서만 호출한다.
        판정 순서가 곧 우선순위다. 위쪽이 먼저 걸린다.
        """
        if sanity <= 0:
            return "ash"

        # 히든 — 트루 조건을 전부 만족한 위에, 흠집 없이 왔을 때만.
        # sanity >= 4 는 "프롤로그에서 깎인 1 말고는 더 깎이지 않았음" 이라는 뜻이다.
        # 프롤로그의 drain_sanity(1) 때문에 5 는 도달 불가. 4 가 만점이다.
        if (clue_count() >= 3 and f_told_truth and trust_jihye >= 3
                and sanity >= 4 and f_opened_door):
            return "hidden"

        if clue_count() >= 3 and f_told_truth and trust_jihye >= 2:
            return "true"

        if f_opened_door and not f_saw_photo:
            return "ash"

        return "default"
