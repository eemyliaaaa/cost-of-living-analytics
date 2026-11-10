
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Cost of Living Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. COLOUR THEME
# =====================================================

MAROON = "#702F3B"
DARK_MAROON = "#49252E"
OLIVE = "#78834B"
CREAM = "#F4F0E8"
CHARCOAL = "#30302E"
MUTED = "#B8AA9A"
WHITE = "#FFFFFF"

# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background-color: #F4F0E8;
    color: #30302E;
}

.block-container {
    padding-top: 0.6rem;
    padding-bottom: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1550px;
}

/* HEADINGS */

h1, h2, h3 {
    color: #49252E !important;
}

h1 {
    font-weight: 750 !important;
}

h2 {
    font-size: 24px !important;
}

h3 {
    font-size: 18px !important;
}

/* HEADER */

.brand-header {
    background: linear-gradient(110deg, #49252E, #702F3B);
    padding: 15px 24px;
    border-radius: 12px;
    margin-bottom: 5px;
    box-shadow: 0 3px 10px rgba(73,37,46,0.12);
}

.brand-header h1 {
    color: white !important;
    font-size: 29px !important;
    font-weight: 750 !important;
    margin: 0 !important;
}

.brand-header p {
    color: #E9DCE0 !important;
    font-size: 11px;
    margin: 5px 0 0 2px;
    letter-spacing: 1.4px;
}

/* HEADER TAG */

.header-tag {
    background: #78834B;
    color: white;
    border-radius: 10px;
    padding: 15px 7px;
    text-align: center;
    margin-top: 3px;
    font-size: 12px;
    font-weight: 700;
}

/* NAVIGATION */

.nav-caption {
    color: #78834B;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 1.4px;
    margin: 8px 0 4px 3px;
}

div[data-testid="stRadio"] {
    margin-bottom: 0;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: white;
    padding: 8px;
    border-radius: 11px;
    border: 1px solid #E5DED3;
    width: 100%;
}

div[data-testid="stRadio"] label {
    background: #F4F0E8;
    border: 1px solid #E5DED3;
    border-radius: 9px;
    padding: 8px 13px;
    transition: all 0.2s ease;
}

div[data-testid="stRadio"] label:hover {
    background: #E6E8D9;
    border-color: #78834B;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: #78834B;
    border-color: #78834B;
    color: white !important;
    font-weight: 700;
}

div[data-testid="stRadio"] label:has(input:checked) p {
    color: white !important;
}

div[data-testid="stRadio"] label p {
    font-size: 13px;
}

/* KPI CARDS */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E9E2D9;
    border-left: 5px solid #78834B;
    padding: 14px 17px;
    border-radius: 10px;
    min-height: 105px;
    box-shadow: 0 2px 7px rgba(0,0,0,0.035);
}

[data-testid="stMetricLabel"] {
    color: #66575A !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #702F3B !important;
    font-size: 24px !important;
    font-weight: 750 !important;
}

/* FILTERS */

div[data-baseweb="select"] > div {
    border-radius: 8px;
    border-color: #D9D0C5;
}

/* BUTTONS */

.stButton button {
    background-color: #702F3B;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton button:hover {
    background-color: #78834B;
    color: white;
}

/* INTERPRETATION CARDS */

.interpretation-card {
    background: white;
    border-left: 5px solid #78834B;
    border-radius: 9px;
    padding: 14px 17px;
    margin: 8px 0 13px 0;
    box-shadow: 0 2px 7px rgba(0,0,0,0.035);
}

.interpretation-card h4 {
    color: #702F3B;
    margin: 0 0 7px 0;
    font-size: 15px;
}

.interpretation-card p {
    color: #403A38;
    font-size: 13px;
    line-height: 1.65;
    margin: 0;
}

/* SECTION LABEL */

.section-label {
    color: #78834B;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 1.4px;
    margin-bottom: 3px;
}

/* OBJECTIVE CARDS */

.objective-card {
    background: white;
    border-top: 4px solid #78834B;
    border-radius: 10px;
    padding: 17px;
    min-height: 180px;
    box-shadow: 0 2px 7px rgba(0,0,0,0.035);
}

