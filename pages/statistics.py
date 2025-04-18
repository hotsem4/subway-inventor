import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import get_session
from src.models import Inventory

st.set_page_config(page_title="📊 재고 통계", layout="wide")

st.title("📊 월별 재고 분석")
sel_month = st.selectbox("월 선택", ["2024-04", "2024-05"], index=0)
month_start = pd.to_datetime(f"{sel_month}-01")
month_end = month_start + pd.offsets.MonthEnd(0)

with get_session() as sess:
    df = pd.read_sql(
        sess.query(Inventory)
            .filter(Inventory.date.between(month_start, month_end))
            .statement, sess.bind)

if df.empty:
    st.info("해당 월 데이터가 없습니다. main 페이지에서 입력해 주세요.")
    st.stop()

item = st.selectbox("소분류 선택", sorted(df["sub"].unique()))
view = df[df["sub"] == item].sort_values("date")

fig = px.line(view, x="date", y="stock", markers=True,
              title=f"{item} | {sel_month} 재고 추이 (기준 {view['target'].iloc[0]})")
fig.update_layout(xaxis_title="날짜", yaxis_title="재고 수량")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(view, use_container_width=True)
