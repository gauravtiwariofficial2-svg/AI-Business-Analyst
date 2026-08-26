import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title("📊 AI Business Analyst")

st.write(
    "Upload your business data and get instant analytics, "
    "visualizations, and business insights."
)

st.divider()

# File uploader
st.subheader("📁 Upload Your Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

# Process uploaded file
df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.success("File uploaded successfully!")

    except Exception:
        st.error(
            "Unable to read this file. "
            "Please upload a valid CSV or Excel file."
        )
        st.stop()

if df is None:
    st.info("Please upload a CSV or Excel file to begin the analysis.")
    st.stop()

# Dataset overview
st.subheader("📊 Dataset Overview")

rows, columns = df.shape

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", rows)

with col2:
    st.metric("Columns", columns)

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

with col4:
    st.metric("Duplicate Rows", int(df.duplicated().sum()))

# Data preview
st.subheader("📋 Data Preview")

st.dataframe(df.head(10), use_container_width=True)

# -----------------------------------------
# STEP 6: DATA QUALITY ANALYSIS
# -----------------------------------------

st.divider()

st.header("🔎 Data Quality Analysis")

# Calculate missing values for every column
missing_values = df.isnull().sum()

# Calculate missing percentage
missing_percentage = (missing_values / len(df)) * 100

# Create a data quality table
quality_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": missing_values.values,
    "Missing %": missing_percentage.values,
    "Data Type": df.dtypes.astype(str).values
})

# Show only columns that contain missing values
missing_df = quality_df[quality_df["Missing Values"] > 0]

st.subheader("⚠️ Missing Value Analysis")

if len(missing_df) > 0:
    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ No missing values found in the dataset.")

# Duplicate analysis
duplicate_count = df.duplicated().sum()

st.subheader("🔁 Duplicate Rows")

if duplicate_count > 0:
    st.warning(
        f"⚠️ {duplicate_count} duplicate rows were found."
    )
else:
    st.success("✅ No duplicate rows found.")

# Data type analysis
st.subheader("🧩 Column Data Types")

st.dataframe(
    quality_df[["Column", "Data Type"]],
    use_container_width=True,
    hide_index=True
)

# Numerical summary
st.subheader("📊 Numerical Summary")

numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:
    st.dataframe(
        numeric_df.describe().T,
        use_container_width=True
    )
else:
    st.info("No numerical columns found.")

# -----------------------------------------
# STEP 7: AUTOMATIC BUSINESS KPI ANALYSIS
# -----------------------------------------

st.divider()

st.header("📊 Business KPI Analysis")


# -----------------------------------------
# Function to find business columns
# -----------------------------------------

def find_column(possible_names):
    for column in df.columns:
        column_clean = str(column).strip().lower()

        for name in possible_names:
            if name in column_clean:
                return column

    return None


# -----------------------------------------
# Detect important business columns
# -----------------------------------------

sales_col = find_column([
    "sales",
    "revenue",
    "amount",
    "total price",
    "total sales"
])

profit_col = find_column([
    "profit",
    "net profit",
    "earnings"
])

quantity_col = find_column([
    "quantity",
    "qty",
    "units"
])

discount_col = find_column([
    "discount"
])

order_col = find_column([
    "order id",
    "orderid",
    "order"
])


# -----------------------------------------
# Main KPI cards
# -----------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


# Total Sales
with kpi1:

    if sales_col:

        total_sales = pd.to_numeric(
            df[sales_col],
            errors="coerce"
        ).sum()

        st.metric(
            "💰 Total Sales",
            f"{total_sales:,.2f}"
        )

    else:

        st.metric(
            "💰 Total Sales",
            "Not found"
        )


# Total Profit
with kpi2:

    if profit_col:

        total_profit = pd.to_numeric(
            df[profit_col],
            errors="coerce"
        ).sum()

        st.metric(
            "📈 Total Profit",
            f"{total_profit:,.2f}"
        )

    else:

        st.metric(
            "📈 Total Profit",
            "Not found"
        )


# Total Quantity
with kpi3:

    if quantity_col:

        total_quantity = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).sum()

        st.metric(
            "📦 Total Quantity",
            f"{total_quantity:,.0f}"
        )

    else:

        st.metric(
            "📦 Total Quantity",
            "Not found"
        )


