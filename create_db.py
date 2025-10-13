import pymysql

mydb = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    cursorclass=pymysql.cursors.DictCursor  # Optional: Returns dicts for easier handling
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS Users")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)

mydb.close()
