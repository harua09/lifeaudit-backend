import psycopg2
from psycopg2.extras import RealDictCursor

# URL Koneksi PostgreSQL ke Supabase
# ⚠️ PENTING: Ganti RAHASIA_PASSWORD_KAMU dengan password database Supabase yang kamu buat saat buat project ini!
DATABASE_URL = "postgresql://postgres:Dila-0108089_KAMU@db.eynkmsgdsgcwqtyarhhy.supabase.co:5432/postgres"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Koneksi Database Gagal: {e}")
        return None