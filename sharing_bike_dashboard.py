import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_day_max_min_df(df):
    day_max_min_df = df.groupby(by="weekday").cnt.sum().sort_values(ascending=False).reset_index()
    day_max_min_df.rename(columns={
    "weekday": "hari",
    "cnt": "permintaan"
    }, inplace=True)
    day_max_min_df["category"] = day_max_min_df["permintaan"].apply(
    lambda x: "max" if x == day_max_min_df["permintaan"].max() else ("min" if x ==day_max_min_df["permintaan"].min() else("other"))
    )
    return day_max_min_df
    
def create_cuaca_df(df):
    cuaca_df = df.groupby(by="weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    cuaca_df.rename(columns={
    "weathersit": "cuaca",
    "cnt": "permintaan"
    }, inplace=True)
    return cuaca_df

def create_tahun_df(df):
    tahun_df = df.groupby(by="yr").cnt.sum().reset_index()
    tahun_df.rename(columns={
    "yr": "tahun",
    "cnt": "permintaan"
    }, inplace=True)
    tahun_df["tahun"] = tahun_df["tahun"].apply(
    lambda x: "2011" if x == 0 else "2012"
    )
    return tahun_df


def create_waktu_df(df):
    waktu_df = df.groupby(by="waktu").cnt.sum().reset_index()
    waktu_df.rename(columns={
    "cnt": "permintaan"
    }, inplace=True)
    waktu_df["category"] = waktu_df["permintaan"].apply(
    lambda x: "max" if x == waktu_df["permintaan"].max() else ("min" if x == waktu_df["permintaan"].min() else "other")
    )
    return waktu_df
    

day_df = pd.read_csv("bike_sharing_dataset/day1_df.csv")
hour_df = pd.read_csv("bike_sharing_dataset/hour1_df.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()



with st.sidebar:
    st.image("logo.png")
    
    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        )


main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date))&
    (day_df["dteday"] <= pd.to_datetime(end_date))
    ]
main1_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date))&
    (hour_df["dteday"] <= pd.to_datetime(end_date))
    ]    

day_max_min_df = create_day_max_min_df(main_df)
cuaca_df = create_cuaca_df(main1_df)
tahun_df = create_tahun_df(main_df)
waktu_df = create_waktu_df(main1_df)


st.header("Bike Sharing Services")

st.subheader("Akumulasi permintaan")

fig = plt.figure(figsize=(10, 5))
sns.barplot(
    y="permintaan",
    x="hari",
    data=day_max_min_df,
    hue="category",
    palette="muted"
)
plt.title("Total permintaan layanan sharing bike dalam hari", loc="center", fontsize=15)
plt.ylabel("Permintaan")
plt.xlabel("Hari ke-")
plt.tick_params(axis="x", labelsize=12)
plt.show()
st.pyplot(fig)

st.subheader("Pengaruh Cuaca")
fig1 = plt.figure(figsize=(10, 5))

sns.barplot(
    y="permintaan",
    x="cuaca",
    data=cuaca_df,
    palette="muted"
)
plt.title("Total perintaan layanan sharing bike tiap kategori cuaca", loc="center", fontsize=15)
plt.ylabel("Permintaan")
plt.xlabel("Kategori cuaca")
plt.tick_params(axis="x", labelsize=12)
plt.show()

st.pyplot(fig1)

st.subheader("Peningkatan tahunan")
fig2 = plt.figure(figsize=(10, 5))
plt.plot(
    tahun_df["tahun"],
    tahun_df["permintaan"],
    marker="o",
    linewidth=2
)
plt.title("Total permintaan layanan sharing bike per tahun", loc="center", fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

st.pyplot(fig2)

st.subheader("Pengaruh Waktu")
fig3 = plt.figure(figsize=(10, 5))
sns.barplot(
    y="permintaan",
    x="waktu",
    data=waktu_df,
    palette="muted",
    hue="category"
)
plt.title("Total permintaan layanan sharing bike terhadap waktu", loc="center", fontsize=15)
plt.ylabel("Permintaan")
plt.xlabel("Waktu")
plt.tick_params(axis="x", labelsize=12)
plt.show()

st.pyplot(fig3)
