from app.database import get_connection


class UserRepository:
    def find_by_email(self, email: str) -> dict | None:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, email, password_hash, created_at FROM users WHERE email = %s",
                    (email,),
                )
                return cur.fetchone()
        finally:
            conn.close()

    def create(self, name: str, email: str, password_hash: str) -> dict:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (name, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, email, created_at
                    """,
                    (name, email, password_hash),
                )
                user = cur.fetchone()
                conn.commit()
                return dict(user)
        finally:
            conn.close()