# debug_db.py
import os
import lancedb

print(f"CWD: {os.getcwd()}")
print(f"DB path absolute: {os.path.abspath('storage/lancedb_store')}")
print(f"DB path exists: {os.path.exists('storage/lancedb_store')}")

db = lancedb.connect("storage/lancedb_store")
print(f"Tables: {db.table_names()}")

table = db.open_table("research_documents")
print(f"Row count: {table.count_rows()}")
print(f"Schema: {table.schema}")
print(f"First row: {table.to_pandas().head(1)}")