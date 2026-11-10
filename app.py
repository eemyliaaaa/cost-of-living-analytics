import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cost of Living Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# COLOUR THEME
# ==========================================

MAROON = "#702F3B"
OLIVE = "#78834B"
CREAM = "#F4F0E8"
CHARCOAL = "#30302E"
MUTED = "#B8AA9A"

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F4F0E8;
    color: #30302E;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #49252E;
}

[data-testid="stMetric"] {
    background-color: white;
    border-left: 5px solid #78834B;
    padding: 16px;
    border-radius: 10px;
}

[data-testid="stMetricValue"] {
    color: #702F3B;
}

.stButton button {
    background-color: #702F3B;
    color: white;
    border-radius: 8px;
}

div[data-testid="stRadio"] > label {
    color: #49252E;
    font-weight: bold;
}

hr {
    border-color: #B8AA9A;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    data = pd.read_csv("merged_dataset.csv")

    data.columns = data.columns.str.strip()
    data["state"] = data["state"].astype(str).str.strip()
    data["division"] = data["division"].astype(str).str.strip()

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "merged_dataset.csv not found. "
        "Please place the CSV file in the same folder as app.py."
    )
    st.stop()


# ==========================================
# DATA PREPARATION
# ==========================================

overall_df = df[
    df["division"].str.lower() == "overall"
].copy()

category_df = df[
    df["division"].str.lower() != "overall"
].copy()

years = sorted(df["year"].unique())
states = sorted(df["state"].unique())

latest_year = max(years)


# ==========================================
# TOP NAVIGATION
# ==========================================

st.markdown("""
<h1 style="color:#702F3B; margin-bottom:0;">
    Cost of Living Analytics
</h1>
<p style="color:#78834B; font-size:16px;">
    MALAYSIA | STATE-LEVEL DATA ANALYSIS
</p>
""", unsafe_allow_html=True)