# Total Orders
with kpi4:

    if order_col:

        total_orders = df[order_col].nunique()

        st.metric(
            "🧾 Total Orders",
            f"{total_orders:,}"
        )

    else:

        st.metric(
            "🧾 Total Orders",
            f"{len(df):,}"
        )


# -----------------------------------------
# Additional Business Metrics
# -----------------------------------------

st.subheader("📌 Additional Business Metrics")

metric1, metric2, metric3 = st.columns(3)


# Average Order Value
with metric1:

    if sales_col and order_col:

        sales_values = pd.to_numeric(
            df[sales_col],
            errors="coerce"
        )

        order_count = df[order_col].nunique()

        if order_count > 0:

            average_order_value = (
                sales_values.sum() / order_count
            )

            st.metric(
                "🛒 Average Order Value",
                f"{average_order_value:,.2f}"
            )

        else:

            st.metric(
                "🛒 Average Order Value",
                "N/A"
            )

    else:

        st.metric(
            "🛒 Average Order Value",
            "N/A"
        )


# Average Profit
with metric2:

    if profit_col:

        profit_values = pd.to_numeric(
            df[profit_col],
            errors="coerce"
        )

        average_profit = profit_values.mean()

        st.metric(
            "📈 Average Profit",
            f"{average_profit:,.2f}"
        )

    else:

        st.metric(
            "📈 Average Profit",
            "N/A"
        )


# Average Discount
with metric3:

    if discount_col:

        discount_values = pd.to_numeric(
            df[discount_col],
            errors="coerce"
        )

        average_discount = discount_values.mean()

        st.metric(
            "🏷️ Average Discount",
            f"{average_discount:.2f}"
        )

    else:

        st.metric(
            "🏷️ Average Discount",
            "N/A"
        )


# -----------------------------------------
# Detected Business Columns
# -----------------------------------------

st.subheader("🔍 Detected Business Columns")


detected_columns = {
    "Sales / Revenue": sales_col,
    "Profit": profit_col,
    "Quantity": quantity_col,
    "Discount": discount_col,
    "Order ID": order_col
}


detected_df = pd.DataFrame(
    list(detected_columns.items()),
    columns=[
        "Business Metric",
        "Detected Column"
    ]
)


