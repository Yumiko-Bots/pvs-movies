from config.config import DATABASE_URL
import psycopg2

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
