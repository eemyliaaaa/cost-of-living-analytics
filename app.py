
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Cost of Living Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# 2. COLOUR PALETTE
# ==========================================================

DARK_GREEN = "#064E3B"
EMERALD = "#059669"
LIME = "#84CC16"
GOLD = "#FBBF24"
ORANGE = "#F97316"
RED = "#B91C1C"

BACKGROUND = "#F0FDF4"
WHITE = "#FFFFFF"
TEXT = "#18352B"
MUTED = "#647C6B"
BORDER = "#D1E7D5"

# ==========================================================
# 3. CUSTOM CSS
# ==========================================================

st.markdown("""
<style>
:root {
    --forest: #064E3B;
    --emerald: #059669;
    --mint: #E8F5EC;
    --gold: #FBBF24;
    --ink: #18352B;
    --muted: #647C6B;
    --line: #D8E8DC;
    --surface: #FFFFFF;
}

.stApp {
    background: linear-gradient(180deg, #F4FAF5 0%, #EEF7F0 100%);
    color: var(--ink);
}

.block-container {
    max-width: 1480px;
    padding: 1.7rem 2.2rem 2.8rem 2.2rem;
}

h1, h2, h3, h4 {
    color: var(--forest) !important;
    font-weight: 750 !important;
    letter-spacing: -0.35px;
}

h1 { margin-bottom: .35rem !important; }
h2 { margin-top: .4rem !important; }
p, label, .stCaption { color: var(--ink); }

/* HERO HEADER */
.hero {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    background: linear-gradient(115deg, #053F30 0%, #066B4D 52%, #0B9A6C 100%);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 23px;
    padding: 34px 38px;
    min-height: 205px;
    color: #FFFFFF;
    box-shadow: 0 14px 34px rgba(6,78,59,.16);
    margin-bottom: 23px;
}
.hero:after {
    content: "";
    position: absolute;
    z-index: -1;
    width: 310px;
    height: 310px;
    border-radius: 50%;
    background: rgba(255,255,255,.075);
    right: 65px;
    top: -165px;
}
.hero:before {
    content: "";
    position: absolute;
    z-index: -1;
    width: 210px;
    height: 210px;
    border-radius: 50%;
    background: rgba(251,191,36,.16);
    right: -55px;
    bottom: -135px;
}
.hero-content { position: relative; z-index: 2; }
.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(27px, 3vw, 38px) !important;
    font-weight: 800 !important;
    margin: 0 0 9px 0 !important;
}
.hero p {
    color: #D9F5E5 !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 0;
}
.hero-tag {
    display: inline-block;
    background: #FBBF24;
    color: #064E3B;
    padding: 8px 14px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: .5px;
    margin-top: 20px;
}
.hero-visual {
    position: absolute;
    right: 6%;
    top: 27px;
    z-index: 2;
    font-size: clamp(52px, 7vw, 82px);
    opacity: .95;
    filter: drop-shadow(0 8px 12px rgba(0,0,0,.12));
}

/* SECTION LABELS */
.eyebrow {
    color: #07865F;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1.8px;
    margin: 2px 0 7px 1px;
    text-transform: uppercase;
}

/* TOP NAVIGATION RADIO */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 9px;
    background: rgba(255,255,255,.92);
    border: 1px solid var(--line);
    border-radius: 15px;
    box-shadow: 0 5px 18px rgba(6,78,59,.055);
    width: 100%;
}
div[data-testid="stRadio"] label {
    background: #F3F8F4;
    border: 1px solid #E0ECE2;
    border-radius: 10px;
    padding: 9px 16px;
    transition: all .18s ease;
}
div[data-testid="stRadio"] label:hover {
    background: #E4F4E9;
    border-color: #8CC9A5;
    transform: translateY(-1px);
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: #087B58;
    border-color: #087B58;
    box-shadow: 0 4px 10px rgba(5,150,105,.18);
}
div[data-testid="stRadio"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 750;
}

/* KPI METRIC CARDS */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #FFFFFF 0%, #FBFEFC 100%);
    border: 1px solid #DCEBDD;
    border-top: 4px solid #059669;
    border-radius: 15px;
    padding: 17px 18px 15px 18px;
    min-height: 122px;
    box-shadow: 0 6px 18px rgba(6,78,59,.055);
    transition: transform .18s ease, box-shadow .18s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(6,78,59,.10);
}
[data-testid="stMetricLabel"] {
    color: #647C6B !important;
    font-size: 12px !important;
    font-weight: 650 !important;
}
[data-testid="stMetricValue"] {
    color: #064E3B !important;
    font-size: clamp(21px, 2vw, 29px) !important;
    font-weight: 850 !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* INFORMATION AND INSIGHT CARDS */
.info-card, .objective-card {
    background: #FFFFFF;
    border: 1px solid #DCEBDD;
    border-radius: 15px;
    padding: 20px;
    height: 100%;
    box-shadow: 0 5px 16px rgba(6,78,59,.05);
    transition: transform .18s ease, box-shadow .18s ease;
}
.info-card:hover, .objective-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(6,78,59,.09);
}
.info-card { border-top: 4px solid #0A8A62; }
.info-card h4, .objective-card h4 {
    color: #064E3B;
    font-size: 16px;
    margin: 0 0 9px 0;
}
.info-card p, .objective-card p {
    color: #526B5A;
    font-size: 13px;
    line-height: 1.75;
}
.objective-card {
    border-top: 4px solid #059669;
    min-height: 185px;
}
.objective-card small {
    display: inline-block;
    color: #8A6411;
    background: #FFF6D9;
    border: 1px solid #F5E4A8;
    border-radius: 20px;
    padding: 5px 9px;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: .7px;
}
.insight-card {
    background: #FFFFFF;
    border: 1px solid #E7EDE7;
    border-left: 5px solid #F4B928;
    border-radius: 12px;
    padding: 15px 17px;
    margin-bottom: 12px;
    box-shadow: 0 4px 13px rgba(6,78,59,.045);
}
.insight-card h4 {
    color: #064E3B;
    font-size: 14px;
    font-weight: 750;
    margin: 0 0 6px 0;
}
.insight-card p {
    color: #526B5A;
    font-size: 13px;
    line-height: 1.65;
    margin: 0;
}

/* FILTERS AND INPUTS */
div[data-baseweb="select"] > div {
    border-color: #B7D7BF;
    border-radius: 10px;
    background: #FFFFFF;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #059669;
    box-shadow: 0 0 0 1px #059669;
}
.stMultiSelect, .stSelectbox, .stTextInput, .stNumberInput {
    background: transparent;
}

/* BUTTONS */
.stButton button, .stDownloadButton button {
    background: linear-gradient(110deg, #07845D, #059669);
    color: #FFFFFF;
    border: 0;
    border-radius: 10px;
    padding: .48rem 1rem;
    font-weight: 750;
    box-shadow: 0 4px 10px rgba(5,150,105,.14);
    transition: all .18s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: #064E3B;
    color: #FFFFFF;
    border: 0;
    transform: translateY(-1px);
}

/* CHARTS, TABLES AND EXPANDERS */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E1EBE2;
    border-radius: 15px;
    padding: 8px 8px 2px 8px;
    box-shadow: 0 5px 17px rgba(6,78,59,.045);
}
div[data-testid="stDataFrame"] {
    border: 1px solid #DCEBDD;
    border-radius: 12px;
    overflow: hidden;
}
details[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #DCEBDD;
    border-radius: 12px;
}

/* DIVIDERS AND FOOTER */
hr {
    border-color: #D7E8DA !important;
    margin: 23px 0 !important;
}
.footer {
    text-align: center;
    padding: 24px 16px;
    margin-top: 34px;
    border-top: 1px solid #D3E5D7;
    color: #647C6B;
    font-size: 12px;
    line-height: 1.8;
}

/* RESPONSIVE SPACING */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 2rem 1rem; }
    .hero { padding: 25px 22px; min-height: 175px; }
    .hero-visual { right: 5%; top: 48px; font-size: 48px; opacity: .55; }
    div[data-testid="stRadio"] > div[role="radiogroup"] { gap: 5px; }
    div[data-testid="stRadio"] label { padding: 7px 10px; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# 4. LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    data = pd.read_csv("merged_dataset.csv")

    data.columns = data.columns.str.strip()

    required_columns = [
        "state",
        "year",
        "population",
        "income_mean",
        "income_median",
        "division",
        "index"
    ]

    missing = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing dataset columns: {missing}"
        )

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

except Exception as error:

    st.error(f"Dataset loading error: {error}")
    st.stop()


# ==========================================================
# 5. PREPARE DATA
# ==========================================================

overall_df = df[
    df["division"].str.lower() == "overall"
].copy()

category_df = df[
    df["division"].str.lower() != "overall"
].copy()

if overall_df.empty:
    st.error("Overall CPI records are missing.")
    st.stop()

years = sorted(
    overall_df["year"].unique().astype(int).tolist()
)

states = sorted(
    overall_df["state"].unique().tolist()
)

categories = sorted(
    category_df["division"].unique().tolist()
)

latest_year = max(years)

latest_data = overall_df[
    overall_df["year"] == latest_year
].copy()

if latest_data.empty:
    st.error("Latest year data is unavailable.")
    st.stop()


# ==========================================================
# 6. MALAYSIA STATE COORDINATES
# ==========================================================

# Approximate geographic locations for state markers.
# These are NOT official state boundary polygons.

state_coordinates = {
    "Johor": (1.90, 103.45),
    "Kedah": (6.12, 100.37),
    "Kelantan": (5.35, 102.00),
    "Melaka": (2.19, 102.25),
    "Negeri Sembilan": (2.73, 102.25),
    "Pahang": (3.75, 102.45),
    "Perak": (4.80, 101.00),
    "Perlis": (6.45, 100.20),
    "Pulau Pinang": (5.40, 100.30),
    "Sabah": (5.60, 116.50),
    "Sarawak": (2.80, 113.50),
    "Selangor": (3.20, 101.50),
    "Terengganu": (5.15, 103.00),
    "W.P. Kuala Lumpur": (3.14, 101.69),
    "W.P. Labuan": (5.28, 115.24),
    "W.P. Putrajaya": (2.93, 101.69)
}


# ==========================================================
# 7. HELPER FUNCTIONS
# ==========================================================

def scale_100(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(50, index=series.index)

    return (
        (series - minimum) /
        (maximum - minimum)
    ) * 100


def show_kpis(items):

    cols = st.columns(len(items))

    for col, item in zip(cols, items):

        with col:

            st.metric(
                label=item[0],
                value=item[1]
            )

            st.caption(item[2])


def insight_card(title, message):

    st.markdown(
        f"""
        <div class="insight-card">
            <h4>✨ {title}</h4>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def chart_layout(fig, height=520):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            color=TEXT,
            size=12
        ),
        margin=dict(
            l=35,
            r=35,
            t=75,
            b=65
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color=TEXT
        )
    )

    return fig