st.dataframe(
    detected_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------------------
# STEP 8: AUTOMATIC VISUAL ANALYSIS
# -----------------------------------------

st.divider()

st.header("📈 Automatic Visual Analysis")


# -----------------------------------------
# Identify categorical and numerical columns
# -----------------------------------------

categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()


numerical_columns = df.select_dtypes(
    include="number"
).columns.tolist()


# -----------------------------------------
# SALES ANALYSIS
# -----------------------------------------

if sales_col:

    st.subheader("💰 Sales Analysis")


    # -------------------------------------
    # Sales by Category
    # -------------------------------------

    category_col = find_column([
        "category",
        "product category",
        "product type"
    ])


    if category_col:

        category_sales = (
            df.groupby(category_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
        )

        st.write("### 📊 Sales by Category")

        st.bar_chart(category_sales)


    # -------------------------------------
    # Sales by Region
    # -------------------------------------

    region_col = find_column([
        "region",
        "area",
        "territory",
        "location"
    ])


    if region_col:

        region_sales = (
            df.groupby(region_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
        )

        st.write("### 🌍 Sales by Region")

        st.bar_chart(region_sales)


# -----------------------------------------
# AUTOMATIC DATE DETECTION
# -----------------------------------------

date_column = None


for column in df.columns:

    try:

        converted_dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        valid_dates = converted_dates.notna().sum()

        if valid_dates > len(df) * 0.5:

            date_column = column
            break

    except Exception:

        continue


# -----------------------------------------
# SALES TREND
# -----------------------------------------

if date_column and sales_col:

    st.subheader("📅 Sales Trend")


    trend_df = df.copy()


    trend_df[date_column] = pd.to_datetime(
        trend_df[date_column],
        errors="coerce"
    )


    trend_df[sales_col] = pd.to_numeric(
        trend_df[sales_col],
        errors="coerce"
    )


    trend_df = trend_df.dropna(
        subset=[
            date_column,
            sales_col
        ]
    )


    monthly_sales = (
        trend_df
        .set_index(date_column)[sales_col]
        .resample("ME")
        .sum()
    )


    if len(monthly_sales) > 1:

        st.write("### 📈 Monthly Sales Trend")

        st.line_chart(monthly_sales)


# -----------------------------------------
# NUMERICAL DATA DISTRIBUTION
# -----------------------------------------

if numerical_columns:

    st.subheader("📊 Numerical Data Distribution")


    selected_numeric = st.selectbox(
        "Select a numerical column",
        numerical_columns,
        key="numeric_distribution"
    )


    numeric_counts = (
        df[selected_numeric]
        .value_counts()
        .sort_index()
    )


    st.bar_chart(numeric_counts)


# -----------------------------------------
# CATEGORICAL DATA DISTRIBUTION
# -----------------------------------------

if categorical_columns:

    st.subheader("📋 Category Distribution")


    selected_category = st.selectbox(
        "Select a categorical column",
        categorical_columns,
        key="category_distribution"
    )


    category_counts = (
        df[selected_category]
        .value_counts()
        .head(15)
    )


    st.bar_chart(category_counts)

# -----------------------------------------
# STEP 9: AUTOMATIC BUSINESS INSIGHTS
# -----------------------------------------

st.divider()

st.header("🧠 Automatic Business Insights")

st.write(
    "The system automatically analyzes the dataset "
    "and generates business-oriented observations."
)


insights = []


# -----------------------------------------
# 1. SALES INSIGHTS
# -----------------------------------------

if sales_col:

    sales_values = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    )

    total_sales = sales_values.sum()

    average_sales = sales_values.mean()

    insights.append(
        f"💰 Total sales generated from the dataset are "
        f"{total_sales:,.2f}."
    )

    insights.append(
        f"📊 Average sales value per record is "
        f"{average_sales:,.2f}."
    )


# -----------------------------------------
# 2. REGION INSIGHTS
# -----------------------------------------

region_col = find_column([
    "region",
    "area",
    "territory",
    "location"
])


if region_col and sales_col:

    region_analysis = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(region_analysis) > 0:

        best_region = region_analysis.idxmax()

        best_region_sales = region_analysis.max()

        worst_region = region_analysis.idxmin()

        worst_region_sales = region_analysis.min()

        insights.append(
            f"🌍 {best_region} is the highest-performing "
            f"region with sales of {best_region_sales:,.2f}."
        )

        insights.append(
            f"⚠️ {worst_region} has the lowest regional sales "
            f"at {worst_region_sales:,.2f}."
        )


# -----------------------------------------
# 3. CATEGORY INSIGHTS
# -----------------------------------------

category_col = find_column([
    "category",
    "product category",
    "product type"
])


if category_col and sales_col:

    category_analysis = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(category_analysis) > 0:

        best_category = category_analysis.idxmax()

        best_category_sales = category_analysis.max()

        worst_category = category_analysis.idxmin()

        worst_category_sales = category_analysis.min()

        insights.append(
            f"🏆 {best_category} is the top-performing "
            f"category with sales of {best_category_sales:,.2f}."
        )

        insights.append(
            f"📉 {worst_category} has the lowest category "
            f"sales at {worst_category_sales:,.2f}."
        )


# -----------------------------------------
# 4. PROFIT INSIGHTS
# -----------------------------------------

if profit_col:

    profit_values = pd.to_numeric(
        df[profit_col],
        errors="coerce"
    )

    total_profit = profit_values.sum()

    average_profit = profit_values.mean()

    insights.append(
        f"📈 Total profit generated is "
        f"{total_profit:,.2f}."
    )

    insights.append(
        f"💵 Average profit per record is "
        f"{average_profit:,.2f}."
    )

    if total_profit > 0:

        insights.append(
            "✅ Overall profitability is positive."
        )

    elif total_profit < 0:

        insights.append(
            "⚠️ Overall profitability is negative "
            "and requires attention."
        )


# -----------------------------------------
# 5. DISCOUNT INSIGHTS
# -----------------------------------------

if discount_col:

    discount_values = pd.to_numeric(
        df[discount_col],
        errors="coerce"
    )

    average_discount = discount_values.mean()

    maximum_discount = discount_values.max()

    insights.append(
        f"🏷️ Average discount is "
        f"{average_discount:.2f}."
    )

    insights.append(
        f"🔖 Maximum recorded discount is "
        f"{maximum_discount:.2f}."
    )


# -----------------------------------------
# 6. QUANTITY INSIGHTS
# -----------------------------------------

if quantity_col:

    quantity_values = pd.to_numeric(
        df[quantity_col],
        errors="coerce"
    )

    total_quantity = quantity_values.sum()

    average_quantity = quantity_values.mean()

    insights.append(
        f"📦 Total quantity sold is "
        f"{total_quantity:,.0f}."
    )

    insights.append(
        f"🛒 Average quantity per record is "
        f"{average_quantity:.2f}."
    )


# -----------------------------------------
# 7. PRODUCT INSIGHTS
# -----------------------------------------

product_col = find_column([
    "product name",
    "product",
    "item"
])


if product_col and sales_col:

    product_analysis = (
        df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(product_analysis) > 0:

        best_product = product_analysis.idxmax()

        best_product_sales = product_analysis.max()

        insights.append(
            f"⭐ {best_product} is the highest-selling "
            f"product with sales of "
            f"{best_product_sales:,.2f}."
        )


# -----------------------------------------
# 8. DISPLAY INSIGHTS
# -----------------------------------------

if insights:

    st.subheader("📌 Key Business Findings")

    for insight in insights:

        st.info(insight)

else:

    st.warning(
        "Not enough business-related columns "
        "were detected to generate insights."
    )


# -----------------------------------------
# 9. BUSINESS RECOMMENDATIONS
# -----------------------------------------

st.subheader("💡 Business Recommendations")


recommendations = []


if region_col and sales_col:

    region_analysis = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(region_analysis) > 1:

        best_region = region_analysis.idxmax()

        worst_region = region_analysis.idxmin()

        recommendations.append(
            f"Focus on expanding successful strategies "
            f"from {best_region} while investigating the "
            f"lower performance of {worst_region}."
        )


if category_col and sales_col:

    category_analysis = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(category_analysis) > 1:

        best_category = category_analysis.idxmax()

        worst_category = category_analysis.idxmin()

        recommendations.append(
            f"Prioritize the {best_category} category "
            f"while reviewing pricing, marketing, and "
            f"demand for {worst_category}."
        )


if discount_col:

    discount_values = pd.to_numeric(
        df[discount_col],
        errors="coerce"
    )

    average_discount = discount_values.mean()

    if average_discount > 0.20:

        recommendations.append(
            "Average discount levels appear relatively "
            "high. Review discounting strategy to protect "
            "profit margins."
        )

    else:

        recommendations.append(
            "Discount levels appear relatively controlled. "
            "Continue monitoring their impact on sales "
            "and profitability."
        )


if profit_col:

    profit_values = pd.to_numeric(
        df[profit_col],
        errors="coerce"
    )

    if profit_values.sum() > 0:

        recommendations.append(
            "Maintain focus on profitable products and "
            "regions while identifying opportunities to "
            "increase margins."
        )

    else:

        recommendations.append(
            "Investigate the main drivers of negative "
            "profitability before increasing sales volume."
        )


if recommendations:

    for recommendation in recommendations:

        st.success(
            f"💡 {recommendation}"
        )

else:

    st.info(
        "No specific recommendations could be generated "
        "from the available columns."
    )
# -----------------------------------------
# STEP 10: EXECUTIVE BUSINESS REPORT
# -----------------------------------------

st.divider()

st.header("🤖 AI-Style Executive Business Report")

st.write(
    "A concise management-level summary generated "
    "automatically from the uploaded business data."
)


# -----------------------------------------
# Prepare report values
# -----------------------------------------

report_sales = None
report_profit = None
report_orders = None
report_region = None
report_category = None
report_product = None
report_discount = None


# -----------------------------------------
# Total Sales
# -----------------------------------------

if sales_col:

    report_sales = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    ).sum()


# -----------------------------------------
# Total Profit
# -----------------------------------------

if profit_col:

    report_profit = pd.to_numeric(
        df[profit_col],
        errors="coerce"
    ).sum()


# -----------------------------------------
# Total Orders
# -----------------------------------------

if order_col:

    report_orders = df[order_col].nunique()

else:

    report_orders = len(df)


# -----------------------------------------
# Best Region
# -----------------------------------------

if region_col and sales_col:

    region_report = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(region_report) > 0:

        report_region = region_report.index[0]


# -----------------------------------------
# Best Category
# -----------------------------------------

if category_col and sales_col:

    category_report = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(category_report) > 0:

        report_category = category_report.index[0]


# -----------------------------------------
# Best Product
# -----------------------------------------

if product_col and sales_col:

    product_report = (
        df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    if len(product_report) > 0:

        report_product = product_report.index[0]


# -----------------------------------------
# Average Discount
# -----------------------------------------

if discount_col:

    report_discount = pd.to_numeric(
        df[discount_col],
        errors="coerce"
    ).mean()


# -----------------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------------

st.subheader("📋 Executive Summary")


summary_parts = []


if report_sales is not None:

    summary_parts.append(
        f"The dataset generated total sales of "
        f"{report_sales:,.2f}"
    )


if report_orders is not None:

    summary_parts.append(
        f"across {report_orders:,} orders/records"
    )


if report_region:

    summary_parts.append(
        f"The strongest region was {report_region}"
    )


if report_category:

    summary_parts.append(
        f"while {report_category} was the leading category"
    )


if report_profit is not None:

    if report_profit > 0:

        summary_parts.append(
            "and overall profitability was positive"
        )

    else:

        summary_parts.append(
            "while overall profitability requires attention"
        )


if summary_parts:

    executive_summary = ". ".join(summary_parts) + "."

    st.success(executive_summary)

else:

    st.info(
        "Insufficient business information "
        "to generate an executive summary."
    )


# -----------------------------------------
# SALES PERFORMANCE
# -----------------------------------------

st.subheader("📈 Sales Performance")


if report_sales is not None:

    st.write(
        f"Total sales amounted to **{report_sales:,.2f}**."
    )

    if report_region:

        st.write(
            f"The **{report_region}** region generated "
            f"the highest sales."
        )

    if report_category:

        st.write(
            f"The **{report_category}** category was "
            f"the strongest sales contributor."
        )

else:

    st.warning(
        "Sales information was not detected."
    )


# -----------------------------------------
# PROFITABILITY
# -----------------------------------------

st.subheader("💰 Profitability Analysis")


if report_profit is not None:

    if report_profit > 0:

        st.success(
            f"Total profit is **{report_profit:,.2f}**, "
            f"indicating positive overall profitability."
        )

    elif report_profit < 0:

        st.error(
            f"Total profit is **{report_profit:,.2f}**. "
            f"The business should investigate cost, pricing, "
            f"and discount drivers."
        )

    else:

        st.warning(
            "Total profit is approximately zero."
        )

else:

    st.info(
        "Profit column was not detected in the dataset."
    )


# -----------------------------------------
# CUSTOMER / ORDER ANALYSIS
# -----------------------------------------

st.subheader("🧾 Order Analysis")


if report_orders:

    st.write(
        f"The dataset contains **{report_orders:,} "
        f"unique orders/records**."
    )


if sales_col and report_orders:

    average_order = (
        report_sales / report_orders
    )

    st.write(
        f"The estimated average order value is "
        f"**{average_order:,.2f}**."
    )


# -----------------------------------------
# DISCOUNT ANALYSIS
# -----------------------------------------

st.subheader("🏷️ Discount Analysis")


if report_discount is not None:

    st.write(
        f"The average recorded discount is "
        f"**{report_discount:.2f}**."
    )

    if report_discount > 0.20:

        st.warning(
            "Discount levels appear relatively high. "
            "Management should evaluate their impact "
            "on profit margins."
        )

    else:

        st.success(
            "Discount levels appear relatively controlled."
        )

else:

    st.info(
        "Discount information was not detected."
    )


# -----------------------------------------
# KEY RISKS
# -----------------------------------------

st.subheader("⚠️ Areas Requiring Attention")


risks = []


if region_col and sales_col:

    region_report = (
        df.groupby(region_col)[sales_col]
        .sum()
        .sort_values(ascending=True)
    )

    if len(region_report) > 1:

        weakest_region = region_report.index[0]

        risks.append(
            f"Investigate the relatively weak sales "
            f"performance of the {weakest_region} region."
        )


if category_col and sales_col:

    category_report = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=True)
    )

    if len(category_report) > 1:

        weakest_category = category_report.index[0]

        risks.append(
            f"Review demand and performance of the "
            f"{weakest_category} category."
        )


if report_profit is not None and report_profit < 0:

    risks.append(
        "Overall profitability is negative and "
        "requires immediate investigation."
    )


if report_discount is not None and report_discount > 0.20:

    risks.append(
        "High discounting may be reducing profit margins."
    )


if risks:

    for risk in risks:

        st.warning(
            f"⚠️ {risk}"
        )

else:

    st.success(
        "No major business risks were automatically detected."
    )


# -----------------------------------------
# MANAGEMENT RECOMMENDATIONS
# -----------------------------------------

st.subheader("💡 Recommended Actions")


actions = []


if report_region:

    actions.append(
        f"Study the strategies driving strong performance "
        f"in {report_region} and consider applying them "
        f"to weaker regions."
    )


if report_category:

    actions.append(
        f"Maintain focus on the {report_category} category "
        f"while identifying opportunities to improve "
        f"lower-performing categories."
    )


if report_product:

    actions.append(
        f"Use {report_product} as a benchmark for "
        f"understanding successful product performance."
    )


if report_discount is not None:

    if report_discount > 0.20:

        actions.append(
            "Review discount policies and measure whether "
            "discounts are generating enough additional "
            "sales to justify reduced margins."
        )

    else:

        actions.append(
            "Continue monitoring discount levels while "
            "balancing sales growth and profitability."
        )


if report_profit is not None:

    if report_profit > 0:

        actions.append(
            "Prioritize profitable growth rather than "
            "sales growth alone."
        )

    else:

        actions.append(
            "Investigate costs, pricing, discounts, and "
            "product-level margins before pursuing "
            "aggressive sales expansion."
        )


if actions:

    for number, action in enumerate(actions, start=1):

        st.write(
            f"**{number}.** {action}"
        )


# -----------------------------------------
# REPORT FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "This report is automatically generated from "
    "the uploaded dataset using rule-based business "
    "analysis. It should be validated against business "
    "context before making major decisions."
)