.objective-card h4 {
    color: #702F3B;
    margin-top: 0;
    font-size: 16px;
}

.objective-card p {
    font-size: 13px;
    color: #514A46;
    line-height: 1.6;
}

.objective-card small {
    color: #78834B;
    font-weight: 700;
    font-size: 10px;
    letter-spacing: 0.7px;
}

/* DIVIDER */

hr {
    border-color: #D9D0C5 !important;
    margin-top: 0.7rem;
    margin-bottom: 0.7rem;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #74675C;
    padding: 17px 5px;
    font-size: 12px;
    border-top: 1px solid #D9D0C5;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. LOAD DATASET
# =====================================================

@st.cache_data
def load_data():

    data = pd.read_csv("merged_dataset.csv")

    data.columns = data.columns.str.strip()

    data["state"] = data["state"].astype(str).str.strip()

    data["division"] = data["division"].astype(str).str.strip()

    numeric_columns = [
        "year",
        "population",
        "income_mean",
        "income_median",
        "index"
    ]

    for col in numeric_columns:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

    data = data.dropna(subset=numeric_columns)

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Dataset not found. Please upload "
        "merged_dataset.csv into the same GitHub repository."
    )
    st.stop()

except Exception as e:

    st.error(f"Unable to load dataset: {e}")
    st.stop()


# =====================================================
# 5. DATA PREPARATION
# =====================================================

overall_df = df[
    df["division"].str.lower() == "overall"
].copy()

category_df = df[
    df["division"].str.lower() != "overall"
].copy()

years = sorted(df["year"].unique().tolist())

states = sorted(df["state"].unique().tolist())

categories = sorted(
    category_df["division"].unique().tolist()
)

latest_year = max(years)

if overall_df.empty:
    st.error("Overall CPI data is missing.")
    st.stop()


# =====================================================
# 6. REUSABLE FUNCTIONS
# =====================================================

def show_kpis(items):

    columns = st.columns(len(items))

    for col, (label, value, description) in zip(columns, items):

        with col:

            st.metric(
                label=label,
                value=value
            )

            st.caption(description)


