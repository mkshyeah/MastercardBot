import pandas as pd

# Если у вас не установлены эти библиотеки, выполните в терминале:
# pip install pandas pyarrow

# --- Укажите здесь путь к вашему .parquet файлу ---
parquet_file_path = r"C:\Users\mvich\Downloads\Telegram Desktop\example_dataset.parquet"

try:
    # Читаем Parquet файл в DataFrame
    df = pd.read_parquet(parquet_file_path)

    # --- Способ 1 (Предпочтительный и быстрый): Показать мне схему и пример ---
    # Этот способ выведет в консоль структуру данных и первые 5 строк.
    # Вы можете просто скопировать этот вывод и отправить мне.
    print("-----------------------------------------")
    print("### Схема данных (Колонки и их типы) ###")
    print("-----------------------------------------")
    df.info()

    print("\n------------------------------------")
    print("### Первые 5 строк датасета ###")
    print("------------------------------------")
    print(df.head())


    # --- Способ 2 (Альтернативный): Конвертация в CSV ---
    # Этот код сконвертирует весь .parquet файл в .csv.
    # Это полезно, если файл не гигантский и вы хотите предоставить все данные.
    csv_output_path = 'converted_dataset.csv'
    # df.to_csv(csv_output_path, index=False)
    # print(f"\n[INFO] Файл был также сконвертирован в: {csv_output_path}")

except FileNotFoundError:
    print(f"[ОШИБКА] Файл не найден по указанному пути: {parquet_file_path}")
except Exception as e:
    print(f"[ОШИБКА] Произошла непредвиденная ошибка: {e}")