import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import io
import hashlib
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="DataLens | EDA Workspace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.set_page_config(
    page_title="DataLens | EDA Workspace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ===== MAIN APPLICATION ===== */
.stApp {
    background: #0B1120;
    color: #F8FAFC;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #0F172A;
    border-right: 1px solid #263750;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

/* ===== HEADINGS AND TEXT ===== */
h1, h2, h3 {
    color: #F8FAFC;
    letter-spacing: -0.4px;
}

p, label, [data-testid="stCaptionContainer"] {
    color: #CBD5E1;
}

/* ===== TABS ===== */
button[data-baseweb="tab"] {
    color: #94A3B8;
    font-weight: 600;
    padding: 12px 16px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #22D3EE;
    border-bottom-color: #22D3EE;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: #111C30;
    border: 1px solid #263750;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC;
}

/* ===== BUTTONS ===== */
.stButton > button,
.stDownloadButton > button {
    background: #0891B2;
    color: #FFFFFF;
    border: 1px solid #22D3EE;
    border-radius: 8px;
    font-weight: 600;
    transition: background 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #0E7490;
    color: #FFFFFF;
    border-color: #67E8F9;
}

/* ===== INPUTS AND SELECTBOXES ===== */
[data-baseweb="input"],
[data-baseweb="select"] > div,
[data-baseweb="textarea"] {
    background: #111C30;
    border-color: #334155;
    border-radius: 8px;
}

/* ===== CONTAINERS ===== */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827;
    border: 1px solid #263750;
    border-radius: 12px;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border: 1px solid #263750;
    border-radius: 10px;
    overflow: hidden;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #263750;
}

/* ===== ALERTS ===== */
[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
<div style="padding: 12px 0 22px 0;">
    <div style="font-size: 30px; font-weight: 800; color: #67E8F9;">
        📊 DataLens
    </div>
    <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px;">
        Explore. Understand. Transform.
    </div>
    <hr style="border-color: #374151; margin-top: 20px;">
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📂 Upload Dataset")

data = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="Upload the dataset you want to explore and clean."
)

if data is not None:
    try:
        file_bytes = data.getvalue()
        dataset_key = hashlib.sha256(file_bytes).hexdigest()

        loaded_df = pd.read_csv(io.BytesIO(file_bytes))

        if st.session_state.get("dataset_key") != dataset_key:
            st.session_state.dataset_key = dataset_key
            st.session_state.original_df = loaded_df.copy()
            st.session_state.working_df = loaded_df.copy()

        original_df = st.session_state.original_df
        working_df = st.session_state.working_df

        st.sidebar.success("Dataset loaded successfully!")

    except Exception as e:
        st.sidebar.error(f"Unable to read this CSV: {e}")
        st.stop()
else:
    st.sidebar.info("Upload a CSV file to get started.")
    st.info("Upload your dataset in the sidebar")
    st.stop()

overview, data_explore, data_cleaning, visualization, compare_changes, export = st.tabs(["Overview", "Data Explore", "Data Cleaning", "Visualization", "Compare Changes", "Export"], width="stretch", )


