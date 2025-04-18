from twilio.rest import Client
import streamlit as st


def send_sms(body: str):
    sid = st.secrets["TWILIO_SID"]
    token = st.secrets["TWILIO_TOKEN"]
    to = st.secrets["ADMIN_PHONE"]
    from_ = st.secrets["FROM_PHONE"]
    Client(sid, token).messages.create(body=body, from_=from_, to=to)
