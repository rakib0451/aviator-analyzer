import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aviator Live Analyzer", layout="wide")

st.title("✈️ Aviator Live Data Analyzer")
st.write("২৪ ঘণ্টা রাউন্ড history সংগ্রহ করে লাইভ এনালাইসিস ও গ্রাফ দেখাবে।")

# --- ডেটা আনার ফাংশন ---
def fetch_data():
    url = "https://aviatortrends.com/history.json"  # ডেমো URL, পরে সঠিক সোর্স দিন
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()  # ধরে নিচ্ছি list of multipliers
    except Exception as e:
        st.error(f"ডেটা আনতে সমস্যা: {e}")
    return []

# --- ডেটা প্রসেস ---
data = fetch_data()
if data:
    df = pd.DataFrame({
        "time": [datetime.now() for _ in data],
        "multiplier": [float(x) for x in data]
    })

    # স্ট্যাটস দেখানো
    st.subheader("📊 বিশ্লেষণ ফলাফল")
    st.write(f"✅ মোট রাউন্ড: {len(df)}")
    st.write(f"✅ গড় multiplier: {df['multiplier'].mean():.2f}x")
    st.write(f"✅ সর্বোচ্চ multiplier: {df['multiplier'].max()}x")
    st.write(f"✅ 10x এর বেশি এসেছে: {(df['multiplier']>=10).sum()} বার")

    # --- লাইন চার্ট ---
    st.subheader("📈 Multiplier Trend (সময় অনুযায়ী)")
    st.line_chart(df.set_index("time")["multiplier"])

    # --- হিস্টোগ্রাম ---
    st.subheader("📊 Multiplier Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["multiplier"], bins=20, color="skyblue", edgecolor="black")
    ax.set_xlabel("Multiplier (x)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

else:
    st.warning("⚠️ ডেটা পাওয়া যায়নি, আবার চেষ্টা করুন।")
