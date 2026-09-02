import pandas as pd
import os


# ============================================================
# GET PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Go one folder back from "website" to "Plant care system"

PROJECT_DIR = os.path.dirname(
    BASE_DIR
)


# ============================================================
# DATASET PATH
# ============================================================

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "data",
    "final_plant_dataset.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    DATA_PATH
)


# ============================================================
# REMOVE OLD CURRY LEAF ENTRY IF IT EXISTS
# ============================================================

if "typeName" in df.columns:

    df = df[
        ~df["typeName"]
        .astype(str)
        .str.lower()
        .str.contains(
            "curry leaf",
            na=False
        )
    ]


# ============================================================
# CURRY LEAF DATA
# ============================================================

curry_leaf = {

    "typeName":
    "Curry Leaf",

    "origin":
    "India",

    "category":
    "Herbs",

    "lightPreference":
    "Outdoor Full Sun",

    "humidityPreference":
    "Medium",

    "temperaturePreference":
    "[18, 35]",

    "springInterval":
    4,

    "summerInterval":
    3,

    "fallInterval":
    5,

    "winterInterval":
    7,

    "growthRate":
    "Moderate",

    "plantToxicity":
    "Non-Toxic",

    "careTips":
    "Grow curry leaf plants in a warm sunny location with well-draining soil. Water when the top layer of soil begins to dry, but avoid waterlogging. Provide plenty of sunlight for healthy growth. Protect the plant from frost and extremely cold temperatures. Prune regularly to encourage bushier growth and remove damaged leaves."

}


# ============================================================
# ADD CURRY LEAF TO DATASET
# ============================================================

new_row = pd.DataFrame(
    [curry_leaf]
)


df = pd.concat(
    [
        df,
        new_row
    ],
    ignore_index=True
)


# ============================================================
# SAVE UPDATED DATASET
# ============================================================

df.to_csv(
    DATA_PATH,
    index=False
)


# ============================================================
# SUCCESS MESSAGE
# ============================================================

print(
    "Curry Leaf added successfully!"
)

print(
    f"Dataset saved at: {DATA_PATH}"
)

print(
    f"Total plants in dataset: {len(df)}"
)