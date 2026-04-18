from sqlalchemy import text
from db.db import engine

with open("db/optimize.sql", "r") as f:
    sql = f.read()

with engine.connect() as conn:
    for statement in sql.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))

print("DB optimized successfully")