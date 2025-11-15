import pandas as pd
import numpy as np
import sys
import os
import time
import pyarrow.parquet as pq

# Этот трюк позволяет скрипту импортировать модули из папки 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import engine, Base
from app.database import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# --- КОНФИГУРАЦИЯ ---
# Убедитесь, что пути к файлам верные
PARQUET_FILE_PATH = r"C:\Users\mvich\Downloads\Telegram Desktop\example_dataset.parquet"
MERCHANTS_CSV_PATH = "merchants.csv"  # Этот файл нам предоставит Человек C
CHUNK_SIZE = 100000  # Обрабатываем по 100,000 строк за раз для экономии памяти

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_merchants():
    try:
        print(f"1. Читаем названия мерчантов из '{MERCHANTS_CSV_PATH}'...")
        merchants_df = pd.read_csv(MERCHANTS_CSV_PATH)
        # Переименовываем колонки для соответствия БД
        merchants_df = merchants_df.rename(columns={'id': 'id', 'name': 'name'})

        print("   Наполняем таблицу 'merchants'... Это займет пару секунд.")
        merchants_df.to_sql('merchants', con=engine, if_exists='replace', index=False)
        
        print("   Таблица 'merchants' успешно наполнена.")
        return True
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл с мерчантами не найден: '{MERCHANTS_CSV_PATH}'.")
        print("   Пожалуйста, получите этот файл от Человека C и положите в корень проекта.")
        return False
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка при работе с мерчантами: {e}")
        return False

def populate_transactions():
    """Читает Parquet, обогащает данные и наполняет таблицу transactions."""
    try:
        print(f"\n2. Начинаем обработку транзакций из '{PARQUET_FILE_PATH}'...")
        
        with SessionLocal() as session:
            print("   Очищаем старые данные из таблицы 'transactions'...")
            session.execute(text("TRUNCATE TABLE transactions;"))
            session.commit()

        start_time = time.time()
        total_rows = 0
        
        parquet_file = pq.ParquetFile(PARQUET_FILE_PATH)
        for i, batch in enumerate(parquet_file.iter_batches(batch_size=CHUNK_SIZE)):
            print(f"   Обрабатываем часть {i+1}...")
            chunk_df = batch.to_pandas()
            # --- КОНЕЦ ЗАМЕНЫ ---

            # --- Обогащение данных ---
            decline_probability = 0.05  # 5% транзакций будут "Declined"
            chunk_df['authorization_status'] = np.random.choice(
                ['Approved', 'Declined'],
                size=len(chunk_df),
                p=[1 - decline_probability, decline_probability]
            )
            
            # Приводим типы данных в соответствие с БД
            chunk_df['transaction_timestamp'] = pd.to_datetime(chunk_df['transaction_timestamp'])

            # Загружаем обработанную часть в БД
            chunk_df.to_sql('transactions', con=engine, if_exists='append', index=False, method='multi')
            total_rows += len(chunk_df)

        end_time = time.time()
        print("\n   Таблица 'transactions' успешно наполнена.")
        print(f"   Всего обработано и загружено: {total_rows} строк.")
        print(f"   Время выполнения: {end_time - start_time:.2f} секунд.")

    except FileNotFoundError:
        print(f"[ОШИБКА] Parquet-файл не найден: '{PARQUET_FILE_PATH}'")
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка при работе с транзакциями: {e}")

if __name__ == "__main__":
    print("--- Запуск скрипта наполнения Базы Данных ---")

    print("   Проверяем и создаем таблицы (если их нет)...")
    Base.metadata.create_all(bind=engine)

    if populate_merchants():
        populate_transactions()
    print("--- Скрипт завершил работу ---")