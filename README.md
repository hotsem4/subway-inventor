<div align="center">

<img src="https://em-content.zobj.net/source/apple/391/sandwich_1f96a.png" width="110" alt="Subway Sandwich" />

# 🥪 Subway Inventory Dashboard

**실매장 현장의 재고 입력 & 통계 + SMS 부족 알람**

</div>

---

## ✨ 왜 필요할까?

| Pain Point           | 기존 방식             | Dashboard 효과                         |
| -------------------- | --------------------- | -------------------------------------- |
| **수기 재고표**      | 종이·엑셀 따로 관리   | 태블릿 🖱 입력 → 즉시 DB 저장           |
| **발주 기준 헷갈림** | 기준 재고 수기로 계산 | 저장 즉시 ⚠️ 부족·과잉 알람 → SMS 전송 |
| **통계 부재**        | 감으로 발주           | 📊 월별 그래프·CSV → 데이터 기반 발주  |

---

## 🔥 주요 기능

|   구분               |   설명                                                  |
| -------------------- | ------------------------------------------------------- |
| **⚙️ 분류 관리**     | 대·중·소 카테고리 CRUD                                  |
| **📋 재고 입력**     | 태블릿 UI → DB 저장, 기준치 비교 알람                   |
| **📲 SMS 알림**      | Twilio – 기준 미달 / 과잉 시 즉시 사장 폰으로 전송      |
| **📊 통계 대시보드** | 월별 재고 추이, Hover 상세, CSV 다운로드                |
| **🔗 DB 플러그인**   | 기본 SQLite → `DB_URL` 한 줄로 PostgreSQL 전환          |
| **🚀 배포 READY**    | GitHub → Streamlit Community Cloud / Docker 즉시 Deploy |

---

## 🏗️ 기술 스택

| Layer          | Tech                               |
| -------------- | ---------------------------------- |
| **UI**         | Streamlit 1.32 · Plotly Express    |
| **ORM/DB**     | SQLAlchemy 2 · SQLite / PostgreSQL |
| **SMS**        | Twilio REST API                    |
| **Auth(옵션)** | Streamlit session state + bcrypt   |
| **DevOps**     | GitHub Actions · Dockerfile        |

---

## 🗂 폴더 구조

```text
subway_inventory/
├── .streamlit/
│   └── secrets.toml   # DB_URL, TWILIO_SID, ...  ⚠︎ 커밋 금지
├── requirements.txt
├── README.md
├── src/
│   ├── db.py          # SQLAlchemy 세션
│   ├── models.py      # Category, Inventory ORM
│   └── alerts.py      # SMS helper
├── main.py            # 입력 UI + SMS 알림
└── pages/
    └── statistics.py  # 월별 통계 대시보드
```

---

## ⚡ 설치 & 실행

```bash
# 1️⃣ 의존성 설치
pip install -r requirements.txt

# 2️⃣ .streamlit/secrets.toml 작성
cat <<EOF > .streamlit/secrets.toml
DB_URL       = "sqlite:///inventory.db"
TWILIO_SID   = "ACxxxxxxxxxxxxxxxxxxxx"
TWILIO_TOKEN = "your_twilio_token"
ADMIN_PHONE  = "+821012345678"
FROM_PHONE   = "+12345678901"
EOF

# 3️⃣ 테이블 생성 & 초기 품목 등록(예시)
python - <<'PY'
from src.db import get_session, engine
from src.models import Base, Category
Base.metadata.create_all(bind=engine)
items=[("빵","생지","위트",320),("빵","생지","화이트",320)]
with get_session() as s:
    for m,mi,sb,t in items:
        s.merge(Category(main=m,mid=mi,sub=sb,target=t))
PY

# 4️⃣ Streamlit 멀티페이지 실행
streamlit run main.py
```

---

## 🔑 핵심 코드 스니펫

### `src/alerts.py`

```python
from twilio.rest import Client
import streamlit as st

def send_sms(body: str):
    sid   = st.secrets["TWILIO_SID"]
    token = st.secrets["TWILIO_TOKEN"]
    to    = st.secrets["ADMIN_PHONE"]
    from_ = st.secrets["FROM_PHONE"]
    Client(sid, token).messages.create(body=body, from_=from_, to=to)
```

### `main.py` 저장 & 알림

```python
from src.alerts import send_sms
...
if st.button("💾 저장"):
    low, high = [], []
    with get_session() as sess:
        for r in rows:
            sess.add(Inventory(**r))
            if r["stock"] < r["target"]:
                low.append(f"{r['sub']} 부족 {r['stock']}/{r['target']}")
            elif r["stock"] > r["target"] * 1.5:
                high.append(f"{r['sub']} 과잉 {r['stock']}")
    if low or high:
        send_sms("[Subway 재고 알림]\n"+"\n".join(low+high))
```

---

## 📜 License  | MIT

<div align="center">Made with 💚 by Subway‑Ops Team</div>
