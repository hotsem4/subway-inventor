import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.db import get_session, engine
from src.models import Base, Category, Inventory

# 테이블 자동 생성 (첫 실행)
Base.metadata.create_all(bind=engine)

# ────── UI 헤더 ──────
st.set_page_config(page_title="🥪 Subway 재고 관리", layout="wide")
with st.container():
    col1, col2 = st.columns([8, 2])
    col1.markdown("### 🥪 써브웨이 재고 관리 시스템")
    col2.markdown(
        f"""<div style='text-align:right;margin-top:24px;'>👋 User: {USERNAME}님</div>""", unsafe_allow_html=True)

# ────── 사이드바: 분류 로드 ──────
with get_session() as sess:
    cats = pd.read_sql(sess.query(Category).statement, sess.bind)

if cats.empty:
    st.error("카테고리 테이블이 비어 있습니다. 관리자 페이지에서 품목을 먼저 등록하세요.")
    st.stop()

sel_date = st.sidebar.date_input("조사 날짜", value=date.today())
main_list = sorted(cats.main.unique())
sel_main = st.sidebar.selectbox("대분류", main_list)

mid_list = sorted(cats[cats.main == sel_main].mid.unique())
sel_mid = st.sidebar.selectbox("중분류", ["전체"]+mid_list)

if sel_mid != "전체":
    sub_df = cats[(cats.main == sel_main) & (cats.mid == sel_mid)]
else:
    sub_df = cats[cats.main == sel_main]
sub_list = sorted(sub_df.sub.unique())
sel_sub = st.sidebar.selectbox("소분류", ["전체"]+sub_list)

# ────── 품목 필터 ──────
flt = cats[cats.main == sel_main]
if sel_mid != "전체":
    flt = flt[flt.mid == sel_mid]
if sel_sub != "전체":
    flt = flt[flt.sub == sel_sub]

st.subheader(f"📦 [{sel_main}] 재고 수량 입력")
results = []
for _, r in flt.iterrows():
    qty = st.number_input(f"{r.mid} > {r.sub} (기준 {r.target})",
                          min_value=0, step=1, key=f"qty_{r.id}")
    results.append(dict(date=sel_date, main=r.main, mid=r.mid,
                   sub=r.sub, stock=qty, target=r.target))

if st.button("💾 저장"):
    with get_session() as sess:
        for row in results:
            sess.add(Inventory(**row))
    st.success("DB 저장 완료!")

# ────── 미리보기 테이블 ──────
preview = pd.DataFrame(results)
st.dataframe(preview, use_container_width=True)
