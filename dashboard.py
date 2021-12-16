import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
st.set_page_config(page_title="Dashboard",page_icon="random", layout="wide",initial_sidebar_state="collapsed")
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="Sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    return df

df = get_data_from_excel()
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)
df_selection = df.query(
    "City == @city"
)
st.title(" Dashboard")
st.markdown("##")
total_sales = int(df_selection["Total"].sum())
average_unit_price = round(df_selection["Unit price"].mean(), 1)
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)
income = int(df_selection["gross income"].sum())


first, second, third ,fourth= st.columns(4)
with first:
    st.subheader("Total Sales:")
    st.subheader(f"$ {total_sales:,}")
with second:
    st.subheader("Average Unit Price:")
    st.subheader(f"{average_unit_price}")
with third:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"$ {average_sale_by_transaction}")
with fourth:
    st.subheader("Total net Profit")
    st.subheader(f"$ {income}")    

st.markdown("""---""")
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Products Sold</b>",
    color_discrete_sequence=["#b80047"] * len(sales_by_product_line),
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(174, 11, 177, 0.8)",
    xaxis=(dict(showgrid=False))
)
fig = px.pie(df["Payment"], title="<b>Payment Type</b>", names='Payment',color_discrete_sequence=px.colors.sequential.RdBu)

first, second = st.columns(2)
first.plotly_chart(fig, use_container_width=True)
second.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("""---""")
sales2 = (
    df_selection.groupby(by=["Customer_type"]).sum()[["Total"]].sort_values(by="Total")
)
fig3 = px.bar(
    sales2,
    x="Total",
    y=sales2.index,
    orientation="h",
    title="<b>Sold by Customer Type</b>",
    color_discrete_sequence=["#b80047"] * len(sales2),
)
fig3.update_layout(
    plot_bgcolor="rgba(174, 11, 177, 0.8)",
    xaxis=(dict(showgrid=False))
)
fig2 = go.Figure(data=[go.Pie(labels=df["Gender"], hole=.3)])


first, second = st.columns(2)
first.plotly_chart(fig2, use_container_width=True)
second.plotly_chart(fig3, use_container_width=True)