def safe_correlation(data, x, y):

    if len(data) < 2:
        return np.nan

    if data[x].nunique() < 2 or data[y].nunique() < 2:
        return np.nan

    return data[x].corr(data[y])


def build_growth_data(selected_states):

    selected = overall_df[
        overall_df["state"].isin(selected_states)
    ].copy()

    selected = selected.sort_values(
        ["state", "year"]
    )

    selected["income_growth"] = (
        selected["income_mean"] /
        selected.groupby("state")["income_mean"].transform("first")
        - 1
    ) * 100

    selected["price_growth"] = (
        selected["index"] /
        selected.groupby("state")["index"].transform("first")
        - 1
    ) * 100

    return selected


# ==========================================================
# 8. HERO HEADER
# ==========================================================

st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>🌿 Cost of Living Analytics</h1>
        <p>MALAYSIA · STATE-LEVEL DATA ANALYSIS</p>
        <div class="hero-tag">
            ✦ DATA INSIGHTS · 2012–2024
        </div>
    </div>
    <div class="hero-visual">📊</div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# 9. NAVIGATION
# ==========================================================

st.markdown(
    '<div class="eyebrow">EXPLORE DASHBOARD</div>',
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


# ==========================================================
# PAGE 1: OVERVIEW
# ==========================================================

if page == "Overview":

    st.markdown(
        '<div class="eyebrow">DASHBOARD OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.title("Malaysia Cost of Living Overview")

    st.write(
        "Explore how household income, population and "
        "consumer prices differ across Malaysian states."
    )

    # -----------------------------------------------
    # KPI CARDS
    # -----------------------------------------------

    show_kpis([
        (
            "Malaysian States",
            f"{overall_df['state'].nunique()}",
            "States and federal territories"
        ),
        (
            "Observation Years",
            f"{min(years)}–{max(years)}",
            f"{len(years)} available years"
        ),
        (
            "Spending Categories",
            f"{len(categories)}",
            "Individual CPI categories"
        ),
        (
            "Dataset Records",
            f"{len(df):,}",
            "Total dataset observations"
        )
    ])

    st.markdown("---")

    # -----------------------------------------------
    # MALAYSIA MAP + SMART INSIGHTS
    # -----------------------------------------------

    st.subheader("Malaysia at a Glance")

    map_col, insight_col = st.columns(
        [1.35, 1],
        gap="large"
    )

    with map_col:

        st.write(
            f"**State-level overview · {latest_year}**"
        )

        map_data = latest_data.copy()

        map_data["latitude"] = map_data["state"].map(
            lambda x: state_coordinates.get(x, (np.nan, np.nan))[0]
        )

        map_data["longitude"] = map_data["state"].map(
            lambda x: state_coordinates.get(x, (np.nan, np.nan))[1]
        )

        map_data = map_data.dropna(
            subset=["latitude", "longitude"]
        )

        fig_map = px.scatter_geo(
            map_data,
            lat="latitude",
            lon="longitude",
            color="index",
            size="population",
            hover_name="state",
            hover_data={
                "latitude": False,
                "longitude": False,
                "population": ":.1f",
                "income_mean": ":,.0f",
                "index": ":.1f"
            },
            color_continuous_scale=[
                "#BBF7D0",
                "#84CC16",
                "#FBBF24",
                "#F97316",
                "#B91C1C"
            ],
            size_max=24
        )

        fig_map.update_geos(
            scope="asia",
            projection_type="mercator",
            center=dict(
                lat=4.5,
                lon=109
            ),
            lataxis_range=[-1, 8],
            lonaxis_range=[98, 120],
            showland=True,
            landcolor="#E8F3E8",
            showocean=True,
            oceancolor="#EAF5FC",
            showcountries=True,
            countrycolor="#FFFFFF",
            showcoastlines=True,
            coastlinecolor="#A7B9A8",
            showframe=False,
            showlakes=True
        )

        fig_map.update_layout(
            height=430,
            title="Malaysian State Indicators",
            coloraxis_colorbar=dict(
                title="Overall CPI"
            ),
            margin=dict(
                l=0,
                r=0,
                t=60,
                b=0
            )
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

        st.caption(
            "Note: Map markers represent approximate state "
            "locations. Bubble size represents population."
        )

    with insight_col:

        st.write("**✨ Smart Insights**")

        max_income = latest_data.loc[
            latest_data["income_mean"].idxmax()
        ]

        max_population = latest_data.loc[
            latest_data["population"].idxmax()
        ]

        max_cpi = latest_data.loc[
            latest_data["index"].idxmax()
        ]

        min_cpi = latest_data.loc[
            latest_data["index"].idxmin()
        ]

        insight_card(
            "Highest Household Income",
            f"{max_income['state']} recorded the highest "
            f"mean household income at RM "
            f"{max_income['income_mean']:,.0f}."
        )

        insight_card(
            "Largest Population",
            f"{max_population['state']} had the largest "
            f"population, at "
            f"{max_population['population']:,.1f} thousand."
        )

        insight_card(
            "Highest Overall CPI",
            f"{max_cpi['state']} recorded the highest "
            f"overall CPI of {max_cpi['index']:.1f}."
        )

        insight_card(
            "Lowest Overall CPI",
            f"{min_cpi['state']} recorded the lowest "
            f"overall CPI of {min_cpi['index']:.1f}."
        )

    st.markdown("---")

    # -----------------------------------------------
    # OBJECTIVES
    # -----------------------------------------------

    st.subheader("Explore the Analysis")

    st.write(
        "The dashboard consists of three main analytical objectives."
    )

    obj1, obj2, obj3 = st.columns(3, gap="medium")

    with obj1:

        st.markdown("""
        <div class="objective-card">
            <h4>📈 Objective 1</h4>
            <b>Income vs Price Growth</b>
            <p>Compare income growth and price growth
            to identify changes in affordability
            across Malaysian states.</p>
            <small>LINE CHART</small>
        </div>
        """, unsafe_allow_html=True)

    with obj2:

        st.markdown("""
        <div class="objective-card">
            <h4>📊 Objective 2</h4>
            <b>Population, Income and Prices</b>
            <p>Examine whether states with larger
            populations also have higher income
            and consumer prices.</p>
            <small>DUMBBELL CHART</small>
        </div>
        """, unsafe_allow_html=True)

    with obj3:

        st.markdown("""
        <div class="objective-card">
            <h4>🔥 Objective 3</h4>
            <b>Spending Category Analysis</b>
            <p>Identify differences in food, housing,
            transport and other spending categories
            across Malaysian states.</p>
            <small>HEATMAP</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------------------------
    # DATASET INFORMATION
    # -----------------------------------------------

    st.subheader("Dataset Information")

    info1, info2 = st.columns(2)

    with info1:

        st.markdown("""
        <div class="info-card">
            <h4>📁 Data Overview</h4>
            <p>
            <b>Geographical coverage:</b> Malaysia<br>
            <b>Observation period:</b> 2012–2024<br>
            <b>Data dimensions:</b> State, year and spending category<br>
            <b>Key indicators:</b> Population, mean income,
            median income and CPI.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with info2:

        st.markdown("""
        <div class="info-card">
            <h4>📊 Analysis Variables</h4>
            <p>
            <b>Population:</b> State population (thousands)<br>
            <b>Mean income:</b> Average household income<br>
            <b>Median income:</b> Middle household income<br>
            <b>CPI:</b> Consumer Price Index by category
            and overall.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================================
# PAGE 2: INCOME VS PRICE GROWTH
# ==========================================================

elif page == "Income & Price":

    st.markdown(
        '<div class="eyebrow">OBJECTIVE 1 · LINE CHART</div>',
        unsafe_allow_html=True
    )

    st.title("Income Growth vs Price Growth")

    st.write(
        "Compare changes in household income and consumer "
        "prices to understand affordability."
    )

    # FILTER

    selected_states = st.multiselect(
        "Select Malaysian States",
        states,
        default=states,
        key="income_states"
    )

    if not selected_states:

        st.warning("Please select at least one state.")
        st.stop()

    growth = build_growth_data(selected_states)

    # AVERAGE BY YEAR

    line_data = growth.groupby("year")[
        ["income_growth", "price_growth"]
    ].mean().reset_index()

    last = line_data.iloc[-1]

    income_growth = last["income_growth"]
    price_growth = last["price_growth"]

    gap = income_growth - price_growth

    show_kpis([
        (
            "Income Growth",
            f"{income_growth:.2f}%",
            "Average since each state's first observation"
        ),
        (
            "CPI Growth",
            f"{price_growth:.2f}%",
            "Average since each state's first observation"
        ),
        (
            "Affordability Gap",
            f"{gap:.2f} pp",
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
            line=dict(
                color=EMERALD,
                width=4
            ),
            marker=dict(
                size=10,
                color=EMERALD
            ),
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
            line=dict(
                color=GOLD,
                width=4
            ),
            marker=dict(
                size=10,
                color=GOLD,
                line=dict(
                    color=DARK_GREEN,
                    width=1
                )
            ),
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
        "Note: Each state uses its earliest available year "
        "as the base year. The chart displays the unweighted "
        "average across the selected states."
    )

    # SMART INTERPRETATION

    st.subheader("✨ Smart Analysis")

    if gap > 0:

        insight_card(
            "Income grew faster than consumer prices",
            f"Income growth was {income_growth:.2f}%, "
            f"while CPI growth was {price_growth:.2f}%. "
            f"The difference was {gap:.2f} percentage points."
        )

    elif gap < 0:

        insight_card(
            "Consumer prices grew faster than income",
            f"CPI growth exceeded income growth by "
            f"{abs(gap):.2f} percentage points. "
            "This may indicate greater affordability pressure."
        )

    else:

        insight_card(
            "Income and CPI growth are equal",
            "The average growth rates are approximately equal."
        )

    st.write(
        "A positive affordability gap means income growth "
        "is higher than CPI growth. A negative gap indicates "
        "that consumer prices increased faster than income."
    )

    # STATE DETAIL TABLE

    with st.expander("View state-level growth data"):

        st.dataframe(
            growth[
                [
                    "state",
                    "year",
                    "income_growth",
                    "price_growth"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# PAGE 3: STATE COMPARISON
# ==========================================================

elif page == "State Comparison":

    st.markdown(
        '<div class="eyebrow">OBJECTIVE 2 · DUMBBELL CHART</div>',
        unsafe_allow_html=True
    )

    st.title("Population, Income and CPI Across States")

    st.write(
        "Examine differences in population, mean household "
        "income and overall CPI across Malaysian states."
    )

    selected_year = st.selectbox(
        "Select Observation Year",
        years,
        index=years.index(latest_year),
        key="comparison_year"
    )

    comparison = overall_df[
        overall_df["year"] == selected_year
    ].copy()

    comparison["income_scaled"] = scale_100(
        comparison["income_mean"]
    )

    comparison["cpi_scaled"] = scale_100(
        comparison["index"]
    )

    comparison = comparison.sort_values(
        "income_scaled"
    )

    highest_income = comparison.loc[
        comparison["income_mean"].idxmax()
    ]

    highest_population = comparison.loc[
        comparison["population"].idxmax()
    ]

    highest_cpi = comparison.loc[
        comparison["index"].idxmax()
    ]

    corr_income = safe_correlation(
        comparison,
        "population",
        "income_mean"
    )

    corr_cpi = safe_correlation(
        comparison,
        "population",
        "index"
    )

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
            "Highest CPI",
            highest_cpi["state"],
            f'{highest_cpi["index"]:.1f}'
        )
    ])

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Population–Income Correlation",
            "N/A" if pd.isna(corr_income) else f"{corr_income:.3f}"
        )

    with c2:

        st.metric(
            "Population–CPI Correlation",
            "N/A" if pd.isna(corr_cpi) else f"{corr_cpi:.3f}"
        )

    st.caption(
        "Correlation measures linear association, not causation."
    )

    st.markdown("---")

    # DUMBBELL CHART

    fig = go.Figure()

    for _, row in comparison.iterrows():

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
                    color="#B8CBB9",
                    width=2.5
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    max_population = comparison["population"].max()

    bubble_sizes = (
        comparison["population"] /
        max_population * 25 + 8
    )

    fig.add_trace(
        go.Scatter(
            x=comparison["income_scaled"],
            y=comparison["state"],
            mode="markers",
            name="Mean Income",
            marker=dict(
                color=EMERALD,
                size=bubble_sizes,
                line=dict(
                    color=WHITE,
                    width=1.5
                )
            ),
            customdata=np.column_stack([
                comparison["income_mean"],
                comparison["population"]
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

    fig.add_trace(
        go.Scatter(
            x=comparison["cpi_scaled"],
            y=comparison["state"],
            mode="markers",
            name="Overall CPI",
            marker=dict(
                color=GOLD,
                size=bubble_sizes,
                line=dict(
                    color=WHITE,
                    width=1.5
                )
            ),
            customdata=np.column_stack([
                comparison["index"],
                comparison["population"]
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
        title=f"Population, Income and CPI Across Malaysian States ({selected_year})",
        xaxis_title="Standardized Value (0–100)",
        yaxis_title="Malaysian States",
        legend_title="Indicator",
        height=680
    )

    fig.update_xaxes(
        range=[-5, 105],
        showgrid=True,
        gridcolor="#E5EEE6"
    )

    fig = chart_layout(fig, height=680)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Note: Income and CPI are independently standardized "
        "to 0–100. Bubble size represents state population "
        "in thousands."
    )

    # INTERPRETATION

    st.subheader("✨ Smart Analysis")

    if pd.isna(corr_income):
        income_text = "Population–income correlation is unavailable."
    elif corr_income > 0:
        income_text = "Population and mean household income show a positive association."
    elif corr_income < 0:
        income_text = "Population and mean household income show a negative association."
    else:
        income_text = "No linear population–income association was observed."

    if pd.isna(corr_cpi):
        cpi_text = "Population–CPI correlation is unavailable."
    elif corr_cpi > 0:
        cpi_text = "Population and CPI show a positive association."
    elif corr_cpi < 0:
        cpi_text = "Population and CPI show a negative association."
    else:
        cpi_text = "No linear population–CPI association was observed."

    insight_card(
        f"State comparison for {selected_year}",
        f"{highest_population['state']} recorded the highest "
        f"population. {highest_income['state']} recorded the "
        f"highest mean income, while {highest_cpi['state']} "
        f"recorded the highest CPI. {income_text} {cpi_text}"
    )

    with st.expander("View detailed state comparison"):

        st.dataframe(
            comparison[
                [
                    "state",
                    "population",
                    "income_mean",
                    "income_median",
                    "index",
                    "income_scaled",
                    "cpi_scaled"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# PAGE 4: CPI HEATMAP
# ==========================================================

elif page == "CPI Heatmap":

    st.markdown(
        '<div class="eyebrow">OBJECTIVE 3 · HEATMAP</div>',
        unsafe_allow_html=True
    )

    st.title("CPI by Spending Category")

    st.write(
        "Identify which spending categories have higher "
        "consumer price index values across Malaysian states."
    )

    selected_year = st.selectbox(
        "Select Observation Year",
        years,
        index=years.index(latest_year),
        key="heatmap_year"
    )

    year_categories = category_df[
        category_df["year"] == selected_year
    ].copy()

    available_categories = sorted(
        year_categories["division"].unique()
    )

    selected_categories = st.multiselect(
        "Select Spending Categories",
        available_categories,
        default=available_categories,
        key="selected_heatmap_categories"
    )

    if not selected_categories:

        st.warning("Please select at least one category.")
        st.stop()

    heatmap_data = year_categories[
        year_categories["division"].isin(selected_categories)
    ].copy()

    heatmap_pivot = heatmap_data.pivot(
        index="state",
        columns="division",
        values="index"
    )

    category_average = heatmap_data.groupby(
        "division"
    )["index"].mean()

    state_average = heatmap_data.groupby(
        "state"
    )["index"].mean()

    highest_category = category_average.idxmax()
    highest_state = state_average.idxmax()

    overall_average = heatmap_data["index"].mean()

    show_kpis([
        (
            "Highest CPI Category",
            highest_category,
            f"{category_average.max():.1f} average index"
        ),
        (
            "Highest Average CPI State",
            highest_state,
            f"{state_average.max():.1f} average index"
        ),
        (
            "Average Category CPI",
            f"{overall_average:.1f}",
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
            "#F0FDF4",
            "#BBF7D0",
            "#84CC16",
            "#FBBF24",
            "#F97316",
            "#B91C1C"
        ],
        labels={
            "x": "Spending Categories",
            "y": "Malaysian States",
            "color": "CPI Index"
        },
        title=(
            "Consumer Price Index by Spending Category "
            f"Across Malaysian States ({selected_year})"
        )
    )

    fig.update_layout(
        height=720,
        margin=dict(
            l=35,
            r=35,
            t=80,
            b=140
        ),
        coloraxis_colorbar=dict(
            title="CPI Index"
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
        "Note: Overall CPI is excluded. Higher index values "
        "indicate a higher price index relative to the "
        "reference period, not necessarily a larger "
        "contribution to inflation."
    )

    # INTERPRETATION

    st.subheader("✨ Smart Analysis")

    insight_card(
        "Highest average spending category",
        f"{highest_category} recorded the highest average "
        f"CPI among the selected categories, with an index "
        f"of {category_average.max():.1f}."
    )

    insight_card(
        "Highest average state CPI",
        f"{highest_state} recorded the highest average "
        f"category CPI at {state_average.max():.1f}."
    )

    # CATEGORY RANKING

    st.subheader("Spending Category Ranking")

    ranking = (
        category_average
        .sort_values(ascending=False)
        .reset_index()
    )

    ranking.columns = [
        "Spending Category",
        "Average CPI"
    ]

    fig_rank = px.bar(
        ranking,
        x="Average CPI",
        y="Spending Category",
        orientation="h",
        text="Average CPI",
        color="Average CPI",
        color_continuous_scale=[
            "#BBF7D0",
            "#84CC16",
            "#FBBF24",
            "#F97316"
        ]
    )

    fig_rank.update_layout(
        title="Average CPI by Spending Category",
        yaxis=dict(
            autorange="reversed"
        ),
        coloraxis_showscale=False
    )

    fig_rank = chart_layout(fig_rank, height=550)

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )

    with st.expander("View category data"):

        st.dataframe(
            ranking.round(2),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# 10. FOOTER
# ==========================================================

st.markdown("""
<div class="footer">
    <b style="color:#064E3B;font-size:14px;">
        🌿 COST OF LIVING ANALYTICS
    </b>
    <br><br>
    Malaysia State-Level Data Analysis
    <br>
    Population · Household Income · Consumer Price Index
    <br><br>
    <span style="color:#059669;">
        Data Visualization Project
    </span>
</div>
""", unsafe_allow_html=True)
