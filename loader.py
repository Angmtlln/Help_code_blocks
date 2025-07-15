import boto3
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from tqdm import tqdm


# Настройка клиента S3
s3 = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)

bucket_name = ''
s3_prefix = 'radiators/'  # Папка в S3
local_dir = './downloads'  # Локальная папка для сохранения

# Создаем локальную папку
os.makedirs(local_dir, exist_ok=True)


def download_file(s3_object):
    s3_key = s3_object['Key']
    local_path = os.path.join(local_dir, os.path.basename(s3_key))

    try:
        s3.download_file(bucket_name, s3_key, local_path)
        return True
    except Exception as e:
        print(f"Ошибка загрузки {s3_key}: {e}")
        return False


# Получаем список всех файлов в папке S3
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
objects = response.get('Contents', [])

# Скачиваем файлы параллельно (10 потоков)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_file, obj) for obj in objects]

    # Прогресс-бар
    successes = 0
    for future in tqdm(as_completed(futures), total=len(objects)):
        if future.result():
            successes += 1

print(f"Успешно скачано: {successes}/{len(objects)} файлов в папку {local_dir}")