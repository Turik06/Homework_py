import sqlite3
from datetime import datetime

DB_NAME = "store.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def insert_sample_goods():
    goods = [
        ("Яблоки", "Фрукты", 0.5, 100),
        ("Молоко", "Молочные продукты", 1.2, 50),
        ("Хлеб", "Выпечка", 0.8, 70)
    ]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO goods (name, category, price, stock) VALUES (?, ?, ?, ?)", goods)
    conn.commit()
    conn.close()

def get_all_goods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, stock FROM goods")
    rows = cursor.fetchall()
    conn.close()
    return rows

def make_purchase(purchase_list):
    conn = get_connection()
    cursor = conn.cursor()
    sale_date = datetime.now().strftime("%Y-%m-%d")
    # Создание нового чека
    cursor.execute("INSERT INTO sales (sale_date) VALUES (?)", (sale_date,))
    sale_id = cursor.lastrowid

    for goods_id, quantity in purchase_list:
        # Проверяем наличие товара на складе
        cursor.execute("SELECT stock, price FROM goods WHERE id = ?", (goods_id,))
        result = cursor.fetchone()
        if result is None:
            continue
        stock, price = result
        if quantity > stock:
            print(f"Товара с id {goods_id} недостаточно на складе.")
            continue
        # Обновление остатка товара
        cursor.execute("UPDATE goods SET stock = stock - ? WHERE id = ?", (quantity, goods_id))
        # Добавление записи в sale_items
        cursor.execute("INSERT INTO sale_items (sale_id, goods_id, quantity) VALUES (?, ?, ?)",
                       (sale_id, goods_id, quantity))
    conn.commit()
    conn.close()
    return sale_id, sale_date

def get_sales_report(sale_date):
    """
    Возвращает количество проданных товаров и выручку за указанную дату.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Количество проданных товаров по каждому типу
    cursor.execute("""
    SELECT g.name, SUM(si.quantity) AS total_sold
    FROM sale_items si
    JOIN sales s ON si.sale_id = s.id
    JOIN goods g ON si.goods_id = g.id
    WHERE s.sale_date = ?
    GROUP BY si.goods_id
    """, (sale_date,))
    items = cursor.fetchall()

    # Выручка за указанную дату
    cursor.execute("""
    SELECT SUM(g.price * si.quantity) AS revenue
    FROM sale_items si
    JOIN sales s ON si.sale_id = s.id
    JOIN goods g ON si.goods_id = g.id
    WHERE s.sale_date = ?
    """, (sale_date,))
    revenue = cursor.fetchone()[0]

    conn.close()
    return items, revenue if revenue else 0

if __name__ == "__main__":
    # Для первоначального заполнения товарами (запустить 1 раз)
    insert_sample_goods()
    print("Пример товаров добавлен в базу.")
