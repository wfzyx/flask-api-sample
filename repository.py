import sqlite3 as sql


def _execute(sqlcmd):
    with sql.connect("db.db") as connection:
        return connection.execute(sqlcmd)


def migrate():
    with sql.connect("db.db") as connection:
        try:
            connection.execute("CREATE TABLE LISTINGS(JSON_URI NOT NULL, EIN, NAME)")
        except sql.OperationalError:
            print("Table 'LISTINGS' already exists")


def get_data_by_name(NAME):
    result = _execute(
        f"SELECT NAME, JSON_URI, EIN FROM LISTINGS WHERE LOWER(NAME) LIKE '%{NAME.lower()}%'"
    )
    return [{"name": item[0], "json_uri": item[1], "ein": item[2]} for item in result]


def get_data_by_ein(EIN):
    result = _execute(
        f"SELECT NAME, JSON_URI, EIN FROM LISTINGS WHERE EIN LIKE '%{EIN}%'"
    )
    return [{"name": item[0], "json_uri": item[1], "ein": item[2]} for item in result]


def get_rows_without_ein():
    return _execute("SELECT JSON_URI FROM LISTINGS WHERE EIN IS NULL").fetchall()


def insert_bulk_with_name(data):
    with sql.connect("db.db") as connection:
        connection.executemany(
            "INSERT INTO LISTINGS (JSON_URI, NAME) VALUES(?,?)", data
        )
        connection.execute(
            "DELETE FROM LISTINGS WHERE rowid NOT IN ( SELECT MIN(rowid) FROM LISTINGS GROUP BY JSON_URI)"
        )
        connection.commit()


def update_ein(JSON_URI, EIN):
    with sql.connect("db.db") as connection:
        connection.execute(
            f"UPDATE LISTINGS SET (EIN) = ('{EIN}') WHERE JSON_URI = '{JSON_URI}'"
        )
        connection.commit()