# -----------------------------------------
# STEP 11: AI BUSINESS ANALYST CHATBOT
# -----------------------------------------

st.divider()

st.header("🤖 Ask Your AI Business Analyst")

st.write(
    "Ask natural-language questions about your uploaded "
    "business data, products, regions, categories, sales, "
    "profit, quantity, orders, and discounts."
)


# -----------------------------------------
# USER QUESTION
# -----------------------------------------

user_question = st.text_input(
    "💬 Ask a business question",
    placeholder="Example: Which product has the highest sales?",
    key="ai_business_question"
)


# -----------------------------------------
# AI BUSINESS ANALYST
# -----------------------------------------

if user_question:

    try:

        # ---------------------------------
        # CREATE BUSINESS CONTEXT
        # ---------------------------------

        context = []

        context.append("BUSINESS DATASET SUMMARY")

        context.append(
            f"Number of records: {len(df):,}"
        )

        context.append(
            f"Number of columns: {len(df.columns)}"
        )


        # ---------------------------------
        # SALES
        # ---------------------------------

        if sales_col:

            sales_values = pd.to_numeric(
                df[sales_col],
                errors="coerce"
            )

            total_sales_ai = sales_values.sum()

            average_sales_ai = sales_values.mean()

            context.append(
                f"Total sales: {total_sales_ai:,.2f}"
            )

            context.append(
                f"Average sales per record: "
                f"{average_sales_ai:,.2f}"
            )


        # ---------------------------------
        # PROFIT
        # ---------------------------------

        if profit_col:

            profit_values = pd.to_numeric(
                df[profit_col],
                errors="coerce"
            )

            total_profit_ai = profit_values.sum()

            average_profit_ai = profit_values.mean()

            context.append(
                f"Total profit: {total_profit_ai:,.2f}"
            )

            context.append(
                f"Average profit per record: "
                f"{average_profit_ai:,.2f}"
            )


        # ---------------------------------
        # QUANTITY
        # ---------------------------------

        if quantity_col:

            quantity_values = pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            )

            total_quantity_ai = quantity_values.sum()

            context.append(
                f"Total quantity sold: "
                f"{total_quantity_ai:,.0f}"
            )


        # ---------------------------------
        # ORDERS
        # ---------------------------------

        if order_col:

            total_orders_ai = df[order_col].nunique()

        else:

            total_orders_ai = len(df)

        context.append(
            f"Total orders/records: "
            f"{total_orders_ai:,}"
        )


        # ---------------------------------
        # DISCOUNT
        # ---------------------------------

        if discount_col:

            discount_values = pd.to_numeric(
                df[discount_col],
                errors="coerce"
            )

            average_discount_ai = discount_values.mean()

            context.append(
                f"Average discount: "
                f"{average_discount_ai:.2f}"
            )


        # ---------------------------------
        # PRODUCT ANALYSIS
        # ---------------------------------

        if product_col:

            context.append("")
            context.append("PRODUCT PERFORMANCE")

            if sales_col:

                product_sales = (
                    df.groupby(product_col)[sales_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Products ranked by sales:"
                )

                for name, value in product_sales.head(10).items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


            if profit_col:

                product_profit = (
                    df.groupby(product_col)[profit_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Products ranked by profit:"
                )

                for name, value in product_profit.head(10).items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


        # ---------------------------------
        # REGION ANALYSIS
        # ---------------------------------

        if region_col:

            context.append("")
            context.append("REGIONAL PERFORMANCE")

            if sales_col:

                region_sales = (
                    df.groupby(region_col)[sales_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Regions ranked by sales:"
                )

                for name, value in region_sales.items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


            if profit_col:

                region_profit = (
                    df.groupby(region_col)[profit_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Regions ranked by profit:"
                )

                for name, value in region_profit.items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


        # ---------------------------------
        # CATEGORY ANALYSIS
        # ---------------------------------

        if category_col:

            context.append("")
            context.append("CATEGORY PERFORMANCE")

            if sales_col:

                category_sales = (
                    df.groupby(category_col)[sales_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Categories ranked by sales:"
                )

                for name, value in category_sales.items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


            if profit_col:

                category_profit = (
                    df.groupby(category_col)[profit_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context.append(
                    "Categories ranked by profit:"
                )

                for name, value in category_profit.items():

                    context.append(
                        f"- {name}: {value:,.2f}"
                    )


        # ---------------------------------
        # DATA QUALITY
        # ---------------------------------

        context.append("")
        context.append("DATA QUALITY")

        context.append(
            f"Missing values: "
            f"{int(df.isnull().sum().sum())}"
        )

        context.append(
            f"Duplicate rows: "
            f"{int(df.duplicated().sum())}"
        )


        # ---------------------------------
        # FINAL BUSINESS CONTEXT
        # ---------------------------------

        business_context = "\n".join(context)


        # ---------------------------------
        # GEMINI PROMPT
        # ---------------------------------

        prompt = f"""
You are a professional Business Analyst.

You are analyzing the user's uploaded business dataset.

Your job is to answer the user's question intelligently
using the business information supplied below.

IMPORTANT RULES:

1. Understand the meaning of the question, not just keywords.

2. If the user asks:
   "Which product?"
   interpret it as a request for product information.
   If no metric is specified, use sales as the default.

3. If the user asks about the best product, region, or category,
   identify the highest-performing one using the relevant metric.

4. If the user asks "why", use the available data to provide
   a reasonable data-supported explanation.

5. Never invent numbers.

6. Never invent products, regions, categories, or metrics.

7. Use the exact values supplied in BUSINESS DATA.

8. If the requested information is unavailable, say so clearly.

9. Give practical business insights.

10. When appropriate, provide a recommendation.

11. Keep answers clear and professional.

12. Answer directly first, then explain briefly.

USER QUESTION:

{user_question}


BUSINESS DATA:

{business_context}


Now answer the user's question as a professional
Business Analyst.
"""


        # ---------------------------------
        # GEMINI CONNECTION
        # ---------------------------------

        from google import genai
        import time

        client = genai.Client()


        # ---------------------------------
        # TRY FREE GEMINI MODELS
        # ---------------------------------

        models_to_try = [
            "gemini-3.1-flash-lite",
            "gemini-3-flash-preview"
        ]

        response = None
        last_error = None


        for model_name in models_to_try:

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    if response and response.text:

                        break

                except Exception as e:

                    last_error = e

                    time.sleep(2)


            if response and response.text:

                break


        # ---------------------------------
        # CHECK RESPONSE
        # ---------------------------------

        if response is None or not response.text:

            if last_error:

                raise last_error

            else:

                raise Exception(
                    "Gemini did not return a response."
                )


        # ---------------------------------
        # DISPLAY RESPONSE
        # ---------------------------------

        st.subheader(
            "🤖 AI Business Analyst Response"
        )

        st.markdown(
            response.text
        )


    # -------------------------------------
    # ERROR HANDLING
    # -------------------------------------

    except Exception as e:

        st.error(
            "Unable to generate the AI response."
        )

        st.code(
            str(e)
        )