import sqlite3 as sql


class Repository:
    def migrate(self):
        with sql.connect("db.db") as connection:
            try:
                connection.execute(
                    "CREATE TABLE LISTINGS(JSON_URI NOT NULL, EIN, NAME)"
                )
            except sql.OperationalError:
                print("Table 'LISTINGS' already exists")

    def get_data_by_name(self, NAME):
        with sql.connect("db.db") as connection:
            result = connection.execute(
                f"SELECT NAME, JSON_URI, EIN FROM LISTINGS WHERE LOWER(NAME) LIKE '%{NAME.lower()}%' "
            )
        return [
            {"name": item[0], "json_uri": item[1], "ein": item[2]} for item in result
        ]

    def get_rows_without_ein(self):
        with sql.connect("db.db") as connection:
            return connection.execute(
                "SELECT JSON_URI FROM LISTINGS WHERE EIN IS NULL"
            ).fetchall()

    def insert_bulk_with_name(self, data):
        with sql.connect("db.db") as connection:
            connection.executemany(
                "INSERT INTO LISTINGS (JSON_URI, NAME) VALUES(?,?)", data
            )
            connection.execute(
                "DELETE FROM LISTINGS WHERE rowid NOT IN ( SELECT MIN(rowid) FROM LISTINGS GROUP BY JSON_URI)"
            )
            connection.commit()

    def update_ein(self, JSON_URI, NAME):
        print("YOOOOOOOOOOOOOOOOOOO")
        with sql.connect("db.db") as connection:
            connection.execute(
                f"UPDATE LISTINGS SET (JSON_URI, NAME) = ({JSON_URI}, {NAME}) WHERE JSON_URI = {JSON_URI}"
            )
            connection.commit()
