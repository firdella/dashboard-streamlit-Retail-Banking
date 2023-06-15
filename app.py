import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title('Explore Retail Banking Dataset')
# Load Data
client = pd.read_csv("./create data/completedclient.csv")
card = pd.read_csv("./create data/completedcard.csv")
dacct = pd.read_csv("./create data/completedacct.csv")
loan = pd.read_csv("./create data/completedloan.csv")
poss = pd.read_csv("./create data/completeddisposition.csv")
distrik = pd.read_csv("./create data/completeddistrict.csv")
dl_merge = pd.merge(dacct,loan, on=["account_id", "year"])


###########################
st.header("Histogram")
st.markdown("## Distribution age customer")
fig = plt.figure(figsize=(6, 4))
plt.xlabel('Age')
plt.ylabel('Count')
plt.hist(client["age"])
st.plotly_chart(fig)
#st.caption('This is a string that explains something above.') 
#############################

############################
st.header("Boxplot")
dm = dl_merge
#st.dataframe(dm)
year_values = (int(dm["year"].min()), int(dm["year"].max()))
metrics = ["duration", "payments", "amount"]
dimension = ["frequency", "year" , "status", "month", "purpose"]

def box_plot(dm, x, y):    
    fig = px.box(
        dm, x=x, y=y, hover_data=dm[dimension + [x]],
        points="all", color=x)
    return fig

st.markdown("## Show Relation using Boxplot")
col1, col2 = st.columns(2)
with col1:
    x = st.selectbox("Select X", dimension, 1, key="boxplot_x")
with col2:
    y = st.selectbox("Select Y", metrics, key="boxplot_y")
st.plotly_chart(box_plot(dm, x, y))
############################################

#############################
st.header("Linechart")
st.markdown("## Trend payments")
l_groupby = loan.groupby(["year", "purpose","status"], as_index=False)['amount'].sum()
def plot():

    chs = l_groupby['purpose'].unique()
    purpose = st.selectbox('Select purpose', chs)
    fig = px.line(l_groupby[l_groupby['purpose'] == purpose], x = "year", y = "amount", color="status"
    )
    plt.grid(True)
    st.plotly_chart(fig)
plot()
p = loan.loc[0:, ['status', 'purpose', 'payments','duration','amount','year','date']]
st.dataframe(p)
#############################
