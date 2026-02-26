import streamlit as st
import pandas as pd
import os
from PIL import Image
import random

# -------------------------------
# CONFIG
# -------------------------------

st.set_page_config(page_title="Smart OOTD Builder", layout="wide")

image_folder = "images/images"

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("styles.csv", on_bad_lines="skip")
    df = df[df['gender'].isin(['Men', 'Women'])]

    # Keep only rows with existing images
    valid_ids = []
    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            if file.endswith(".jpg"):
                valid_ids.append(int(file.split(".")[0]))

    df = df[df['id'].isin(valid_ids)]
    return df

df = load_data()

# -------------------------------
# TITLE
# -------------------------------

st.title("👗 Smart OOTD Builder")
st.write("Build your Outfit Of The Day with full control")

if df.empty:
    st.error("No valid data found. Check images folder and styles.csv.")
    st.stop()

# -------------------------------
# GENDER
# -------------------------------

gender = st.selectbox("Select Gender", ["Men", "Women"])
gender_df = df[df['gender'] == gender]

# -------------------------------
# TOPWEAR
# -------------------------------

st.subheader("👕 Topwear")

top_df = gender_df[gender_df['subCategory'] == "Topwear"]

top_type = st.selectbox(
    "Select Top Type",
    ["None"] + sorted(top_df['articleType'].dropna().unique())
)

top_item = None

if top_type != "None":
    filtered = top_df[top_df['articleType'] == top_type]

    top_color = st.selectbox(
        "Select Top Color",
        ["Any"] + sorted(filtered['baseColour'].dropna().unique())
    )

    if top_color == "Any":
        top_item = filtered.sample(1).iloc[0]
    else:
        top_item = filtered[filtered['baseColour'] == top_color].sample(1).iloc[0]

# -------------------------------
# BOTTOMWEAR
# -------------------------------

st.subheader("👖 Bottomwear")

bottom_df = gender_df[gender_df['subCategory'] == "Bottomwear"]

bottom_type = st.selectbox(
    "Select Bottom Type",
    ["None"] + sorted(bottom_df['articleType'].dropna().unique())
)

bottom_item = None

if bottom_type != "None":
    filtered = bottom_df[bottom_df['articleType'] == bottom_type]

    bottom_color = st.selectbox(
        "Select Bottom Color",
        ["Any"] + sorted(filtered['baseColour'].dropna().unique())
    )

    if bottom_color == "Any":
        bottom_item = filtered.sample(1).iloc[0]
    else:
        bottom_item = filtered[filtered['baseColour'] == bottom_color].sample(1).iloc[0]

# -------------------------------
# FOOTWEAR
# -------------------------------

st.subheader("👟 Footwear")

foot_df = gender_df[gender_df['masterCategory'] == "Footwear"]

foot_type = st.selectbox(
    "Select Footwear Type",
    ["None"] + sorted(foot_df['articleType'].dropna().unique())
)

foot_item = None

if foot_type != "None":
    filtered = foot_df[foot_df['articleType'] == foot_type]

    foot_color = st.selectbox(
        "Select Footwear Color",
        ["Any"] + sorted(filtered['baseColour'].dropna().unique())
    )

    if foot_color == "Any":
        foot_item = filtered.sample(1).iloc[0]
    else:
        foot_item = filtered[filtered['baseColour'] == foot_color].sample(1).iloc[0]

# -------------------------------
# DISPLAY OOTD
# -------------------------------

st.subheader("🔥 Your OOTD")

col1, col2, col3 = st.columns(3)

if top_item is not None:
    img = Image.open(f"{image_folder}/{top_item['id']}.jpg")
    col1.image(img, caption="Topwear")

if bottom_item is not None:
    img = Image.open(f"{image_folder}/{bottom_item['id']}.jpg")
    col2.image(img, caption="Bottomwear")

if foot_item is not None:
    img = Image.open(f"{image_folder}/{foot_item['id']}.jpg")
    col3.image(img, caption="Footwear")