def show_interpretation(title, message):

    st.markdown(
        f"""
        <div class="interpretation-card">
            <h4>💡 {title}</h4>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def scale_100(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:

        return pd.Series(
            50,
            index=series.index
        )

    return (
        (series - minimum) /
        (maximum - minimum)
    ) * 100


def format_correlation(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:.3f}"


def chart_layout(fig, height=520):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=CHARCOAL,
            size=12
        ),
        margin=dict(
            l=35,
            r=35,
            t=75,
            b=65
        ),
        hoverlabel=dict(
            bgcolor=WHITE,
            font_color=CHARCOAL
        )
    )

    return fig


# =====================================================
# 7. BRAND HEADER
# =====================================================

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.markdown("""
    <div class="brand-header">
        <h1>Cost of Living Analytics</h1>
        <p>MALAYSIA · STATE-LEVEL DATA ANALYSIS</p>
    </div>
    """, unsafe_allow_html=True)

with header_col2:

    st.markdown("""
    <div class="header-tag">
        <div style="font-size:22px;">📊</div>
        <div>2024 DATA</div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 8. TOP NAVIGATION
# =====================================================

st.markdown(
    '<div class="nav-caption">EXPLORE DASHBOARD</div>',
    unsafe_allow_html=True
)

page = st.radio(
    "Navigation",
    [
        "Overview",
        "Income & Price",
        "State Comparison",
        "CPI Heatmap"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")


# =====================================================
# PAGE 1: OVERVIEW
# =====================================================

if page == "Overview":

    st.markdown(
        '<div class="section-label">DASHBOARD OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.title("Malaysia Cost of Living Overview")

    st.write(
        "Explore population, household income and consumer "
        "price index across Malaysian states to understand "
        "changes in affordability and cost of living."
    )

    # KPI SUMMARY

    show_kpis([
        (
            "Malaysian States",
            df["state"].nunique(),
            "States and federal territories"
        ),
        (
            "Observation Years",
            f"{min(years)}–{max(years)}",
            f"{len(years)} available years"
        ),
        (
            "Spending Categories",
            category_df["division"].nunique(),
            "Individual CPI categories"
        ),
        (
            "Dataset Records",
            f"{len(df):,}",
            "Total observations"
        )
    ])

    st.markdown("---")

    # TWO-COLUMN OVERVIEW

    left, right = st.columns([1.15, 1], gap="large")

    with left:

        st.subheader("About This Dashboard")

        st.write(
            "This dashboard analyses Malaysian state-level "
            "population, household income and Consumer Price "
            "Index (CPI) data."
        )

        st.markdown("#### Main Areas of Analysis")

        st.markdown("""
        - Income growth compared with price growth.
        - Population, income and CPI relationships.
        - CPI differences across spending categories.
        """)

        st.markdown("#### Dataset Information")

        st.markdown(f"""
        - **Coverage:** {len(states)} states and territories
        - **Period:** {min(years)}–{max(years)}
        - **Latest observation:** {latest_year}
        - **Individual CPI categories:** {len(categories)}
        - **Total observations:** {len(df):,}
        """)

    with right:

        st.subheader("Analysis Highlights")

        latest_overall = overall_df[
            overall_df["year"] == latest_year
        ]

        highest_income = latest_overall.loc[
            latest_overall["income_mean"].idxmax()
        ]

        highest_population = latest_overall.loc[
            latest_overall["population"].idxmax()
        ]

        highest_cpi = latest_overall.loc[
            latest_overall["index"].idxmax()
        ]

        st.markdown(f"""
        <div class="interpretation-card">
            <h4>💰 Highest Mean Household Income</h4>
            <p><b>{highest_income['state']}</b><br>
            RM {highest_income['income_mean']:,.0f}</p>
        </div>

        <div class="interpretation-card">
            <h4>👥 Highest Population</h4>
            <p><b>{highest_population['state']}</b><br>
            {highest_population['population']:,.1f} thousand</p>
        </div>

        <div class="interpretation-card">
            <h4>📈 Highest Overall CPI</h4>
            <p><b>{highest_cpi['state']}</b><br>
            CPI Index: {highest_cpi['index']:.1f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # OBJECTIVES

    st.subheader("Explore the Analysis")

    st.write(
        "Three visualizations are designed to address "
        "the main objectives of this study."
    )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:

        st.markdown("""
        <div class="objective-card">
            <h4>📈 Objective 1</h4>
            <b>Income vs Price Growth</b>
            <p>Compare income growth and CPI growth
            to examine changes in affordability.</p>
            <small>LINE CHART · TREND ANALYSIS</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="objective-card">
            <h4>📊 Objective 2</h4>
            <b>Population, Income & CPI</b>
            <p>Examine the relationship between population,
            household income and consumer prices.</p>
            <small>DUMBBELL CHART · STATE COMPARISON</small>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="objective-card">
            <h4>🔥 Objective 3</h4>
            <b>Spending Category Comparison</b>
            <p>Identify differences in CPI across food,
            housing, transport and other categories.</p>
            <small>HEATMAP · CATEGORY ANALYSIS</small>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# PAGE 2: INCOME VS PRICE GROWTH
# =====================================================

elif page == "Income & Price":

    st.markdown(
        '<div class="section-label">OBJECTIVE 1 · LINE CHART</div>',
        unsafe_allow_html=True
    )

    st.title("Income Growth vs Price Growth")

    st.write(
        "Compare household income growth and consumer "
        "price index growth across Malaysian states."
    )

    # STATE FILTER

    selected_states = st.multiselect(
        "Select Malaysian States",
        options=states,
        default=states,
        key="line_states"
    )

    if not selected_states:

        st.warning("Please select at least one state.")
        st.stop()

    filtered = overall_df[
        overall_df["state"].isin(selected_states)
    ].copy()

    filtered = filtered.sort_values(
        ["state", "year"]
    )

    # GROWTH CALCULATIONS

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

    line_data = filtered.groupby("year")[
        ["income_growth", "price_growth"]
    ].mean().reset_index()

    latest_data = line_data.iloc[-1]

    avg_income = latest_data["income_growth"]
    avg_cpi = latest_data["price_growth"]
    avg_gap = avg_income - avg_cpi

    # KPI CARDS

    show_kpis([
        (
            "Average Income Growth",
            f"{avg_income:.2f}%",
            "Since the base year"
        ),
        (
            "Average CPI Growth",
            f"{avg_cpi:.2f}%",
            "Since the base year"
        ),
        (
            "Affordability Gap",
            f"{avg_gap:.2f} pp",
            "Income growth minus CPI growth"
        )
    ])

    st.markdown("---")

    # LINE CHART

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=line_data["year"],
            y=line_data["income_growth"],
            mode="lines+markers",
            name="Income Growth",
            line=dict(color=MAROON, width=3),
            marker=dict(size=9),
            hovertemplate=(
                "Year: %{x}<br>"
                "Income Growth: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=line_data["year"],
            y=line_data["price_growth"],
            mode="lines+markers",
            name="CPI Growth",
            line=dict(color=OLIVE, width=3),
            marker=dict(size=9),
            hovertemplate=(
                "Year: %{x}<br>"
                "CPI Growth: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Average Income Growth vs CPI Growth Across Malaysian States",
        xaxis_title="Year",
        yaxis_title="Growth Since Base Year (%)",
        hovermode="x unified",
        legend_title="Indicator"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=line_data["year"]
    )

    fig = chart_layout(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Note: Growth is calculated using the earliest "
        "available observation for each selected state "
        "as its base year. Results represent the unweighted "
        "average across selected states."
    )

    # INTERPRETATION

    st.subheader("Interpretation")

    if avg_gap > 0:

        show_interpretation(
            "Income growth exceeds CPI growth",
            f"Average income growth was {avg_income:.2f}%, "
            f"compared with CPI growth of {avg_cpi:.2f}%. "
            f"The difference was {avg_gap:.2f} percentage "
            "points. This suggests income increased faster "
            "than consumer prices in the selected states."
        )

    elif avg_gap < 0:

        show_interpretation(
            "CPI growth exceeds income growth",
            f"CPI growth exceeded income growth by "
            f"{abs(avg_gap):.2f} percentage points. "
            "This suggests greater relative affordability pressure."
        )

    else:

        show_interpretation(
            "Income and CPI growth are equal",
            "Average household income growth and CPI growth "
            "are approximately equal."
        )

    st.write(
        "The line chart illustrates changes in household "
        "income and consumer prices over time. A larger "
        "difference between the two lines indicates that "
        "income growth has outpaced price growth."
    )


# =====================================================
# PAGE 3: STATE COMPARISON
# =====================================================

elif page == "State Comparison":

    st.markdown(
        '<div class="section-label">OBJECTIVE 2 · DUMBBELL CHART</div>',
        unsafe_allow_html=True
    )

    st.title("Population, Income and CPI Across States")

    st.write(
        "Compare household income and overall CPI across "
        "Malaysian states, with population represented "
        "by bubble size."
    )

    # YEAR FILTER

    selected_year = st.selectbox(
        "Select Observation Year",
        options=years,
        index=years.index(latest_year),
        key="dumbbell_year"
    )

    dumbbell_data = overall_df[
        overall_df["year"] == selected_year
    ].copy()

    if dumbbell_data.empty:

        st.warning("No data available for the selected year.")
        st.stop()

    # NORMALIZE VALUES

    dumbbell_data["income_scaled"] = scale_100(
        dumbbell_data["income_mean"]
    )

    dumbbell_data["cpi_scaled"] = scale_100(
        dumbbell_data["index"]
    )

    dumbbell_data = dumbbell_data.sort_values(
        "income_scaled"
    )

    # SUMMARY VALUES

    highest_population = dumbbell_data.loc[
        dumbbell_data["population"].idxmax()
    ]

    highest_income = dumbbell_data.loc[
        dumbbell_data["income_mean"].idxmax()
    ]

    highest_cpi = dumbbell_data.loc[
        dumbbell_data["index"].idxmax()
    ]

    # CORRELATION

    population_income_corr = dumbbell_data[
        ["population", "income_mean"]
    ].corr().iloc[0, 1]

    population_cpi_corr = dumbbell_data[
        ["population", "index"]
    ].corr().iloc[0, 1]

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

    corr1, corr2 = st.columns(2)

    with corr1:

        st.metric(
            "Population–Income Correlation",
            format_correlation(population_income_corr)
        )

    with corr2:

        st.metric(
            "Population–CPI Correlation",
            format_correlation(population_cpi_corr)
        )

    st.caption(
        "Correlation coefficients are calculated across "
        "the states for the selected year. Correlation "
        "does not establish causation."
    )

    st.markdown("---")

    # DUMBBELL CHART

    fig = go.Figure()

    # CONNECTING LINES

    for _, row in dumbbell_data.iterrows():

        fig.add_trace(
            go.Scatter(
                x=[
                    row["income_scaled"],
                    row["cpi_scaled"]
                ],
                y=[
                    row["state"],
                    row["state"]
                ],
                mode="lines",
                line=dict(
                    color=MUTED,
                    width=2.5
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # POPULATION BUBBLE SIZE

    max_population = dumbbell_data["population"].max()

    bubble_sizes = (
        dumbbell_data["population"] /
        max_population * 25 + 8
    )

    # INCOME

    fig.add_trace(
        go.Scatter(
            x=dumbbell_data["income_scaled"],
            y=dumbbell_data["state"],
            mode="markers",
            name="Mean Income",
            marker=dict(
                color=MAROON,
                size=bubble_sizes,
                line=dict(color=WHITE, width=1)
            ),
            customdata=np.column_stack([
                dumbbell_data["income_mean"],
                dumbbell_data["population"]
            ]),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Standardized Income: %{x:.1f}<br>"
                "Mean Income: RM %{customdata[0]:,.0f}<br>"
                "Population: %{customdata[1]:,.1f} thousand"
                "<extra></extra>"
            )
        )
    )

    # CPI

    fig.add_trace(
        go.Scatter(
            x=dumbbell_data["cpi_scaled"],
            y=dumbbell_data["state"],
            mode="markers",
            name="Overall CPI",
            marker=dict(
                color=OLIVE,
                size=bubble_sizes,
                line=dict(color=WHITE, width=1)
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
        )
    )

    fig.update_layout(
        title=(
            "Population, Income and CPI Across "
            f"Malaysian States ({selected_year})"
        ),
        xaxis_title="Standardized Value (0–100)",
        yaxis_title="Malaysian States",
        legend_title="Indicator",
        height=680,
        hovermode="closest"
    )

    fig.update_xaxes(
        range=[-5, 105],
        showgrid=True,
        gridcolor="#EAE5DE"
    )

    fig = chart_layout(fig, height=680)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Note: Income and CPI are independently standardized "
        "to 0–100. Bubble size represents population in thousands."
    )

    # INTERPRETATION

    st.subheader("Interpretation")

    if pd.isna(population_income_corr):

        income_message = (
            "The population–income correlation could not be calculated."
        )

    elif population_income_corr > 0:

        income_message = (
            "Population and mean household income showed "
            "a positive association."
        )

    elif population_income_corr < 0:

        income_message = (
            "Population and mean household income showed "
            "a negative association."
        )

    else:

        income_message = (
            "No linear association was observed between "
            "population and mean household income."
        )

    if pd.isna(population_cpi_corr):

        cpi_message = (
            "The population–CPI correlation could not be calculated."
        )

    elif population_cpi_corr > 0:

        cpi_message = (
            "Population and overall CPI showed a positive association."
        )

    elif population_cpi_corr < 0:

        cpi_message = (
            "Population and overall CPI showed a negative association."
        )

    else:

        cpi_message = (
            "No linear association was observed between "
            "population and overall CPI."
        )

    show_interpretation(
        f"State-level findings for {selected_year}",
        f"{highest_population['state']} recorded the highest "
        f"population. {highest_income['state']} had the highest "
        f"mean household income, while {highest_cpi['state']} "
        f"recorded the highest overall CPI. {income_message} "
        f"{cpi_message}"
    )

    st.write(
        "Correlation values help examine whether population "
        "is associated with household income and CPI. "
        "These relationships do not establish causation."
    )


# =====================================================
# PAGE 4: CPI HEATMAP
# =====================================================

elif page == "CPI Heatmap":

    st.markdown(
        '<div class="section-label">OBJECTIVE 3 · HEATMAP</div>',
        unsafe_allow_html=True
    )

    st.title("Consumer Price Index by Spending Category")

    st.write(
        "Compare consumer price index values across "
        "Malaysian states and individual spending categories."
    )

    # YEAR FILTER

    selected_year = st.selectbox(
        "Select Observation Year",
        options=years,
        index=years.index(latest_year),
        key="heatmap_year"
    )

    heatmap_data = category_df[
        category_df["year"] == selected_year
    ].copy()

    available_categories = sorted(
        heatmap_data["division"].unique()
    )

    # CATEGORY FILTER

    selected_categories = st.multiselect(
        "Select Spending Categories",
        options=available_categories,
        default=available_categories,
        key="heatmap_categories"
    )

    if not selected_categories:

        st.warning(
            "Please select at least one spending category."
        )
        st.stop()

    heatmap_data = heatmap_data[
        heatmap_data["division"].isin(selected_categories)
    ].copy()

    # PIVOT TABLE

    heatmap_pivot = heatmap_data.pivot(
        index="state",
        columns="division",
        values="index"
    )

    # SUMMARY VALUES

    category_avg = heatmap_data.groupby(
        "division"
    )["index"].mean()

    state_avg = heatmap_data.groupby(
        "state"
    )["index"].mean()

    highest_category = category_avg.idxmax()
    highest_category_value = category_avg.max()

    highest_state = state_avg.idxmax()
    highest_state_value = state_avg.max()

    overall_avg = heatmap_data["index"].mean()

    # KPI CARDS

    show_kpis([
        (
            "Highest CPI Category",
            highest_category,
            f"{highest_category_value:.1f} average index"
        ),
        (
            "Highest Average CPI State",
            highest_state,
            f"{highest_state_value:.1f} average index"
        ),
        (
            "Average Category CPI",
            f"{overall_avg:.1f}",
            f"Observation year {selected_year}"
        )
    ])

    st.markdown("---")

    # HEATMAP

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
            color="Consumer Price Index"
        ),
        title=(
            "Consumer Price Index by Spending "
            f"Category Across Malaysian States ({selected_year})"
        )
    )

    fig.update_layout(
        height=720,
        coloraxis_colorbar=dict(
            title="CPI Index"
        ),
        margin=dict(
            l=35,
            r=35,
            t=80,
            b=130
        )
    )

    fig.update_xaxes(
        tickangle=-40
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    fig = chart_layout(fig, height=720)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Note: Overall CPI is excluded. The heatmap shows "
        "individual spending category index values. "
        "Higher index values do not directly measure "
        "each category's contribution to inflation."
    )

    # INTERPRETATION

    st.subheader("Interpretation")

    show_interpretation(
        f"Spending category findings for {selected_year}",
        f"{highest_category} recorded the highest average "
        f"CPI among the selected categories, at "
        f"{highest_category_value:.1f}. {highest_state} "
        f"recorded the highest average category CPI across "
        f"the selected categories, at {highest_state_value:.1f}."
    )

    st.write(
        "The heatmap uses colour intensity to show differences "
        "in consumer price index values. Darker red shades "
        "represent higher index values, while lighter shades "
        "represent lower index values."
    )


# =====================================================
# 9. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    <b style="color:#702F3B;">
        Cost of Living Analytics
    </b>
    <br>
    Malaysia State-Level Visualization Project
    <br>
    Scientific Visualisation
</div>
""", unsafe_allow_html=True)
