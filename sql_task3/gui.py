import tkinter as tk
from tkinter import ttk, messagebox
from db_data import get_all_goods, make_purchase, get_sales_report
from datetime import datetime
import sqlite3

def style_widgets():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#ffffff", foreground="#000000",
                    rowheight=25, fieldbackground="#ffffff", font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#e1e1e1")
    style.map("Treeview", background=[('selected', '#cce5ff')])
    style.configure("TButton", font=("Arial", 10))
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TEntry", font=("Arial", 10))

def get_stock_for_goods(goods_id):
    try:
        conn = sqlite3.connect("store.db")
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM goods WHERE id = ?", (goods_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except:
        return None

def load_goods():
    for i in tree.get_children():
        tree.delete(i)
    goods = get_all_goods()
    for row in goods:
        tree.insert("", tk.END, values=row)

def make_purchase_action():
    try:
        id_text = entry_id.get().strip()
        qty_text = entry_qty.get().strip()

        if not id_text or not qty_text:
            raise ValueError("Оба поля должны быть заполнены.")

        goods_id = int(id_text)
        quantity = int(qty_text)

        if quantity <= 0:
            raise ValueError("Количество должно быть положительным.")

        stock = get_stock_for_goods(goods_id)
        if stock is None:
            raise ValueError("Товар с таким ID не найден.")
        if quantity > stock:
            raise ValueError(f"Недостаточно товара на складе. Осталось: {stock} шт.")

        sale_id, sale_date = make_purchase([(goods_id, quantity)])
        messagebox.showinfo("Покупка", f"Покупка успешно оформлена!\nЧек №{sale_id} от {sale_date}")
        load_goods()
        entry_id.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_id.focus()

    except ValueError as ve:
        messagebox.showwarning("Ошибка ввода", str(ve))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при покупке: {e}")

def show_report():
    sale_date = datetime.now().strftime("%Y-%m-%d")
    items, revenue = get_sales_report(sale_date)
    report = f"Отчет за {sale_date}:\n\n"
    report += "Проданные товары:\n"
    for name, total in items:
        report += f"- {name}: {total} шт.\n"
    report += f"\nВыручка: {revenue:.2f} у.е." if revenue else "\nВыручка: 0.00 у.е."
    messagebox.showinfo("Отчет", report)

# --- Интерфейс ---
root = tk.Tk()
root.title("Система учёта продаж")
root.geometry("800x500")
root.configure(bg="#f5f5f5")

style_widgets()

title = tk.Label(root, text="Учёт продаж магазина", font=("Arial", 16, "bold"), bg="#f5f5f5")
title.pack(pady=10)

tree = ttk.Treeview(root, columns=("ID", "Название", "Категория", "Цена", "Остаток"), show="headings", height=10)
for col in ("ID", "Название", "Категория", "Цена", "Остаток"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)
tree.pack(fill=tk.BOTH, padx=20, expand=True)

# --- Блок ввода ---
form_frame = ttk.Frame(root)
form_frame.pack(pady=15)

ttk.Label(form_frame, text="ID товара:").grid(row=0, column=0, padx=5)
entry_id = ttk.Entry(form_frame, width=10)
entry_id.grid(row=0, column=1, padx=5)

ttk.Label(form_frame, text="Количество:").grid(row=0, column=2, padx=5)
entry_qty = ttk.Entry(form_frame, width=10)
entry_qty.grid(row=0, column=3, padx=5)

btn_buy = ttk.Button(form_frame, text="Купить", command=make_purchase_action)
btn_buy.grid(row=0, column=4, padx=10)

# --- Кнопка отчёта ---
btn_report = ttk.Button(root, text="Показать отчёт за сегодня", command=show_report)
btn_report.pack(pady=10)

# --- Загрузка товаров при запуске ---
load_goods()
entry_id.focus()
root.mainloop()
