from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from database import get_db_connection
import psycopg2.extras

app = FastAPI(title="LifeAudit API")

# Setup CORS agar bisa diakses oleh frontend (HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema data yang dikirim user
class LogSchema(BaseModel):
    date: date
    journal_text: str
    sleep_hours: float
    mood_emoji: str

@app.get("/")
def read_root():
    return {"message": "API LifeAudit Siap Digunakan!"}

# 1. ENDPOINT UNTUK MENYIMPAN DATA (POST)
@app.post("/logs")
def create_log(payload: LogSchema):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Gagal terhubung ke database")
    
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO daily_logs (date, journal_text, sleep_hours, mood_emoji)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET journal_text = EXCLUDED.journal_text,
                sleep_hours = EXCLUDED.sleep_hours,
                mood_emoji = EXCLUDED.mood_emoji;
        """
        cursor.execute(query, (payload.date, payload.journal_text, payload.sleep_hours, payload.mood_emoji))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "Sukses", "message": "Catatan harian berhasil disimpan!"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")

# 2. ENDPOINT UNTUK MENGAMBIL SEMUA DATA (GET)
@app.get("/logs")
def get_all_logs():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Gagal terhubung ke database")
    
    try:
        # Menggunakan RealDictCursor agar langsung berbentuk JSON yang ramah frontend
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM daily_logs ORDER BY date DESC;")
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=400, detail=f"Gagal mengambil data: {str(e)}")