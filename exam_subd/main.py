import sqlite3
import csv

connection = sqlite3.connect('base.db')
cursor = connection.cursor()


# -- Таблица "Магазин" (modified to match user's loop and image)
cursor.execute("""CREATE TABLE IF NOT EXISTS Store (
    StoreID TEXT PRIMARY KEY NOT NULL UNIQUE,
    District TEXT NOT NULL,
    Address TEXT
);""")
# -- Таблица "Товар"
cursor.execute("""CREATE TABLE IF NOT EXISTS Product (
    Article TEXT PRIMARY KEY,
    Department TEXT,
    ProductName TEXT,
    UnitOfMeasure TEXT,
    QuantityPerPackage INTEGER,
    PricePerPackage REAL
);""")
# -- Таблица "Движение товаров"
cursor.execute("""CREATE TABLE IF NOT EXISTS GoodsMovement (
    OperationID INTEGER PRIMARY KEY,
    Date DATE,
    StoreID TEXT,
    Article TEXT,
    PackageQuantity INTEGER,
    OperationType TEXT,
    FOREIGN KEY (StoreID) REFERENCES Store(StoreID),
    FOREIGN KEY (Article) REFERENCES Product(Article)
);""")

base = 'base.db'
move_goods = 'movement of goods.txt'
product = 'product.txt'
shop_txt = 'shop.txt'

# Загрузка данных в таблицу "Store" (modified to match user's loop)
for s in open(shop_txt, encoding="utf-8"):
    shop_data = s.strip().split('\t')
    if len(shop_data) < 3:
        continue
    cursor.execute("INSERT INTO Store (StoreID, District, Address) VALUES (?, ?, ?)", (shop_data[0], shop_data[1], shop_data[2]))

# Загрузка данных в таблицу "Товар" (unchanged)
with open(product, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    header = next(reader, None)
    if header:
        print(f"Header of 'Product' file: {header}")
    for row in reader:
        if not row:
            continue
        try:
            row[4] = int(row[4])
        except ValueError:
            row[4] = 0 # Set to 0 if conversion fails
        try:
            row[5] = float(row[5])
        except ValueError:
            row[5] = 0.0 # Set to 0.0 if conversion fails
        cursor.execute("INSERT INTO Product (Article, Department, ProductName, UnitOfMeasure, QuantityPerPackage, PricePerPackage) VALUES (?, ?, ?, ?, ?, ?)", row)

# Загрузка данных в таблицу "GoodsMovement" (unchanged)
with open(move_goods, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if not row or len(row) < 6:
            continue
        try:
            row[0] = int(row[0])
        except ValueError:
            continue # skip row if OperationID is invalid
        day, month, year = row[1].split('.')
        row[1] = f"{year}-{month}-{day}"
        row[4] = int(row[4])
        cursor.execute("INSERT INTO GoodsMovement (OperationID, Date, StoreID, Article, PackageQuantity, OperationType) VALUES (?, ?, ?, ?, ?, ?)", row)

connection.commit()
connection.close()


connection = sqlite3.connect('base.db')
cursor = connection.cursor()

answer = cursor.execute("""
SELECT CAST(SUM(CAST(REPLACE(Product.QuantityPerPackage, ',', '.') AS REAL) * GoodsMovement.PackageQuantity) / 1000 AS INTEGER)
FROM GoodsMovement
JOIN Product ON GoodsMovement.Article = Product.Article
JOIN Store ON GoodsMovement.StoreID = Store.StoreID
WHERE Product.ProductName LIKE '%Шампунь%'
  AND Store.Address LIKE '%Тургеневская%'
  AND GoodsMovement.OperationType = 'Продажа'
  AND STRFTIME('%Y-%m-%d', Date) BETWEEN '2023-09-07' AND '2023-09-22'
""")
integer_answer = answer.fetchone()[0]


print(integer_answer)


connection.close()