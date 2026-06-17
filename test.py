import pandas as pd
import json
import lancedb

db = lancedb.connect("storage/lancedb_store")
table = db.open_table("research_documents")
df = table.to_pandas()

# 1. Define a function to parse the JSON string and extract chunk_size
def get_chunk_size(payload_string):
    try:
        # Parse the JSON string into a Python dictionary
        data = json.loads(payload_string)
        # Safely extract the chunk_size from meta_data
        return data.get('meta_data', {}).get('chunk_size')
    except (json.JSONDecodeError, TypeError):
        # Return None if there's an error parsing or missing data
        return None

# 2. Apply the function to create a new column with just the chunk sizes
df['chunk_size'] = df['payload'].apply(get_chunk_size)

# 3. Calculate the average (pandas automatically ignores None/NaN values)
average_chunk_size = df['chunk_size'].mean()

print(f"Average Chunk Size: {average_chunk_size}")