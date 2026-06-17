# debug_schema.py
import lancedb

db = lancedb.connect("storage/lancedb_store")
table = db.open_table("research_documents")

print(table.schema)
print(60*"-")
print(table.list_indices())
print(60*"-")
print(table.count_rows())
print(60*"-")
df = table.to_pandas()
print(f"Columns: {df.columns.tolist()}")
print(60*"-")
print(f"Row count: {len(df)}")
print(60*"-")
df['payload'].iloc[0:5].to_csv("sample_payload.csv")