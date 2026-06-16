import streamlit as st
import pandas as pd

from PIL import Image

pfmea = pd.read_csv("pfmea_database.csv")
torque = pd.read_csv("torque_data.csv")

banner = Image.open("images/factory_background.png")
# Page Setup
st.set_page_config(
    page_title="Rear Axle Industry 4.0 Platform",
    layout="wide"
)

# Title
st.title("🚛 Rear Axle Industry 4.0 Platform")

st.image(
    banner,
    use_container_width=True
)

# Sidebar
st.sidebar.title("RA07 Dashboard")

module = st.sidebar.radio(
    "Select Module",
    [
        "Rear Axle PFMEA",
        "Torquing Data Visualisation"
    ]
)

# ==================================================
# ==================================================
# TORQUING MODULE
# ==================================================

if module == "Torquing Data Visualisation":

    st.header("🔧 Rear Axle Torquing Data Visualisation")

    # Select Axle
    selected_axle = st.selectbox(
        "Select Axle",
        sorted(torque["Axle"].unique())
    )

    axle_data = torque[
        torque["Axle"] == selected_axle
    ]

    # Select Component
    component = st.selectbox(
        "Select Sub Assembly",
        sorted(axle_data["Component"].unique())
    )

    component_data = axle_data[
        axle_data["Component"] == component
    ]

    # KPI Counts
    ok_count = len(
        component_data[
            component_data["Status"] == "OK"
        ]
    )

    under_count = len(
        component_data[
            component_data["Status"] == "UNDER TORQUE"
        ]
    )

    over_count = len(
        component_data[
            component_data["Status"] == "OVER TORQUE"
        ]
    )

    total_count = len(component_data)
    compliance = round(
        (ok_count / total_count) * 100,
        2
    )

    # KPI Cards

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Bolts",
        total_count
    )

    col2.metric(
        "OK",
        ok_count
    )

    col3.metric(
        "Under Torque",
        under_count
    )

    col4.metric(
        "Over Torque",
        over_count
    )

    col5.metric(
        "Compliance %",
        f"{compliance}%"
    )


    st.divider()

    st.subheader(
        f"{component} Torque Traceability"
    )

    # Colour Status

    def color_status(val):

        if val == "OK":
            return "background-color:#90EE90"

        elif val == "UNDER TORQUE":
            return "background-color:#FFFF99"

        elif val == "OVER TORQUE":
            return "background-color:#FF9999"

        return ""

    styled_df = component_data.style.map(
        color_status,
        subset=["Status"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True
    )
    st.divider()

    st.subheader("Bolt Status Grid")

    cols = st.columns(4)

    for idx, row in enumerate(component_data.itertuples()):

        if row.Status == "OK":
            icon = "🟢"

        elif row.Status == "UNDER TORQUE":
            icon = "🟡"

        else:
            icon = "🔴"

        cols[idx % 4].write(
            f"{icon} {row[4]}"
        )
    st.divider()

    st.subheader(
        f"{component} Status Distribution"
    )

    status_summary = component_data[
        "Status"
    ].value_counts()

    st.bar_chart(
        status_summary
    )

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Bolts", total_count)
    col2.metric("OK", ok_count)
    col3.metric("Under Torque", under_count)
    col4.metric("Over Torque", over_count)

    st.divider()

    st.subheader(f"{component} Bolt Details")

    st.dataframe(
        component_data,
        use_container_width=True
    )

# ==================================================
# PFMEA MODULE
# ==================================================

else:

    st.header("📋 Rear Axle PFMEA")

    process = st.selectbox(
        "Select Process",
        sorted(pfmea["Process"].unique())
    )

    filtered = pfmea[
        pfmea["Process"] == process
        ]

    failure_mode = st.selectbox(
        "Select Failure Mode",
        filtered["Failure Mode"]
    )

    record = filtered[
        filtered["Failure Mode"] == failure_mode
        ].iloc[0]

    st.subheader("Function")
    st.write(record["Function"])

    st.subheader("Effect")
    st.write(record["Effect"])

    st.subheader("Cause")
    st.write(record["Cause"])

    st.subheader("Prevention Control")
    st.write(record["Prevention Control"])

    st.subheader("Detection Control")
    st.write(record["Detection Control"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Severity",
        record["Severity"]
    )

    col2.metric(
        "Occurrence",
        record["Occurrence"]
    )

    col3.metric(
        "Detection",
        record["Detection"]
    )

    col4.metric(
        "RPN",
        record["RPN"]
    )