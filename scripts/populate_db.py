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
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARQUET_FILE_PATH = os.path.join(PROJECT_ROOT, "example_dataset.parquet")
MERCHANTS_CSV_PATH = os.path.join(PROJECT_ROOT, "merchants.csv")
CHUNK_SIZE = 100000

# НОВАЯ НАСТРОЙКА: Ограничиваем количество частей для загрузки.
# Установите None, чтобы загрузить все данные.
# Установим 50, чтобы загрузить примерно половину от ~104 частей для ускорения.
MAX_CHUNKS_TO_LOAD = 50

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
    print("   Начинаем загрузку транзакций...")
    start_time = time.time()
    try:
        parquet_file = pq.ParquetFile(PARQUET_FILE_PATH)
        num_row_groups = parquet_file.num_row_groups
        print(f"   Файл Parquet содержит {parquet_file.metadata.num_rows} строк в {num_row_groups} группах.")
        print(f"   Установлен лимит на загрузку: {MAX_CHUNKS_TO_LOAD or 'НЕТ'} частей.")

        total_rows_processed = 0
        for i, batch in enumerate(parquet_file.iter_batches(batch_size=CHUNK_SIZE)):
            # Проверка на ограничение количества частей
            if MAX_CHUNKS_TO_LOAD is not None and i >= MAX_CHUNKS_TO_LOAD:
                print(f"   Достигнут лимит в {MAX_CHUNKS_TO_LOAD} частей. Завершаем загрузку.")
                break

            print(f"   Обрабатываем часть {i+1}...")
            df = batch.to_pandas()

            # Обогащение данных
            decline_chance = 0.15 
            df['authorization_status'] = np.random.choice(
                ['Approved', 'Declined'],
                size=len(df),
                p=[1 - decline_chance, decline_chance]
            )

            # Загрузка в БД
            df.to_sql('transactions', con=engine, if_exists='append', index=False, method='multi')
            total_rows_processed += len(df)

        end_time = time.time()
        print(f"   Загрузка транзакций завершена. Загружено {total_rows_processed} строк.")
        print(f"   Время выполнения: {end_time - start_time:.2f} секунд.")
        return True
    except Exception as e:
        print(f"   !!! Ошибка при загрузке транзакций: {e}")
        return False

if __name__ == "__main__":
    print("--- Запуск скрипта наполнения Базы Данных ---")

    print("   Проверяем и создаем таблицы (если их нет)...")
    Base.metadata.create_all(bind=engine)

    if populate_merchants():
        populate_transactions()
    print("--- Скрипт завершил работу ---")