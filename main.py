import sqlite3
import openpyxl
from pathlib import Path

p = Path(".")

workbooks = []
for child in p.iterdir():
   if str(child.suffix) == ".xlsx":
       workbooks.append(str(child))

wookbook1= openpyxl.load_workbook(workbooks[0])
worksheet1 = wookbook1.active

wookbook2= openpyxl.load_workbook(workbooks[1])
worksheet2 = wookbook2.active

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
    CREATE TABLE IF NOT EXISTS data1 
        (id VARCHAR NOT NULL,
        value REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS data2 
        (id VARCHAR NOT NULL,
        value REAL NOT NULL);    
        """)

for row  in worksheet1.values:
    cur.execute("insert into data1 values (?, ?)", row)

for row  in worksheet2.values:
    cur.execute("insert into data2 values (?, ?)", row)
    
cur.execute("""
    SELECT id, SUM(value) as value
        FROM
        (
            SELECT id, value AS value FROM data1
            UNION ALL
            SELECT id, -value FROM data2
        )
        GROUP BY id
        HAVING SUM(value) <> 0""")

result = cur.fetchall()
for i in result:
    print(i)

input()