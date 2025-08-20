import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os

# File to store reports
REPORT_FILE = "reports.csv"

# Initialize CSV if not exists
if not os.path.exists(REPORT_FILE):
    df_init = pd.DataFrame(columns=["name", "description", "latitude", "longitude", "timestamp"])
    df_init.to_csv(REPORT_FILE, index=False)

# Load reports
df = pd.read_csv(REPORT_FILE)

# ---- FORM ----
st.title("🧹 Anti-Sludge Mapping")

with st.form("report_form"):
    st.subheader("Report a Sludge Issue")
    name = st.text_input("Your Name")
    description = st.text_area("Description of the issue")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", format="%.6f")
    with col2:
        lon = st.number_input("Longitude", format="%.6f")

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        if name and description:
            new_entry = {
                "name": name,
                "description": description,
                "latitude": lat,
                "longitude": lon,
                "timestamp": datetime.now()
            }
            df = pd.concat([df, pd.DataFrame([new_entry])])
            df.to_csv(REPORT_FILE, index=False)
            st.success("✅ Report submitted!")
        else:
            st.error("❗ Name and description are required.")

# ---- MAP ----
st.subheader("📍 Map of Reported Issues")

# Create Folium map
if not df.empty:
    avg_lat = df["latitude"].mean()
    avg_lon = df["longitude"].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
    for _, row in df.iterrows():
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=f"{row['name']}: {row['description']}",
            tooltip=row["timestamp"]
        ).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("No reports yet.")
