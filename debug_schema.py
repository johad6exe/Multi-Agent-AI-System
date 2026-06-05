# debug_schema.py
import lancedb
import pandas as pd

db = lancedb.connect("storage/lancedb_store")
table = db.open_table("research_documents")

df = table.to_pandas()
print(f"Columns: {df.columns.tolist()}")
print(f"Row count: {len(df)}")
print(f"\nFirst row payload:\n{df['payload'].iloc[0]}")