from config import db

try:
    import psycopg2
except Exception:
    psycopg2 = None


def con():
    if psycopg2 is None:
        return None
    return psycopg2.connect(**db)


def make_db():
    try:
        c = con()
        if c is None:
            return
        cur = c.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        c.commit()
        cur.close()
        c.close()
    except Exception:
        pass


def pid(name):
    try:
        c = con()
        if c is None:
            return None
        cur = c.cursor()
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
            (name,),
        )
        cur.execute("SELECT id FROM players WHERE username = %s", (name,))
        r = cur.fetchone()
        c.commit()
        cur.close()
        c.close()
        if r:
            return r[0]
    except Exception:
        return None


def save(name, sc, lv):
    try:
        i = pid(name)
        if i is None:
            return
        c = con()
        if c is None:
            return
        cur = c.cursor()
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (i, sc, lv),
        )
        c.commit()
        cur.close()
        c.close()
    except Exception:
        pass


def best(name):
    try:
        c = con()
        if c is None:
            return 0
        cur = c.cursor()
        cur.execute("""
            SELECT COALESCE(MAX(g.score), 0)
            FROM players p
            LEFT JOIN game_sessions g ON p.id = g.player_id
            WHERE p.username = %s
        """, (name,))
        r = cur.fetchone()
        cur.close()
        c.close()
        if r:
            return r[0]
    except Exception:
        return 0
    return 0


def top():
    try:
        c = con()
        if c is None:
            return []
        cur = c.cursor()
        cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            ORDER BY g.score DESC, g.played_at ASC
            LIMIT 10
        """)
        r = cur.fetchall()
        cur.close()
        c.close()
        return r
    except Exception:
        return []
