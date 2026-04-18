from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.zactgkcbgxynlguwiqwe:g00dn1ght422hb1@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB Connected")
        print("Result:", result.scalar())

except Exception as e:
    print("Connection failed")
    print(e)