import sqlite3
import sys


def init_db():
    conn = sqlite3.connect('referrals.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        callback TEXT NOT NULL UNIQUE,
        content TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def show_all():
    conn = sqlite3.connect('referrals.db')
    conn.row_factory = sqlite3.Row
    refs = conn.execute('SELECT * FROM referrals').fetchall()
    conn.close()

    print("\n📋 Список рефералок:")
    for ref in refs:
        print(f"{ref['id']}: {ref['name']} (Callback: {ref['callback']})")
    return bool(refs)


def add_referral():
    print("\n➕ Добавление рефералки")
    name = input("Название: ")
    callback = input("Callback (например REF_TINKOFF): ")

    print("\nВведите текст (Ctrl+D для сохранения):")
    content = sys.stdin.read().strip()

    conn = sqlite3.connect('referrals.db')
    try:
        conn.execute('INSERT INTO referrals (name, callback, content) VALUES (?, ?, ?)',
                     (name, callback, content))
        conn.commit()
        print("✅ Успешно добавлено!")
    except sqlite3.IntegrityError:
        print("❌ Ошибка: такой callback уже существует")
    finally:
        conn.close()


def edit_referral():
    if not show_all():
        return

    ref_id = input("\n✏️ Введите ID для редактирования: ")

    conn = sqlite3.connect('referrals.db')
    conn.row_factory = sqlite3.Row
    ref = conn.execute('SELECT * FROM referrals WHERE id = ?', (ref_id,)).fetchone()
    conn.close()

    if not ref:
        print("❌ Рефералка не найдена!")
        return

    print(f"\nРедактирование: {ref['name']}")
    new_name = input(f"Название [{ref['name']}]: ") or ref['name']
    new_callback = input(f"Callback [{ref['callback']}]: ") or ref['callback']

    print("\nТекущий текст:")
    print(ref['content'])
    print("\nВведите новый текст (Ctrl+D для сохранения):")
    new_content = sys.stdin.read().strip() or ref['content']

    conn = sqlite3.connect('referrals.db')
    try:
        conn.execute('''
        UPDATE referrals 
        SET name=?, callback=?, content=?
        WHERE id=?
        ''', (new_name, new_callback, new_content, ref_id))
        conn.commit()
        print("✅ Успешно обновлено!")
    except sqlite3.IntegrityError:
        print("❌ Ошибка: такой callback уже существует")
    finally:
        conn.close()


def delete_referral():
    if not show_all():
        return

    ref_id = input("\n🗑️ Введите ID для удаления: ")

    conn = sqlite3.connect('referrals.db')
    cur = conn.execute('DELETE FROM referrals WHERE id = ?', (ref_id,))
    conn.commit()
    conn.close()

    if cur.rowcount > 0:
        print("✅ Успешно удалено!")
    else:
        print("❌ Рефералка не найдена")


def main():
    init_db()
    while True:
        print("\n🔧 Редактор рефералок")
        print("1. Показать все")
        print("2. Добавить")
        print("3. Редактировать")
        print("4. Удалить")
        print("5. Выйти")

        choice = input("> ")

        if choice == "1":
            show_all()
        elif choice == "2":
            add_referral()
        elif choice == "3":
            edit_referral()
        elif choice == "4":
            delete_referral()
        elif choice == "5":
            break
        else:
            print("❌ Неверный ввод")


if __name__ == "__main__":
    main()