page = st.radio(
    "Navigation",
    [
        "Overview",
        "Income vs Price Growth",
        "State Comparison",
        "CPI Heatmap"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")


# ==========================================
# REUSABLE KPI FUNCTION
# ==========================================

def show_kpis(items):

    columns = st.columns(len(items))

    for col, (label, value, description) in zip(columns, items):

        with col:
            st.metric(label, value)
            st.caption(description)


# ==========================================
# PAGE 1: OVERVIEW
# ==========================================

if page == "Overview":

    st.title("Malaysia Cost of Living Overview")

    st.write(
        "This dashboard explores household income, population "
        "and consumer price index (CPI) across Malaysian states "
        "to understand changes in affordability and cost of living."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Malaysian States", df["state"].nunique())
    col2.metric("Observation Years", df["year"].nunique())
    col3.metric("Spending Categories", category_df["division"].nunique())

    st.markdown("---")

    st.subheader("Dataset Information")

    st.write("""
    **Dataset:** Merged Malaysian Population, Household Income
    and Consumer Price Index Dataset.

    **Variables:**
    - State
    - Year
    - Population
    - Mean household income
    - Median household income
    - Spending division
    - Consumer price index
    """)

    st.subheader("Visualization Objectives")

    st.markdown("""
    **Objective 1: Income Growth vs Price Growth**

    To compare household income growth and consumer price index
    growth across Malaysian states from 2012 to 2024.

    **Objective 2: Population, Income and Cost of Living**

    To examine the relationship between population size,
    household income and consumer price index across states.

    **Objective 3: Consumer Price Index by Spending Category**

    To identify and compare consumer price index values across
    major spending categories among Malaysian states.
    """)

    st.info(
        "Use the top navigation bar to explore the three "
        "visualization pages."
    )


# ==========================================
# PAGE 2: LINE CHART
# ==========================================

elif page == "Income vs Price Growth":

    st.title("Income Growth vs Price Growth")

    st.write(
        "Compare household income growth and CPI growth "
        "across Malaysian states from 2012 to 2024."
    )

    selected_states = st.multiselect(
        "Select Malaysian States",
        states,
        default=states
    )

    if not selected_states:
        st.warning("Please select at least one state.")
        st.stop()

    filtered = overall_df[
        overall_df["state"].isin(selected_states)
    ].copy()

    filtered = filtered.sort_values(["state", "year"])

    # Base year calculation
    filtered["income_growth"] = (
        filtered["income_mean"] /
        filtered.groupby("state")["income_mean"].transform("first")
        - 1
    ) * 100

    filtered["price_growth"] = (
        filtered["index"] /
        filtered.groupby("state")["index"].transform("first")
        - 1
    ) * 100

    filtered["affordability_gap"] = (
        filtered["income_growth"] -
        filtered["price_growth"]
    )

    # Average across selected states
    line_data = filtered.groupby("year")[
        ["income_growth", "price_growth"]
    ].mean().reset_index()

    final = filtered[filtered["year"] == latest_year]

    avg_income = line_data.iloc[-1]["income_growth"]
    avg_cpi = line_data.iloc[-1]["price_growth"]
    avg_gap = avg_income - avg_cpi

    show_kpis([
        (
            "Average Income Growth",
            f"{avg_income:.2f}%",
            "Since 2012"
        ),
        (
            "Average CPI Growth",
            f"{avg_cpi:.2f}%",
            "Since 2012"
        ),
        (
            "Affordability Gap",
            f"{avg_gap:.2f} pp",
            "Income growth minus CPI growth"
        )
    ])

    st.markdown("---")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=line_data["year"],
        y=line_data["income_growth"],
        mode="lines+markers",
        name="Income Growth",
        line=dict(color=MAROON, width=3),
        marker=dict(size=9)
    ))

    fig.add_trace(go.Scatter(
        x=line_data["year"],
        y=line_data["price_growth"],
        mode="lines+markers",
        name="CPI Growth",
        line=dict(color=OLIVE, width=3),
        marker=dict(size=9)
    ))

    fig.update_layout(
        title="Average Income Growth vs CPI Growth Across Malaysian States",
        xaxis_title="Year",
        yaxis_title="Growth Since 2012 (%)",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Indicator",
        height=520
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Note: Growth is calculated using 2012 as the base year. "
        "Values represent the average percentage growth across "
        "the selected states."
    )

    st.subheader("Interpretation")

    if avg_gap > 0:
        st.success(
            f"Income growth exceeded CPI growth by "
            f"{avg_gap:.2f} percentage points on average. "
            "This suggests improved relative affordability "
            "compared with the 2012 base year."
        )
    else:
        st.warning(
            "CPI growth exceeded income growth on average, "
            "suggesting greater affordability pressure."
        )

    st.write(
        "The line chart compares changes in household income "
        "and consumer prices over time. A larger gap between "
        "the two lines indicates that income has grown faster "
        "than consumer prices."
    )


# ==========================================
# PAGE 3: DUMBBELL CHART
# ==========================================

elif page == "State Comparison":

    st.title("Population, Income and CPI Across States")

    st.write(
        "Compare mean household income and overall CPI "
        "across Malaysian states, with population represented "
        "by bubble size."
    )

    selected_year = st.selectbox(
        "Select Year",
        years,
        index=years.index(latest_year)
    )

    dumbbell_data = overall_df[
        overall_df["year"] == selected_year
    ].copy()

    # Standardize income and CPI separately
    def scale_100(series):

        min_value = series.min()
        max_value = series.max()

        if max_value == min_value:
            return pd.Series(50, index=series.index)

        return (
            (series - min_value) /
            (max_value - min_value)
        ) * 100

    dumbbell_data["income_scaled"] = scale_100(
        dumbbell_data["income_mean"]
    )

    dumbbell_data["cpi_scaled"] = scale_100(
        dumbbell_data["index"]
    )

    dumbbell_data = dumbbell_data.sort_values(
        "income_scaled"
    )

    highest_population = dumbbell_data.loc[
        dumbbell_data["population"].idxmax()
    ]

    highest_income = dumbbell_data.loc[
        dumbbell_data["income_mean"].idxmax()
    ]

    highest_cpi = dumbbell_data.loc[
        dumbbell_data["index"].idxmax()
    ]

    show_kpis([
        (
            "Highest Population",
            highest_population["state"],
            f'{highest_population["population"]:,.1f} thousand'
        ),
        (
            "Highest Mean Income",
            highest_income["state"],
            f'RM {highest_income["income_mean"]:,.0f}'
        ),
        (
            "Highest Overall CPI",
            highest_cpi["state"],
            f'{highest_cpi["index"]:.1f}'
        )
    ])

    st.markdown("---")

    fig = go.Figure()

    for _, row in dumbbell_data.iterrows():

        state = row["state"]

        fig.add_trace(go.Scatter(
            x=[row["income_scaled"], row["cpi_scaled"]],
            y=[state, state],
            mode="lines",
            line=dict(color=MUTED, width=3),
            showlegend=False,
            hoverinfo="skip"
        ))

    fig.add_trace(go.Scatter(
        x=dumbbell_data["income_scaled"],
        y=dumbbell_data["state"],
        mode="markers",
        name="Mean Income",
        marker=dict(
            color=MAROON,
            size=dumbbell_data["population"] /
                 dumbbell_data["population"].max() * 25 + 8,
            sizemode="diameter"
        ),
        customdata=np.column_stack([
            dumbbell_data["income_mean"],
            dumbbell_data["population"]
        ]),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Standardized income: %{x:.1f}<br>"
            "Mean income: RM %{customdata[0]:,.0f}<br>"
            "Population: %{customdata[1]:,.1f} thousand"
            "<extra></extra>"
        )
    ))

    fig.add_trace(go.Scatter(
        x=dumbbell_data["cpi_scaled"],
        y=dumbbell_data["state"],
        mode="markers",
        name="Overall CPI",
        marker=dict(
            color=OLIVE,
            size=dumbbell_data["population"] /
                 dumbbell_data["population"].max() * 25 + 8
        ),
        customdata=np.column_stack([
            dumbbell_data["index"],
            dumbbell_data["population"]
        ]),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Standardized CPI: %{x:.1f}<br>"
            "Actual CPI: %{customdata[0]:.1f}<br>"
            "Population: %{customdata[1]:,.1f} thousand"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title=f"Population, Income and CPI Across Malaysian States ({selected_year})",
        xaxis_title="Standardized Value (0–100)",
        yaxis_title="Malaysian States",
        template="plotly_white",
        height=650,
        legend_title="Indicator"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Note: Income and CPI are independently standardized "
        "to 0–100. Bubble size represents population. "
        "Population is measured in thousands."
    )

    st.subheader("Interpretation")

    st.write(
        f"In {selected_year}, {highest_population['state']} "
        f"recorded the highest population, while "
        f"{highest_income['state']} had the highest mean "
        f"household income. {highest_cpi['state']} recorded "
        f"the highest overall CPI."
    )

    st.write(
        "The dumbbell chart highlights the relative positions "
        "of income and CPI across states. Bubble sizes help "
        "compare population levels."
    )


# ==========================================
# PAGE 4: HEATMAP
# ==========================================

elif page == "CPI Heatmap":

    st.title("Consumer Price Index by Spending Category")

    st.write(
        "Explore differences in consumer price index "
        "across Malaysian states and spending categories."
    )

    selected_year = st.selectbox(
        "Select Year",
        years,
        index=years.index(latest_year),
        key="heatmap_year"
    )

    heatmap_data = category_df[
        category_df["year"] == selected_year
    ].copy()

    categories = sorted(
        heatmap_data["division"].unique()
    )

    selected_categories = st.multiselect(
        "Select Spending Categories",
        categories,
        default=categories
    )

    if not selected_categories:
        st.warning("Please select at least one category.")
        st.stop()

    heatmap_data = heatmap_data[
        heatmap_data["division"].isin(selected_categories)
    ]

    heatmap_pivot = heatmap_data.pivot(
        index="state",
        columns="division",
        values="index"
    )

    category_avg = heatmap_data.groupby(
        "division"
    )["index"].mean()

    highest_category = category_avg.idxmax()
    highest_category_value = category_avg.max()

    state_avg = heatmap_data.groupby(
        "state"
    )["index"].mean()

    highest_state = state_avg.idxmax()
    highest_state_value = state_avg.max()

    overall_avg = heatmap_data["index"].mean()

    show_kpis([
        (
            "Highest CPI Category",
            highest_category,
            f"{highest_category_value:.1f}"
        ),
        (
            "Highest Average CPI State",
            highest_state,
            f"{highest_state_value:.1f}"
        ),
        (
            "Average Category CPI",
            f"{overall_avg:.1f}",
            f"Year {selected_year}"
        )
    ])

    st.markdown("---")

    fig = px.imshow(
        heatmap_pivot,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale=[
            "#FFF4C2",
            "#F9A03F",
            "#D1493F",
            "#8F001A"
        ],
        labels=dict(
            x="Spending Categories",
            y="Malaysian States",
            color="CPI"
        ),
        title=f"Consumer Price Index by Spending Category ({selected_year})"
    )

    fig.update_layout(
        template="plotly_white",
        height=700,
        xaxis_tickangle=-40
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretation")

    st.write(
        f"For {selected_year}, {highest_category} recorded "
        f"the highest average CPI among the selected categories, "
        f"with an index of {highest_category_value:.1f}."
    )

    st.write(
        f"{highest_state} recorded the highest average "
        f"category CPI across the selected categories, "
        f"at {highest_state_value:.1f}."
    )

    st.caption(
        "Note: Overall CPI is excluded because this heatmap "
        "focuses on individual spending categories. "
        "CPI values are index values, not expenditure weights."
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#74675C; padding:10px;">
    <b>Cost of Living Analytics</b><br>
    Malaysia State-Level Visualization Project<br>
    Scientific Visualisation
</div>
""", unsafe_allow_html=True)