if data is not None:
    with overview:
        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / OVERVIEW</div>
            <h1 class="explore-heading">Your Dataset at a Glance</h1>
            <p class="explore-subtitle">
                Understand your data structure, quality, and composition
                                before starting your analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)


        df = original_df

        st.markdown("### 📌 Dataset Summary")
        st.caption(
            "An overview of the original dataset as it was uploaded."
        )

        with st.container(border=True):
            st.markdown("#### 📂 File Information")

            st.markdown(
                f"""
                <div style="
                    background: #111C30;
                    border: 1px solid #263750;
                    border-radius: 10px;
                    padding: 14px 16px;
                    margin-bottom: 16px;
                ">
                    <div style="
                        color: #94A3B8;
                        font-size: 12px;
                        margin-bottom: 5px;
                    ">UPLOADED FILE</div>
                    <div style="
                        color: #67E8F9;
                        font-size: 17px;
                        font-weight: 650;
                        overflow-wrap: anywhere;
                    ">📄 {data.name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # First row of metrics
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "📄 Total Rows",
                f"{df.shape[0]:,}"
            )

            col2.metric(
                "📊 Total Columns",
                f"{df.shape[1]:,}"
            )

            col3.metric(
                "🧠 Memory Usage",
                f"{df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB"
            )

            # Second row of metrics
            col4, col5, col6 = st.columns(3)

            col4.metric(
                "🕳️ Missing Values",
                f"{df.isna().sum().sum():,}"
            )

            col5.metric(
                "♻️ Duplicate Rows",
                f"{df.duplicated().sum():,}"
            )

            col6.metric(
                "🧩 Numeric Columns",
                f"{len(df.select_dtypes(include='number').columns):,}"
            )

        # ---------- Column Type Distribution ----------
        st.markdown("")
        st.markdown("### 🧩 Column Type Distribution")
        st.caption(
            "See how your dataset's columns are distributed by data type."
        )

        numeric_cols = list(
            df.select_dtypes(include="number").columns
        )

        categorical_cols = list(
            df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns
        )

        datetime_cols = list(
            df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )

        classified_cols = (
            numeric_cols + categorical_cols + datetime_cols
        )

        other_cols = [
            col for col in df.columns
            if col not in classified_cols
        ]

        type_counts = [
            ("Numerical", len(numeric_cols), "#22D3EE"),
            ("Categorical", len(categorical_cols), "#A78BFA"),
            ("Datetime", len(datetime_cols), "#34D399"),
            ("Other", len(other_cols), "#FBBF24"),
        ]

        total_cols = len(df.columns)

        if total_cols > 0:
            with st.container(border=True):
                
                segments = ""

                for label, count, color in type_counts:
                    if count == 0:
                        continue

                    percentage = count / total_cols * 100

                    segments += f"""
                    <div title="{label}: {count} columns ({percentage:.1f}%)"
                         style="
                            width: {percentage}%;
                            background: {color};
                            height: 100%;
                            min-width: 2px;
                         ">
                    </div>
                    """

                st.markdown(
                    f"""
                    <div style="
                        display: flex;
                        width: 100%;
                        height: 14px;
                        border-radius: 8px;
                        overflow: hidden;
                        background: #263750;
                        margin: 10px 0 22px 0;
                    ">
                        {segments}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown("""
                <style>
                .datalens-legend-card {
                    background: #111C30;
                    border: 1px solid #263750;
                    border-radius: 10px;
                    padding: 12px;
                    min-height: 94px;
                }

                .datalens-legend-label {
                    font-size: 12px;
                    font-weight: 650;
                    margin-bottom: 8px;
                }

                .datalens-legend-count {
                    color: #F8FAFC;
                    font-size: 23px;
                    font-weight: 750;
                }

                .datalens-legend-percentage {
                    color: #94A3B8;
                    font-size: 12px;
                }
                </style>
                """, unsafe_allow_html=True)
                # Distribution legend
                legend_cols = st.columns(4)

                for i, (label, count, color) in enumerate(type_counts):
                    percentage = (
                        count / total_cols * 100
                        if total_cols else 0
                    )

                    with legend_cols[i]:
                        st.markdown(
                            f"""
                            <div class="datalens-legend-card">
                                <div class="datalens-legend-label" style="color: {color};">
                                    ● {label}
                                </div>
                                <div class="datalens-legend-count">{count}</div>
                                <div class="datalens-legend-percentage">
                                    {percentage:.1f}% of columns
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with st.expander("🔎 View columns by data type"):

                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:
                        st.markdown("##### 🔢 Numerical")
                        st.write(
                            ", ".join(numeric_cols)
                            if numeric_cols else "No numerical columns"
                        )

                        st.markdown("##### 🔤 Categorical")
                        st.write(
                            ", ".join(categorical_cols)
                            if categorical_cols else "No categorical columns"
                        )

                    with detail_col2:
                        st.markdown("##### 📅 Datetime")
                        st.write(
                            ", ".join(datetime_cols)
                            if datetime_cols else "No datetime columns"
                        )

                        st.markdown("##### 🧩 Other")
                        st.write(
                            ", ".join(other_cols)
                            if other_cols else "No other columns"
                        )

        else:
            st.warning("The uploaded dataset contains no columns.")

        st.markdown("")
        st.markdown("### 🗃️ Dataset Preview")
        st.caption(
            "Explore the original uploaded records. "
            "Cleaning operations will not change this preview."
        )

        with st.container(border=True):
            preview_col1, preview_col2 = st.columns([3, 1])

            with preview_col1:
                st.markdown("#### Raw Data")

            with preview_col2:
                st.markdown(
                    f"""
                    <div style="
                        text-align: right;
                        color: #94A3B8;
                        padding-top: 5px;
                    ">
                        {len(df):,} rows · {len(df.columns):,} columns
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.dataframe(
                df,
                use_container_width=True,
                height=420,
                hide_index=True
            )

        st.caption(
            "DataLens · Overview is based on the original uploaded dataset."
        )
        

    with data_explore:
        df = st.session_state.get("working_df", original_df)

        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / EXPLORATION</div>
            <h1 class="explore-heading">Explore Your Data</h1>
            <p class="explore-subtitle">
                Dive into individual columns, understand distributions,
                inspect data quality, and discover patterns in your dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)

        total_rows, total_cols = df.shape
        total_missing = int(df.isna().sum().sum())
        total_duplicates = int(df.duplicated().sum())
        total_cells = total_rows * total_cols

        missing_percentage = (
            total_missing / total_cells * 100
            if total_cells > 0 else 0
        )

        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=["object", "category", "bool", "string"]
            ).columns
        )

        datetime_columns = list(
            df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )

        st.markdown("### Dataset Snapshot")
        st.caption("A live overview of your current working dataset.")

        s1, s2, s3, s4 = st.columns(4)

        s1.metric("Total Rows", f"{total_rows:,}")
        s2.metric("Total Columns", f"{total_cols:,}")
        s3.metric("Missing Values", f"{total_missing:,}")
        s4.metric("Duplicate Rows", f"{total_duplicates:,}")

        st.progress(
            min(missing_percentage / 100, 1.0),
            text=f"{missing_percentage:.2f}% of all cells are missing"
        )

        st.divider()

        if total_cols == 0:
            st.warning("The uploaded dataset has no columns to explore.")

        else:
            st.markdown("### Column Inspector")
            st.caption(
                "Select a column to inspect its datatype, quality, "
                "and statistical properties."
            )

            selected_col = st.selectbox(
                "Choose a column",
                options=list(df.columns),
                key="explore_selected_column"
            )

            series = df[selected_col]

            non_missing = series.dropna()
            missing_count = int(series.isna().sum())
            unique_count = int(series.nunique())
            missing_col_pct = (
                missing_count / len(df) * 100
                if len(df) > 0 else 0
            )
            memory_mb = (
                series.memory_usage(deep=True, index=False)
                / (1024 ** 2)
            )

            st.markdown("#### Column Information")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Data Type", str(series.dtype))
            c2.metric("Missing Values", f"{missing_count:,}")
            c3.metric("Unique Values", f"{unique_count:,}")
            c4.metric("Memory Usage", f"{memory_mb:.3f} MB")

            c5, c6, c7 = st.columns(3)

            c5.metric("Missing Percentage", f"{missing_col_pct:.2f}%")
            c6.metric("Non-Missing Values", f"{len(non_missing):,}")

            if len(series) > 0:
                c7.metric(
                    "Unique Ratio",
                    f"{unique_count / len(series) * 100:.2f}%"
                )
            else:
                c7.metric("Unique Ratio", "N/A")

            # ---------- Column Statistics ----------
            st.markdown("#### Statistical Profile")

            if pd.api.types.is_numeric_dtype(series):

                stat1, stat2, stat3 = st.columns(3)
                stat4, stat5, stat6 = st.columns(3)

                stat1.metric(
                    "Mean",
                    f"{series.mean():,.4f}"
                    if non_missing.size else "N/A"
                )

                stat2.metric(
                    "Median",
                    f"{series.median():,.4f}"
                    if non_missing.size else "N/A"
                )

                mode_values = series.mode(dropna=True)

                stat3.metric(
                    "Mode",
                    str(mode_values.iloc[0])
                    if not mode_values.empty else "N/A"
                )

                stat4.metric(
                    "Standard Deviation",
                    f"{series.std():,.4f}"
                    if non_missing.size > 1 else "N/A"
                )

                stat5.metric(
                    "Minimum",
                    f"{series.min():,.4f}"
                    if non_missing.size else "N/A"
                )

                stat6.metric(
                    "Maximum",
                    f"{series.max():,.4f}"
                    if non_missing.size else "N/A"
                )

                with st.expander("View detailed numerical statistics"):
                    st.dataframe(
                        series.describe().to_frame("Value"),
                        use_container_width=True
                    )

            elif (
                pd.api.types.is_datetime64_any_dtype(series)
            ):
                stat1, stat2, stat3 = st.columns(3)

                stat1.metric(
                    "Earliest Date",
                    str(series.min()) if non_missing.size else "N/A"
                )

                stat2.metric(
                    "Latest Date",
                    str(series.max()) if non_missing.size else "N/A"
                )

                mode_values = series.mode(dropna=True)

                stat3.metric(
                    "Most Frequent",
                    str(mode_values.iloc[0])
                    if not mode_values.empty else "N/A"
                )

            else:
                mode_values = series.mode(dropna=True)

                mode_value = (
                    mode_values.iloc[0]
                    if not mode_values.empty else "N/A"
                )

                mode_frequency = (
                    int(series.value_counts(dropna=True).iloc[0])
                    if not series.value_counts(dropna=True).empty else 0
                )

                stat1, stat2, stat3 = st.columns(3)

                stat1.metric("Most Frequent Value", str(mode_value))
                stat2.metric("Mode Frequency", f"{mode_frequency:,}")
                stat3.metric(
                    "Distinct Values",
                    f"{unique_count:,}"
                )

                with st.expander("View most frequent values"):
                    frequency_table = (
                        series.value_counts(dropna=True)
                        .head(10)
                        .rename_axis("Value")
                        .reset_index(name="Frequency")
                    )

                    st.dataframe(
                        frequency_table,
                        use_container_width=True,
                        hide_index=True
                    )

            # ---------- Selected Column Preview ----------
            with st.expander("Preview selected column"):
                st.dataframe(
                    series.to_frame().head(100),
                    use_container_width=True,
                    height=300
                )

            st.divider()
            
            st.markdown("### Complete Column Information")
            st.caption(
                "Review the datatype, unique count, missing count, "
                "and memory usage of every column."
            )

            column_info = pd.DataFrame({
                "Column Name": df.columns.astype(str),
                "Data Type": [str(dtype) for dtype in df.dtypes],
                "Non-Missing": [
                    int(df[col].notna().sum()) for col in df.columns
                ],
                "Unique Values": [
                    int(df[col].nunique()) for col in df.columns
                ],
                "Missing Values": [
                    int(df[col].isna().sum()) for col in df.columns
                ],
                "Missing %": [
                    round(
                        df[col].isna().sum() / len(df) * 100, 2
                    ) if len(df) > 0 else 0
                    for col in df.columns
                ],
                "Memory (MB)": [
                    round(
                        df[col].memory_usage(deep=True, index=False)
                        / (1024 ** 2), 4
                    )
                    for col in df.columns
                ]
            })

            st.dataframe(
                column_info,
                use_container_width=True,
                height=350,
                hide_index=True
            )

            st.divider()
            st.markdown("### Descriptive Statistics")
            st.caption(
                "Summarize numerical columns and, optionally, "
                "include statistics for categorical columns."
            )

            include_all_stats = st.checkbox(
                "Include categorical and other column statistics",
                value=False,
                key="explore_include_all_stats"
            )

            try:
                if include_all_stats:
                    descriptive_stats = df.describe(
                        include="all"
                    ).T
                else:
                    descriptive_stats = df.describe().T

                if descriptive_stats.empty:
                    st.info(
                        "No numerical columns are available for "
                        "descriptive statistics. Enable the option above "
                        "to inspect other column types."
                    )
                else:
                    st.dataframe(
                        descriptive_stats,
                        use_container_width=True,
                        height=350
                    )

            except Exception as e:
                st.warning(
                    f"Could not calculate descriptive statistics: {e}"
                )

            st.divider()

            st.markdown("### Missing Value Analysis")
            st.caption(
                "Identify which columns have missing values and "
                "where further cleaning may be needed."
            )

            missing_by_column = df.isna().sum()
            missing_by_column = missing_by_column[
                missing_by_column > 0
            ].sort_values(ascending=False)

            if missing_by_column.empty:
                st.success(
                    "Excellent! No missing values were found "
                    "in the current working dataset."
                )
            else:
                chart_col, table_col = st.columns(
                    [1.5, 1], gap="large"
                )

                with chart_col:
                    st.markdown("#### Missing Values by Column")

                    st.bar_chart(
                        missing_by_column,
                        horizontal=True,
                        x_label="Missing Value Count",
                        y_label="Column"
                    )

                with table_col:
                    st.markdown("#### Missing Value Details")

                    missing_info = pd.DataFrame({
                        "Missing Count": missing_by_column,
                        "Missing %": [
                            round(
                                df[col].isna().sum() / len(df) * 100, 2
                            ) if len(df) > 0 else 0
                            for col in missing_by_column.index
                        ]
                    })

                    st.dataframe(
                        missing_info,
                        use_container_width=True,
                        height=350
                    )

            st.divider()

            # ==========================================
            # 5. SEARCH AND PREVIEW DATA
            # ==========================================
            st.markdown("### Explore Dataset Rows")
            st.caption(
                "Search the current working dataset to find records "
                "containing a particular value."
            )

            search_text = st.text_input(
                "Search across all columns",
                placeholder="e.g. London, 25, Female...",
                key="explore_search_text"
            )

            if search_text.strip():
                search_mask = df.astype("string").apply(
                    lambda column: column.str.contains(
                        search_text,
                        case=False,
                        na=False,
                        regex=False
                    )
                ).any(axis=1)

                filtered_df = df.loc[search_mask]

                st.caption(
                    f"Found {len(filtered_df):,} matching row(s)."
                )
            else:
                filtered_df = df

            st.dataframe(
                filtered_df.head(500),
                use_container_width=True,
                height=400,
                hide_index=True
            )

            st.caption(
                f"Showing up to 500 rows from "
                f"{len(filtered_df):,} matching row(s)."
            )



    with data_cleaning:
        
        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / WORKSPACE</div>
            <h1 class="explore-heading">Data Cleaning Studio</h1>
            <p class="explore-subtitle">
                Inspect, clean, and prepare your dataset with practical
                data-quality tools. Changes apply to your working dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        df = st.session_state.working_df

        if df.empty and len(df.columns) == 0:
            st.warning("Your working dataset has no rows or columns.")

        else:
            st.markdown("### Dataset Quality")
            st.caption("A quick snapshot of your current working dataset.")

            total_missing = int(df.isna().sum().sum())
            total_duplicates = int(df.duplicated().sum())
            total_cells = df.shape[0] * df.shape[1]
            missing_pct = (
                (total_missing / total_cells) * 100
                if total_cells > 0 else 0
            )

            m1, m2, m3, m4 = st.columns(4)

            m1.metric("Total Rows", f"{df.shape[0]:,}")
            m2.metric("Total Columns", f"{df.shape[1]:,}")
            m3.metric("Missing Values", f"{total_missing:,}")
            m4.metric("Duplicate Rows", f"{total_duplicates:,}")

            st.progress(
                min(missing_pct / 100, 1.0),
                text=f"Missing cells: {missing_pct:.2f}% of all dataset cells"
            )

            st.divider()

            # ---------- Cleaning Tools ----------
            st.markdown("### Cleaning Tools")
            st.caption(
                "Choose a tool below. Each action updates the working dataset."
            )

            with st.expander("🔤  Datatype Conversion", expanded=True):

                if len(df.columns) > 0:

                    c1, c2, c3 = st.columns([2, 1.5, 2])

                    with c1:
                        dtype_col = st.selectbox(
                            "Select column",
                            options=list(df.columns),
                            key="clean_dtype_column"
                        )
                    with c2:
                        st.markdown("**Current datatype**")
                        st.code(str(df[dtype_col].dtype))


                    with c3:
                        target_dtype = st.selectbox(
                            "Convert to",
                            options=[
                                "string",
                                "Int64",
                                "float64",
                                "category",
                                "datetime"
                            ],
                            key="clean_target_dtype"
                        )

                    st.caption(
                        "Tip: converting text to numbers may fail if the "
                        "column contains non-numeric values."
                    )

                    if st.button(
                        "Apply Datatype Conversion",
                        key="apply_dtype",
                        type="primary"
                    ):
                        try:
                            converted = df[dtype_col].copy()

                            if target_dtype == "datetime":
                                converted = pd.to_datetime(
                                    converted, errors="raise"
                                )
                            elif target_dtype == "Int64":
                                converted = pd.to_numeric(
                                    converted, errors="raise"
                                ).astype("Int64")
                            elif target_dtype == "float64":
                                converted = pd.to_numeric(
                                    converted, errors="raise"
                                ).astype("float64")
                            elif target_dtype == "string":
                                converted = converted.astype("string")
                            elif target_dtype == "category":
                                converted = converted.astype("category")

                            st.session_state.working_df[dtype_col] = converted

                            st.success(
                                f"'{dtype_col}' converted to "
                                f"{target_dtype} successfully."
                            )                        

                        except Exception as e:
                            st.error(f"Conversion failed: {e}")

                else:
                    st.info("No columns are available for conversion.")

            with st.expander("🩹 Missing Values", expanded=False):

                working = st.session_state.working_df

                # Find columns that actually contain missing values
                missing_counts = working.isna().sum()
                columns_with_missing = missing_counts[missing_counts > 0]

                if columns_with_missing.empty:
                    st.success("No missing values found in the working dataset.")

                else:
                    # Show an overview of missing values
                    missing_table = pd.DataFrame({
                        "Missing Values": columns_with_missing,
                        "Missing %": (
                            columns_with_missing / len(working) * 100
                        ).round(2)
                    })

                    st.markdown("#### Missing Values Overview")
                    st.dataframe(
                        missing_table,
                        use_container_width=True
                    )

                    st.divider()

                    # Select a specific column
                    st.markdown("#### Select Column to Clean")

                    selected_missing_col = st.selectbox(
                        "Choose a column containing missing values",
                        options=columns_with_missing.index.tolist(),
                        key="missing_column_select"
                    )

                    selected_series = working[selected_missing_col]
                    missing_count = int(selected_series.isna().sum())
                    missing_pct = missing_count / len(working) * 100

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Selected Column", selected_missing_col)
                    col2.metric("Missing Values", missing_count)
                    col3.metric("Missing Percentage", f"{missing_pct:.2f}%")

                    # Determine the selected column's data type
                    is_numeric = pd.api.types.is_numeric_dtype(selected_series)
                    is_datetime = pd.api.types.is_datetime64_any_dtype(
                        selected_series
                    )
                    is_categorical = (
                        isinstance(selected_series.dtype, pd.CategoricalDtype)
                        or pd.api.types.is_object_dtype(selected_series)
                        or pd.api.types.is_string_dtype(selected_series)
                        or pd.api.types.is_bool_dtype(selected_series)
                    )

                    if is_numeric:
                        data_type_label = "Numerical"
                        strategies = [
                            "Mean",
                            "Median",
                            "Mode",
                            "Custom Value"
                        ]

                    elif is_datetime:
                        data_type_label = "Datetime"
                        strategies = [
                            "Mode",
                            "Custom Value"
                        ]

                    elif is_categorical:
                        data_type_label = "Categorical"
                        strategies = [
                            "Mode",
                            "Custom Value"
                        ]

                    else:
                        data_type_label = "Other"
                        strategies = [
                            "Mode",
                            "Custom Value"
                        ]

                    st.caption(
                        f"Detected type: {data_type_label} "
                        f"({selected_series.dtype})"
                    )

                    # Choose an appropriate strategy
                    strategy = st.selectbox(
                        "Choose an imputation strategy",
                        options=strategies,
                        key="missing_strategy_select"
                    )

                    # Custom value input
                    if strategy == "Custom Value":
                        custom_value = st.text_input(
                            "Enter replacement value",
                            value="Unknown",
                            key="missing_custom_value_input",
                            help=(
                                "For numeric columns, enter a valid number. "
                                "For datetime columns, enter a valid date or timestamp."
                            )
                        )

                    st.caption(
                        "Only the selected column will be modified. "
                        "Other columns will remain unchanged."
                    )

                    # Apply treatment
                    if st.button(
                        "Apply to Selected Column",
                        key="apply_selected_missing",
                        type="primary"
                    ):

                        try:
                            working = st.session_state.working_df.copy()
                            series = working[selected_missing_col]

                            if strategy == "Mean":
                                fill_value = series.mean()
                                working[selected_missing_col] = series.fillna(
                                    fill_value
                                )

                            elif strategy == "Median":
                                fill_value = series.median()
                                working[selected_missing_col] = series.fillna(
                                    fill_value
                                )

                            elif strategy == "Mode":
                                modes = series.mode(dropna=True)

                                if modes.empty:
                                    st.error(
                                        "Cannot calculate the mode because "
                                        "the column has no non-missing values."
                                    )
                                    st.stop()

                                fill_value = modes.iloc[0]
                                working[selected_missing_col] = series.fillna(
                                    fill_value
                                )

                            elif strategy == "Custom Value":
                                if not custom_value.strip():
                                    st.error("Please enter a replacement value.")
                                    st.stop()

                                if is_numeric:
                                    # Validate and preserve numeric dtype
                                    fill_value = pd.to_numeric(
                                        custom_value,
                                        errors="raise"
                                    )

                                elif is_datetime:
                                    fill_value = pd.to_datetime(
                                        custom_value,
                                        errors="raise"
                                    )

                                else:
                                    fill_value = custom_value

                                working[selected_missing_col] = series.fillna(
                                    fill_value
                                )

                            remaining = int(
                                working[selected_missing_col].isna().sum()
                            )

                            st.session_state.working_df = working

                            st.success(
                                f"Applied {strategy.lower()} to "
                                f"'{selected_missing_col}'. "
                                f"{remaining} missing value(s) remain."
                            )

                        except Exception as e:
                            st.error(f"Could not fill missing values: {e}")

            with st.expander("📑  Duplicate Rows", expanded=False):

                duplicate_count = int(df.duplicated().sum())

                if duplicate_count == 0:
                    st.success("No duplicate rows found.")

                else:
                    st.warning(
                        f"{duplicate_count:,} duplicate rows detected."
                    )

                    st.dataframe(
                        df[df.duplicated(keep=False)].head(100),
                        use_container_width=True
                    )

                    keep_option = st.radio(
                        "Which occurrence should be kept?",
                        options=[
                            "Keep first occurrence",
                            "Keep last occurrence"
                        ],
                        horizontal=True,
                        key="duplicate_keep_option"
                    )

                    if st.button(
                        "Remove Duplicate Rows",
                        key="remove_duplicates",
                        type="primary"
                    ):
                        keep_value = (
                            "first"
                            if keep_option == "Keep first occurrence"
                            else "last"
                        )

                        before = len(df)

                        st.session_state.working_df = (
                            st.session_state.working_df
                            .drop_duplicates(keep=keep_value)
                            .copy()
                        )

                        removed = (
                            before - len(st.session_state.working_df)
                        )

                        st.success(f"Removed {removed:,} duplicate rows.")
                        st.rerun()

            with st.expander("🗂️  Column Management", expanded=False):

                if len(df.columns) > 0:

                    st.markdown("#### Rename a Column")

                    rename_col = st.selectbox(
                        "Column to rename",
                        options=list(df.columns),
                        key="rename_column_select"
                    )

                    new_name = st.text_input(
                        "New column name",
                        value=str(rename_col),
                        key="rename_column_name"
                    )

                    if st.button(
                        "Rename Column",
                        key="rename_column_button"
                    ):
                        new_name = new_name.strip()

                        if not new_name:
                            st.error("Column name cannot be empty.")

                        elif new_name != rename_col and new_name in df.columns:
                            st.error("A column with that name already exists.")

                        else:
                            st.session_state.working_df = (
                                st.session_state.working_df.rename(
                                    columns={rename_col: new_name}
                                )
                            )
                            st.success(
                                f"Column '{rename_col}' renamed to '{new_name}'."
                            )
                            st.rerun()

                    st.divider()
                    st.markdown("#### Drop Columns")

                    columns_to_drop = st.multiselect(
                        "Select columns to remove",
                        options=list(st.session_state.working_df.columns),
                        key="drop_columns_select"
                    )

                    if st.button(
                        "Drop Selected Columns",
                        key="drop_columns_button"
                    ):
                        if not columns_to_drop:
                            st.warning("Select at least one column.")

                        elif len(columns_to_drop) == len(df.columns):
                            st.error(
                                "You cannot remove every column. "
                                "Keep at least one column in the dataset."
                            )

                        else:
                            st.session_state.working_df = (
                                st.session_state.working_df
                                .drop(columns=columns_to_drop)
                                .copy()
                            )
                            st.success(
                                f"Removed {len(columns_to_drop)} column(s)."
                            )
                            st.rerun()

                else:
                    st.info("No columns are available to manage.")


            with st.expander("📈  Outlier Handling", expanded=False):

                numeric_cols = list(
                    df.select_dtypes(include="number").columns
                )

                if numeric_cols:

                    st.caption(
                        "Uses the Interquartile Range (IQR) method. "
                        "Outliers are flagged below Q1 − 1.5 × IQR or "
                        "above Q3 + 1.5 × IQR."
                    )

                    outlier_col = st.selectbox(
                        "Select numeric column",
                        options=numeric_cols,
                        key="outlier_column"
                    )

                    series = df[outlier_col].dropna()

                    if len(series) >= 2:
                        q1 = series.quantile(0.25)
                        q3 = series.quantile(0.75)
                        iqr = q3 - q1

                        lower_bound = q1 - 1.5 * iqr
                        upper_bound = q3 + 1.5 * iqr

                        outlier_mask = (
                            (df[outlier_col] < lower_bound)
                            | (df[outlier_col] > upper_bound)
                        ).fillna(False)

                        outlier_count = int(outlier_mask.sum())

                        o1, o2, o3 = st.columns(3)
                        o1.metric("Outliers Detected", outlier_count)
                        o2.metric("Lower Bound", f"{lower_bound:.3f}")
                        o3.metric("Upper Bound", f"{upper_bound:.3f}")

                        st.write("**How would you like to handle them?**")

                        outlier_action = st.radio(
                            "Outlier treatment",
                            [
                                "Cap at IQR bounds",
                                "Remove rows containing outliers"
                            ],
                            key="outlier_action",
                            horizontal=True
                        )

                        if st.button(
                            "Apply Outlier Treatment",
                            key="apply_outliers",
                            type="primary"
                        ):
                            if outlier_count == 0:
                                st.info("No outliers to treat in this column.")

                            elif outlier_action == "Cap at IQR bounds":
                                st.session_state.working_df.loc[
                                    :, outlier_col
                                ] = df[outlier_col].clip(
                                    lower=lower_bound,
                                    upper=upper_bound
                                )

                                st.success(
                                    f"Capped {outlier_count} values in "
                                    f"'{outlier_col}' at the IQR bounds."
                                )
                                st.rerun()

                            else:
                                st.session_state.working_df = (
                                    df.loc[~outlier_mask].copy()
                                )

                                st.success(
                                    f"Removed {outlier_count} row(s) "
                                    f"containing outliers in '{outlier_col}'."
                                )
                                st.rerun()

                    else:
                        st.info(
                            "At least two non-missing numeric values are "
                            "needed to inspect outliers."
                        )

                else:
                    st.info("No numeric columns are available for outlier analysis.")

            st.divider()
            st.markdown("### Current Working Dataset")
            st.caption(
                "Preview of the dataset after the cleaning operations "
                "you have applied."
            )

            st.dataframe(
                st.session_state.working_df.head(100),
                use_container_width=True,
                height=350
            )

            st.caption(
                f"Showing up to 100 rows of "
                f"{len(st.session_state.working_df):,} total rows."
            )




    with visualization:
        df = st.session_state.working_df
        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / VISUALIZATION</div>
            <h1 class="explore-heading">Visualize Your Data</h1>
            <p class="explore-subtitle">
                Explore individual columns, compare two variables, and create charts
                from your current working dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if df.empty or len(df.columns) == 0:
            st.warning("Your working dataset is empty. Upload a dataset first.")
        else:
            numeric_cols = list(df.select_dtypes(include="number").columns)
            datetime_cols = list(df.select_dtypes(include=["datetime", "datetimetz"]).columns)

            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Rows", f"{len(df):,}")
            metric2.metric("Columns", f"{len(df.columns):,}")
            metric3.metric("Numeric columns", len(numeric_cols))

            sns.set_theme(
                style="darkgrid",
                rc={
                    "figure.facecolor": "#0B1120",
                    "axes.facecolor": "#111C30",
                    "axes.edgecolor": "#263750",
                    "axes.labelcolor": "#F8FAFC",
                    "text.color": "#F8FAFC",
                    "xtick.color": "#CBD5E1",
                    "ytick.color": "#CBD5E1",
                    "grid.color": "#263750",
                    "grid.alpha": 0.4,
                },
            )

            def style_chart(fig, ax, title, xlabel=None, ylabel=None):
                ax.set_title(title, color="#F8FAFC", fontsize=14, fontweight="bold", pad=12)
                if xlabel is not None:
                    ax.set_xlabel(xlabel, color="#CBD5E1")
                if ylabel is not None:
                    ax.set_ylabel(ylabel, color="#CBD5E1")
                ax.tick_params(colors="#CBD5E1")
                for spine in ax.spines.values():
                    spine.set_color("#263750")
                fig.tight_layout()

            st.markdown("### Chart Configuration")
            analysis_type = st.selectbox(
                "Choose analysis type",
                ["Univariate", "Bivariate"],
                key="datalens_analysis_type",
            )

            fig = None

            # ------------------------------------------
            # UNIVARIATE: one column at a time
            # ------------------------------------------
            if analysis_type == "Univariate":
                col1, col2 = st.columns(2)
                selected_col = col1.selectbox(
                    "Select column",
                    options=list(df.columns),
                    key="datalens_univariate_column",
                )
                series = df[selected_col]
                is_numeric = pd.api.types.is_numeric_dtype(series)
                is_datetime = pd.api.types.is_datetime64_any_dtype(series)

                if is_numeric:
                    chart_options = ["KDE Plot", "Histogram", "Box Plot"]
                elif is_datetime:
                    chart_options = ["Records Over Time", "Date Frequency"]
                else:
                    chart_options = ["Count Plot", "Pie Plot"]

                chart_type = col2.selectbox(
                    "Select chart type",
                    chart_options,
                    key="datalens_univariate_chart",
                )
                color = st.color_picker("Chart color", "#22D3EE", key="datalens_uni_color")
                valid = series.dropna()

                if valid.empty:
                    st.warning("This column contains no non-missing values to plot.")
                else:
                    fig, ax = plt.subplots(figsize=(12, 6))

                    if is_numeric:
                        if chart_type == "KDE Plot":
                            if valid.nunique() < 2:
                                st.info("A KDE plot needs at least two distinct numeric values. Showing a histogram instead.")
                                sns.histplot(x=valid, ax=ax, color=color, kde=False)
                            else:
                                sns.kdeplot(x=valid, ax=ax, color=color, fill=True)
                        elif chart_type == "Histogram":
                            sns.histplot(x=valid, ax=ax, color=color, bins="auto")
                        else:  # Box Plot
                            sns.boxplot(x=valid, ax=ax, color=color)
                        style_chart(fig, ax, f"{chart_type} — {selected_col}", xlabel=selected_col)

                    elif is_datetime:
                        dates = pd.to_datetime(valid, errors="coerce").dropna()
                        if dates.empty:
                            plt.close(fig)
                            fig = None
                            st.warning("No valid dates were found in this column.")
                        elif chart_type == "Records Over Time":
                            counts = dates.value_counts().sort_index()
                            ax.plot(counts.index, counts.values, color=color, marker="o", linewidth=2)
                            fig.autofmt_xdate()
                            style_chart(fig, ax, f"Records Over Time — {selected_col}", "Date", "Record count")
                        else:
                            frequency = st.selectbox(
                                "Group dates by", ["Day", "Month", "Year"], key="datalens_date_frequency"
                            )
                            date_series = pd.Series(dates)
                            if frequency == "Day":
                                counts = date_series.dt.floor("D").value_counts().sort_index()
                            elif frequency == "Month":
                                counts = date_series.dt.to_period("M").value_counts().sort_index()
                                counts.index = counts.index.astype(str)
                            else:
                                counts = date_series.dt.to_period("Y").value_counts().sort_index()
                                counts.index = counts.index.astype(str)
                            ax.bar(counts.index.astype(str), counts.values, color=color)
                            ax.tick_params(axis="x", labelrotation=45)
                            style_chart(fig, ax, f"Record Frequency by {frequency}", frequency, "Record count")

                    else:
                        counts = valid.astype("string").value_counts().head(20)
                        if chart_type == "Count Plot":
                            sns.barplot(x=counts.index.astype(str), y=counts.values, ax=ax, color=color)
                            ax.tick_params(axis="x", labelrotation=45)
                            style_chart(fig, ax, f"Count Plot — {selected_col}", selected_col, "Count")
                        else:  # Pie Plot
                            plt.close(fig)
                            fig, ax = plt.subplots(figsize=(9, 6))
                            ax.pie(
                                counts.values,
                                labels=counts.index.astype(str),
                                autopct="%.1f%%",
                                startangle=90,
                                textprops={"color": "#F8FAFC"},
                            )
                            ax.set_title(f"Pie Plot — {selected_col}", color="#F8FAFC", fontweight="bold")
                            fig.patch.set_facecolor("#0B1120")
                            fig.tight_layout()
                            if valid.nunique() > 20:
                                st.caption("The pie chart displays the 20 most frequent categories.")

            # ------------------------------------------
            # BIVARIATE: compare two columns
            # ------------------------------------------
            else:
                c1, c2, c3 = st.columns(3)
                x_col = c1.selectbox("Select X-axis column", list(df.columns), key="datalens_bivariate_x")
                y_col = c2.selectbox(
                    "Select Y-axis column",
                    list(df.columns),
                    index=min(1, len(df.columns) - 1),
                    key="datalens_bivariate_y",
                )

                if x_col == y_col:
                    st.info("Choose two different columns to compare them.")
                else:
                    x_num = pd.api.types.is_numeric_dtype(df[x_col])
                    y_num = pd.api.types.is_numeric_dtype(df[y_col])
                    x_date = pd.api.types.is_datetime64_any_dtype(df[x_col])
                    y_date = pd.api.types.is_datetime64_any_dtype(df[y_col])

                    # Date + numeric should be checked before general category + numeric.
                    if (x_date and y_num) or (x_num and y_date):
                        date_col, value_col = (x_col, y_col) if x_date else (y_col, x_col)
                        chart_type = c3.selectbox(
                            "Select chart type", ["Line Plot", "Scatter Plot"], key="datalens_date_numeric_chart"
                        )
                        plot_data = df[[date_col, value_col]].copy()
                        plot_data[date_col] = pd.to_datetime(plot_data[date_col], errors="coerce")
                        plot_data = plot_data.dropna()
                        if plot_data.empty:
                            st.warning("No complete date and numeric values are available.")
                        else:
                            fig, ax = plt.subplots(figsize=(12, 6))
                            if chart_type == "Line Plot":
                                grouped = plot_data.groupby(date_col, as_index=False)[value_col].mean().sort_values(date_col)
                                sns.lineplot(data=grouped, x=date_col, y=value_col, ax=ax, color="#22D3EE")
                            else:
                                sns.scatterplot(data=plot_data, x=date_col, y=value_col, ax=ax, color="#22D3EE")
                            fig.autofmt_xdate()
                            style_chart(fig, ax, f"{value_col} over time", date_col, value_col)

                    elif x_num and y_num:
                        chart_type = c3.selectbox(
                            "Select chart type", ["Scatter Plot", "2D Histogram Plot"], key="datalens_numeric_numeric_chart"
                        )
                        plot_data = df[[x_col, y_col]].dropna()
                        if plot_data.empty:
                            st.warning("No complete rows are available for these columns.")
                        else:
                            fig, ax = plt.subplots(figsize=(12, 6))
                            if chart_type == "Scatter Plot":
                                sns.scatterplot(data=plot_data, x=x_col, y=y_col, ax=ax, color="#22D3EE", alpha=0.75)
                            else:
                                sns.histplot(data=plot_data, x=x_col, y=y_col, bins=30, cmap="mako", ax=ax)
                            style_chart(fig, ax, f"{chart_type}: {x_col} vs {y_col}", x_col, y_col)

                    elif (not x_num and y_num) or (x_num and not y_num):
                        category_col, numeric_col = (y_col, x_col) if x_num else (x_col, y_col)
                        chart_type = c3.selectbox(
                            "Select chart type", ["Bar Plot", "Box Plot"], key="datalens_category_numeric_chart"
                        )
                        plot_data = df[[category_col, numeric_col]].dropna().copy()
                        top_categories = plot_data[category_col].value_counts().head(20).index
                        plot_data = plot_data[plot_data[category_col].isin(top_categories)]

                        if plot_data.empty:
                            st.warning("No complete rows are available for these columns.")
                        else:
                            fig, ax = plt.subplots(figsize=(12, 6))
                            if chart_type == "Bar Plot":
                                aggregation = st.selectbox(
                                    "Select aggregation", ["mean", "median", "sum", "count"], key="datalens_bar_aggregation"
                                )
                                grouped = plot_data.groupby(category_col, observed=True)[numeric_col]
                                if aggregation == "mean":
                                    values = grouped.mean()
                                elif aggregation == "median":
                                    values = grouped.median()
                                elif aggregation == "sum":
                                    values = grouped.sum()
                                else:
                                    values = grouped.count()
                                values = values.sort_values(ascending=False)
                                sns.barplot(x=values.index.astype(str), y=values.values, ax=ax, color="#22D3EE")
                                ax.tick_params(axis="x", labelrotation=45)
                                style_chart(fig, ax, f"{aggregation.title()} of {numeric_col} by {category_col}", category_col, aggregation.title())
                            else:
                                sns.boxplot(data=plot_data, x=category_col, y=numeric_col, ax=ax, color="#22D3EE")
                                ax.tick_params(axis="x", labelrotation=45)
                                style_chart(fig, ax, f"{numeric_col} by {category_col}", category_col, numeric_col)
                            if df[category_col].nunique() > 20:
                                st.caption("Only the 20 most frequent categories are shown.")

                    elif not x_num and not y_num and not x_date and not y_date:
                        chart_type = c3.selectbox(
                            "Select chart type", ["Heatmap", "Grouped Count Plot"], key="datalens_category_category_chart"
                        )
                        plot_data = df[[x_col, y_col]].dropna()
                        if plot_data.empty:
                            st.warning("No complete rows are available for these columns.")
                        else:
                            top_x = plot_data[x_col].value_counts().head(15).index
                            top_y = plot_data[y_col].value_counts().head(15).index
                            plot_data = plot_data[plot_data[x_col].isin(top_x) & plot_data[y_col].isin(top_y)]
                            fig, ax = plt.subplots(figsize=(12, 6))
                            if chart_type == "Heatmap":
                                table = pd.crosstab(plot_data[x_col], plot_data[y_col])
                                sns.heatmap(table, annot=True, fmt="d", cmap="mako", ax=ax)
                                style_chart(fig, ax, f"Heatmap: {x_col} vs {y_col}", y_col, x_col)
                            else:
                                sns.countplot(data=plot_data, x=x_col, hue=y_col, ax=ax)
                                ax.tick_params(axis="x", labelrotation=45)
                                ax.legend(title=y_col, facecolor="#111C30", labelcolor="#F8FAFC")
                                style_chart(fig, ax, f"Grouped Counts: {x_col} by {y_col}", x_col, "Count")

                    else:
                        st.info("This column combination is not supported. Try numeric/numeric, category/numeric, category/category, or date/numeric.")

            # Display and download the chart, if one was created.
            if fig is not None:
                st.markdown("### Chart Preview")
                st.pyplot(fig, use_container_width=True)
                image_buffer = io.BytesIO()
                fig.savefig(image_buffer, format="png", dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
                image_buffer.seek(0)
                st.download_button(
                    "⬇️ Download Chart as PNG",
                    data=image_buffer,
                    file_name="datalens_chart.png",
                    mime="image/png",
                    key="datalens_download_chart",
                )
                plt.close(fig)




    with compare_changes:

        # Get original and current working datasets
        original = original_df.copy()
        current = st.session_state.get("working_df", original_df).copy()

        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / Compare Changes</div>
            <h1 class="explore-heading">Track Your Data Transformations</h1>
            <p class="explore-subtitle">
                Compare your original dataset with the cleaned version.
            </p>
        </div>
        """, unsafe_allow_html=True)
        


        st.write("")

        # --------------------------------------------------
        # 1. Dataset comparison metrics
        # --------------------------------------------------
        original_rows, original_cols = original.shape
        current_rows, current_cols = current.shape

        original_missing = int(original.isna().sum().sum())
        current_missing = int(current.isna().sum().sum())

        original_duplicates = int(original.duplicated().sum())
        current_duplicates = int(current.duplicated().sum())

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Original Rows",
                f"{original_rows:,}",
                help="Number of rows in the uploaded dataset."
            )

        with c2:
            st.metric(
                "Current Rows",
                f"{current_rows:,}",
                delta=f"{current_rows - original_rows:+,}"
            )

        with c3:
            st.metric(
                "Original Missing Values",
                f"{original_missing:,}"
            )

        with c4:
            st.metric(
                "Current Missing Values",
                f"{current_missing:,}",
                delta=f"{current_missing - original_missing:+,}",
                delta_color="inverse"
            )

        st.write("")

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            st.metric("Original Columns", original_cols)

        with c6:
            st.metric(
                "Current Columns",
                current_cols,
                delta=f"{current_cols - original_cols:+,}"
            )

        with c7:
            st.metric("Original Duplicates", f"{original_duplicates:,}")

        with c8:
            st.metric("Current Duplicates", f"{current_duplicates:,}")

        st.divider()

        # --------------------------------------------------
        # 2. Added and removed columns
        # --------------------------------------------------
        st.subheader("Column Changes")

        original_columns = set(original.columns)
        current_columns = set(current.columns)

        added_columns = [
            col for col in current.columns
            if col not in original_columns
        ]

        removed_columns = [
            col for col in original.columns
            if col not in current_columns
        ]

        common_columns = [
            col for col in current.columns
            if col in original_columns
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Added Columns**")

            if added_columns:
                st.success(f"{len(added_columns)} column(s) added")
                st.write(added_columns)
            else:
                st.caption("No columns added.")

        with col2:
            st.markdown("**Removed Columns**")

            if removed_columns:
                st.warning(f"{len(removed_columns)} column(s) removed")
                st.write(removed_columns)
            else:
                st.caption("No columns removed.")

        # --------------------------------------------------
        # 3. Datatype comparison
        # --------------------------------------------------
        st.divider()
        st.subheader("Datatype Changes")

        dtype_changes = []

        for col in common_columns:
            old_dtype = str(original[col].dtype)
            new_dtype = str(current[col].dtype)

            if old_dtype != new_dtype:
                dtype_changes.append({
                    "Column": col,
                    "Original Datatype": old_dtype,
                    "Current Datatype": new_dtype
                })

        if dtype_changes:
            st.dataframe(
                pd.DataFrame(dtype_changes),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No datatype changes detected.")

        # --------------------------------------------------
        # 4. Missing-value comparison by column
        # --------------------------------------------------
        st.divider()
        st.subheader("Missing Values Comparison")

        missing_comparison = pd.DataFrame({
            "Column": common_columns,
            "Original Missing": [
                int(original[col].isna().sum())
                for col in common_columns
            ],
            "Current Missing": [
                int(current[col].isna().sum())
                for col in common_columns
            ]
        })

        if not missing_comparison.empty:
            missing_comparison["Difference"] = (
                missing_comparison["Current Missing"]
                - missing_comparison["Original Missing"]
            )

            changed_missing = missing_comparison[
                missing_comparison["Difference"] != 0
            ]

            if not changed_missing.empty:
                st.dataframe(
                    changed_missing,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Missing-value counts have not changed.")

        # --------------------------------------------------
        # 5. Modified cell values
        # --------------------------------------------------
        st.divider()
        st.subheader("Modified Cell Values")

        # Compare only rows whose index labels and columns exist
        # in both datasets.
        common_indexes = original.index.intersection(current.index)

        if common_indexes.empty or not common_columns:
            st.info(
                "No matching rows and columns are available "
                "for a cell-by-cell comparison."
            )
        else:
            old_values = original.loc[
                common_indexes, common_columns
            ]
            new_values = current.loc[
                common_indexes, common_columns
            ]

            try:
                differences = old_values.compare(
                    new_values,
                    result_names=("Original", "Current")
                )

                if differences.empty:
                    st.info(
                        "No modified cell values detected "
                        "for matching rows and columns."
                    )
                else:
                    st.caption(
                        f"{len(differences):,} row(s) contain "
                        "at least one changed value."
                    )

                    st.dataframe(
                        differences,
                        use_container_width=True
                    )

                    # Download the comparison report
                    comparison_csv = differences.to_csv().encode("utf-8")

                    st.download_button(
                        label="Download Changes Report (CSV)",
                        data=comparison_csv,
                        file_name="datalens_changes_report.csv",
                        mime="text/csv"
                    )

            except (TypeError, ValueError) as error:
                st.warning(
                    "A cell-by-cell comparison could not be "
                    f"completed: {error}"
                )


    with export:
        df = st.session_state.get("working_df", original_df).copy()
        st.markdown("""
        <style>
        .explore-hero {
            background: linear-gradient(135deg, #111C30, #172554);
            border: 1px solid #263750;
            border-radius: 16px;
            padding: 26px 28px;
            margin-bottom: 22px;
        }

        .explore-eyebrow {
            color: #22D3EE;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .explore-heading {
            color: #F8FAFC !important;
            font-size: 28px !important;
            font-weight: 750 !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        .explore-subtitle {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explore-hero">
            <div class="explore-eyebrow">DATALENS / EXPORT</div>
            <h1 class="explore-heading">Export Your Dataset</h1>
            <p class="explore-subtitle">
                Download your cleaned dataset in your preferred format.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # --------------------------------------------------
        # 1. Export summary
        # --------------------------------------------------
        st.subheader("Dataset Ready for Export")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Rows", f"{df.shape[0]:,}")

        with c2:
            st.metric("Columns", f"{df.shape[1]:,}")

        with c3:
            st.metric(
                "Missing Values",
                f"{int(df.isna().sum().sum()):,}"
            )

        st.divider()

        # --------------------------------------------------
        # 2. Export settings
        # --------------------------------------------------
        st.subheader("Export Settings")

        col1, col2 = st.columns(2)

        with col1:
            export_format = st.selectbox(
                "Select file format",
                ["CSV", "Excel (.xlsx)", "JSON"],
                key="export_format"
            )

        with col2:
            file_name = st.text_input(
                "File name",
                value="datalens_cleaned_data",
                key="export_file_name"
            )

        # Remove a file extension if the user enters one.
        base_name = file_name.strip()

        for extension in [".csv", ".xlsx", ".json"]:
            if base_name.lower().endswith(extension):
                base_name = base_name[:-len(extension)]

        if not base_name:
            base_name = "datalens_cleaned_data"

        st.write("")

        # --------------------------------------------------
        # 3. Generate download file
        # --------------------------------------------------
        if export_format == "CSV":

            file_data = df.to_csv(index=False).encode("utf-8-sig")
            download_name = f"{base_name}.csv"
            mime_type = "text/csv"

        elif export_format == "Excel (.xlsx)":

            buffer = io.BytesIO()

            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )

            file_data = buffer.getvalue()
            download_name = f"{base_name}.xlsx"
            mime_type = (
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )

        else:  # JSON

            file_data = df.to_json(
                orient="records",
                indent=2,
                force_ascii=False,
                date_format="iso"
            ).encode("utf-8")

            download_name = f"{base_name}.json"
            mime_type = "application/json"

        st.download_button(
            label=f"Download {export_format} File",
            data=file_data,
            file_name=download_name,
            mime=mime_type,
            use_container_width=True
        )

        st.divider()

        st.subheader("Preview Before Export")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing up to 10 of {len(df):,} rows. "
            "The downloaded file contains the full current dataset."
        )

