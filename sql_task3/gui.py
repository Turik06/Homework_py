import tkinter as tk
from tkinter import messagebox, ttk
from db_data import get_all_goods, make_purchase, get_sales_report

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система учёта продаж")
        self.selected_goods = {}
        self.create_widgets()
        self.load_goods()

    def create_widgets(self):
        # Таблица товаров
        self.tree = ttk.Treeview(self.root, columns=("ID", "Название", "Категория", "Цена", "Остаток"), show="headings")
        for col in ("ID", "Название", "Категория", "Цена", "Остаток"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Форма покупки
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="Введите ID товара и количество через запятую (напр. 1,2)").grid(row=0, column=0)
        self.purchase_entry = tk.Entry(frame, width=30)
        self.purchase_entry.grid(row=1, column=0)
        buy_btn = tk.Button(frame, text="Купить", command=self.purchase)
        buy_btn.grid(row=1, column=1, padx=5)

        # Кнопка отчёта
        report_btn = tk.Button(self.root, text="Отчет за сегодня", command=self.show_report)
        report_btn.pack(pady=5)

    def load_goods(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Загрузка данных товаров
        goods = get_all_goods()
        for row in goods:
            self.tree.insert("", tk.END, values=row)

    def purchase(self):
        data = self.purchase_entry.get().strip()
        if not data:
            messagebox.showwarning("Ошибка", "Введите данные для покупки.")
            return
        try:
            # Ожидается формат: "id,количество" или несколько пар через точку с запятой
            # Например: "1,2; 2,1"
            purchases = []
            entries = data.split(";")
            for entry in entries:
                goods_id, qty = map(int, entry.split(","))
                purchases.append((goods_id, qty))
            sale_id, sale_date = make_purchase(purchases)
            messagebox.showinfo("Покупка", f"Покупка успешно оформлена!\nЧек №{sale_id} от {sale_date}")
            self.load_goods()
            self.purchase_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оформлении покупки: {e}")

    def show_report(self):
        from datetime import datetime
        sale_date = datetime.now().strftime("%Y-%m-%d")
        items, revenue = get_sales_report(sale_date)
        report = f"Отчет за {sale_date}:\n\n"
        report += "Проданные товары:\n"
        for name, total in items:
            report += f"- {name}: {total} шт.\n"
        report += f"\nВыручка: {revenue} у.е."
        messagebox.showinfo("Отчет", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()
