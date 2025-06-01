
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🌿 Mwanza Irrigation Data Tool", layout="wide")
st.title("🌿 Mwanza Irrigation Data Collection Tool")

DATA_FILE = "data.csv"

# Load existing data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "EPA", "Section", "Visit Date", "Scheme", "GPS E", "GPS N",
        "Project", "Financial Year", "Quarter", "Month",
        "Male", "Female", "Total",
        "Potential Area", "Developed Area", "Utilized Area", "Newly Developed",
        "Water Sources", "Irrigation Systems",
        "1 Crop", "2 Crops",
        "Challenges", "Solutions"
    ])

# Show form
st.subheader("📋 Submit Irrigation Data")
with st.form("data_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        epa = st.text_input("EPA Name")
        section = st.text_input("Section")
        visit_date = st.date_input("Date of Visit")
        scheme = st.text_input("Scheme Name")
        gps_e = st.text_input("GPS Easting")
        gps_n = st.text_input("GPS Northing")
        project = st.text_input("Project Name")
        fy = st.text_input("Financial Year")
        quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
        month = st.text_input("Month")
        male = st.number_input("Male Beneficiaries", min_value=0, step=1)
        female = st.number_input("Female Beneficiaries", min_value=0, step=1)
    with col2:
        potential = st.number_input("Potential Area (Ha)", step=0.1)
        developed = st.number_input("Developed Area (Ha)", step=0.1)
        utilized = st.number_input("Utilized Area (Ha)", step=0.1)
        new_dev = st.number_input("Newly Developed Area (Ha)", step=0.1)
        water_sources = st.multiselect("Water Sources", ["Dam", "Stream", "Shallow Well", "Deep Well", "Borehole"])
        technology = st.multiselect("Irrigation Systems", ["Watering cans", "Pumps", "Solar Pumps", "River diversion"])
        crop1 = st.number_input("Area under 1 Cropping Cycle (Ha)", step=0.1)
        crop2 = st.number_input("Area under 2 Cropping Cycles (Ha)", step=0.1)
        challenges = st.text_area("Challenges")
        solutions = st.text_area("Proposed Solutions")

    submitted = st.form_submit_button("Submit")

    if submitted:
        new_row = {
            "EPA": epa, "Section": section, "Visit Date": visit_date, "Scheme": scheme,
            "GPS E": gps_e, "GPS N": gps_n, "Project": project, "Financial Year": fy,
            "Quarter": quarter, "Month": month,
            "Male": male, "Female": female, "Total": male + female,
            "Potential Area": potential, "Developed Area": developed, "Actual Area": actual,
            "Newly Developed": new_dev,
            "Water Sources": ", ".join(water_sources),
            "Irrigation Systems": ", ".join(systems),
            "1 Crop": crop1, "2 Crops": crop2, "3 Crops": crop3, "4 Crops": crop4,
            "Challenges": challenges, "Solutions": solutions
        }
        df = df._append(new_row, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Data submitted and saved!")

# Editable table
st.subheader("📊 Saved Records")
if not df.empty:
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.write("📝 Edit any cell, and click below to save changes.")
    if st.button("💾 Save Changes"):
        edited_df.to_csv(DATA_FILE, index=False)
        st.success("Changes saved!")

    delete_row = st.number_input("Enter row number to delete (starting at 0)", min_value=0, max_value=len(df)-1, step=1)
    if st.button("🗑️ Delete Selected Row"):
        df = df.drop(delete_row).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Row {delete_row} deleted.")
else:
    st.info("No data yet.")
