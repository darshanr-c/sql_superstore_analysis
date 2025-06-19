import pandas as pd
from sqlalchemy import create_engine

# Load CSV file
df = pd.read_csv("data/superstore_raw.csv", encoding="latin1")

# Set up connection string
engine = create_engine("postgresql+psycopg2://postgres:<password>@localhost:5432/superstore_db")

# Load dataframe to PostgreSQL (replace if exists)
df.to_sql("orders", engine, if_exists="replace", index=False)

print("Data loaded successfully.")