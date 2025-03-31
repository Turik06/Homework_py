import sqlite3
import csv
import os

# --- Конфигурация ---
db_name = 'university_results_only.db' # Новое имя файла БД

data_files = {
    'study_level': 'study_level_data.txt',
    'majors': 'majors_data.txt',
    'study_types': 'study_types_data.txt',
    'students': 'students_data.txt',
}

# --- Шаг 1: Создание и заполнение БД 
if os.path.exists(db_name):
    os.remove(db_name)

connection = sqlite3.connect(db_name)
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# -- Создание таблиц --
cursor.execute("""CREATE TABLE IF NOT EXISTS study_level (
    id_study_level INTEGER PRIMARY KEY,
    name TEXT
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS majors (
    id_major INTEGER PRIMARY KEY,
    name TEXT
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS study_types (
    id_type INTEGER PRIMARY KEY,
    name TEXT
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS students (
    id_student INTEGER PRIMARY KEY,
    id_study_level INTEGER,
    id_major INTEGER,
    id_study_type INTEGER,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    average_grade INTEGER,
    FOREIGN KEY (id_study_level) REFERENCES study_level(id_study_level),
    FOREIGN KEY (id_major) REFERENCES majors(id_major),
    FOREIGN KEY (id_study_type) REFERENCES study_types(id_type)
);""")

# -- Загрузка данных --

filename = data_files['study_level']
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
            if len(row) == 2:
                cursor.execute("INSERT INTO study_level (id_study_level, name) VALUES (?, ?)", (int(row[0]), row[1]))

# Загрузка данных в таблицу "majors"
filename = data_files['majors']
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
             if len(row) == 2:
                cursor.execute("INSERT INTO majors (id_major, name) VALUES (?, ?)", (int(row[0]), row[1]))

# Загрузка данных в таблицу "study_types"
filename = data_files['study_types']
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
             if len(row) == 2:
                cursor.execute("INSERT INTO study_types (id_type, name) VALUES (?, ?)", (int(row[0]), row[1]))

# Загрузка данных в таблицу "students"
filename = data_files['students']
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
            if len(row) == 8:
                id_student = int(row[0])
                id_study_level = int(row[1])
                id_major = int(row[2])
                id_study_type = int(row[3])
                average_grade = int(row[7])
                middle_name = row[6] if row[6] else None
                cursor.execute("""
                    INSERT INTO students
                    (id_student, id_study_level, id_major, id_study_type, last_name, first_name, middle_name, average_grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_student, id_study_level, id_major, id_study_type, row[4], row[5], middle_name, average_grade))

connection.commit()



# --- Шаг 2: Выполнение запросов---


# 1. Количество всех студентов
cursor.execute("SELECT COUNT(*) FROM students;")
total = cursor.fetchone()[0]
print(f"# 1.  Общее кол-во студентов: {total}")

# 2. Количество студентов по направлениям

cursor.execute("""
    SELECT m.name, COUNT(s.id_student)
    FROM students s JOIN majors m ON s.id_major = m.id_major
    GROUP BY m.name ORDER BY m.name;
""")
result = cursor.fetchall()
print(f"# 2.  Количество студентов по направлениям: {result}")

# 3. Количество студентов по формам обучения

cursor.execute("""SELECT st.name, COUNT(s.id_student)
    FROM students s JOIN study_types st ON s.id_study_type = st.id_type
    GROUP BY st.name ORDER BY st.name;""")
result = cursor.fetchall()
print(f"# 3.  Количество студентов по формам обучения: {result}")

# 4. Максимальный, минимальный, средний баллы по направлениям
 
cursor.execute("""SELECT m.name, MAX(s.average_grade), MIN(s.average_grade), ROUND(AVG(s.average_grade), 2)
    FROM students s JOIN majors m ON s.id_major = m.id_major
    GROUP BY m.name ORDER BY m.name;""")
result  = cursor.fetchall()
print("# 4. Максимальный, минимальный, средний баллы по направлениям")
[print(f"  - {row[0]}: Макс={row[1]}, Мин={row[2]}, Средний={row[3]}") for row in result]

# 5. Средний балл по направлениям, уровням и формам обучения

cursor.execute("""SELECT m.name, sl.name, st.name, ROUND(AVG(s.average_grade), 2)
    FROM students s
    JOIN majors m ON s.id_major = m.id_major
    JOIN study_level sl ON s.id_study_level = sl.id_study_level
    JOIN study_types st ON s.id_study_type = st.id_type
    GROUP BY m.name, sl.name, st.name ORDER BY m.name, sl.name, st.name;""")
result = cursor.fetchall()
print("# 5. Средний балл по направлениям, уровням и формам обучения")
[print(f"  - Направление: {row[0]}, Уровень: {row[1]}, Форма: {row[2]} -> Средний балл: {row[3]}") for row in result]

# 6. Топ-5 студентов для повышенной стипендии


cursor.execute("""
    SELECT s.last_name, s.first_name, s.middle_name, s.average_grade
    FROM students s 
    JOIN majors m ON s.id_major = m.id_major 
    JOIN study_types st ON s.id_study_type = st.id_type 
    WHERE m.name = 'Applied computer science'
    AND st.name = 'Full-time'               
    ORDER BY s.average_grade DESC             
    LIMIT 5;                                 
""")
top_students = cursor.fetchall()

print("\n# 6.  ТОП-5 студентов для повышенной стипендии:")
for student in top_students:
    print(f"{student[0]} {student[1]} {student[2]} - {student[3]:.2f}")

# 7. Сколько однофамильцев в данной базе? 

cursor.execute("""SELECT last_name,COUNT(*) as count 
               FROM students
               GROUP BY last_name
               HAVING COUNT(*)>1
               ORDER BY count DESC,last_name;
               """)

count_last_name= cursor.fetchall()
total = 0
for row in count_last_name:
        print(f"# 7.   - Фамилия '{row[0]}' встречается {row[1]} раз(а).")
        total += row[1]
print(f"  Всего групп однофамильцев: {len(count_last_name)}")

# 8. Есть ли среди обучающихся полные тезки (совпадают фамилии, имена, отчества)

cursor.execute("""SELECT last_name,first_name,middle_name, COUNT(*) as count
               FROM students
               GROUP BY last_name,first_name,middle_name
               HAVING COUNT(*)>1
               ORDER BY  count DESC,last_name;""")
count_fio = cursor.fetchall()
total =0 
for row in count_fio:
    print(f"# 8.   - ФИО {row[0],row[1],row[2]} встречается {row[3]} раз(а).")
    total+=1
print(f"  Всего групп однофамильцев: {len(count_fio)}")