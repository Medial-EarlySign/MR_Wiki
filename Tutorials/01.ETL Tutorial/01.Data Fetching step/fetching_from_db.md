# Fetching from Databases

Fetching data from a database follows the same lazy-iterator pattern as file-based fetching but uses database-specific helpers from `ETL_Infra`.

The core helper is `db_fetcher`. To support batching and resuming without loading the entire dataset into memory, `db_fetcher` automatically wraps your SQL query to sort the results by patient ID (`ORDER BY pid`). 

> **[Important]:** Your SQL query *must* return a column named `pid`.

To maintain the state between batches (remembering the last processed `pid`), you must also initialize and pass a `batch_mapper` dictionary.

> **[NOTE]** When the database is small and can ne all loaded in one batch, those steps are less important.

### Example Usage

Here is a complete example demonstrating how to initialize the `DB_Access` object and create a database fetcher function:

```python
from typing import Dict
from ETL_Infra.data_fetcher.db_fetcher import db_fetcher, DB_Access

# 1. Initialize a global batch mapper to remember the last pid seen in each batch
batch_mapper: Dict[int, str] = dict()

# 2. Initialize the database access object
def get_db() -> DB_Access:
    user = 'my_user'
    password = 'my_password'
    host = 'localhost'
    port = 5439
    database = 'my_db'
    
    # Build your SQLAlchemy connection string
    conn_str = f"redshift+redshift_connector://{user}:{password}@{host}:{port}/{database}"
    
    # Initialize DB_Access (you can also pass connect_args like {"sslmode": "verify-ca"})
    db = DB_Access(conn_str, {"sslmode": "verify-ca"})
    return db

# 3. Create the data fetcher function
def db_demographic_fetcher(batch_size: int, start_batch: int):
    db = get_db()
    
    # Define the query. Ensure the patient identifier is aliased as "pid"
    query = """
        SELECT ptid as pid, birth_yr as byear, gender as sex 
        FROM db_schema.patient
    """
    
    # db_fetcher automatically adds the `ORDER BY pid` to this query and handles batching
    return db_fetcher(db, query, batch_size, start_batch, batch_mapper)
```
