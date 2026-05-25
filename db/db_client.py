import psycopg2


class DbClient:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        conn = psycopg2.connect(**self.db_config)
        return conn

    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

        cursor.close()
        conn.close()