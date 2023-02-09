def insert(cursor, data, table):
    keys, values = data
    cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({values});")


def update(cursor, data, table):
    email, items = data
    cursor.execute(f"UPDATE {table} SET {items} WHERE email='{email}';")


def delete(cursor, data, table):
    email, _ = data
    cursor.execute(f"DELETE FROM {table} WHERE email='{email}';")


operations = {
    'INSERT': insert,
    'UPDATE': update,
    'DELETE': delete
}
