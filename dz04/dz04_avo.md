# Проектирование иерархии классов для работы с медиа-файлами

## 1. Анализ предметной области

### Основные сущности:
- **Базовый файл** — общие свойства и методы для всех типов файлов
- **Медиа-файл** — расширяет базовый, добавляет медиа-специфичные атрибуты
- **Аудио, Видео, Фото** — конкретные типы с уникальными метаданными
- **Хранилище** — абстракция над местом хранения (локальное, S3, облако)

### Ключевые требования:
- Общие атрибуты: имя, размер, дата создания, владелец, путь
- Типоспецифичные метаданные
- Поддержка 2 разных типов хранилищ
- Возможность расширения (новые типы файлов, новые хранилища)

---

## 2. Базовая иерархия классов

# Классы для работы с медиа-файлами

```python
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List


class FileStatus(Enum):
    """Статус файла в системе"""
    ACTIVE = "active"
    DELETED = "deleted"
    SYNCING = "syncing"
    ERROR = "error"


class BaseFile(ABC):
    """
    Базовый класс для всех типов файлов.
    Содержит общие атрибуты и методы.
    """
    
    def __init__(self, name: str, owner: str, size: int = 0):
        """
        Инициализация базового файла.
        
        Args:
            name: Имя файла
            owner: Владелец файла
            size: Размер в байтах
        """
        self.name = name
        self.owner = owner
        self.size = size
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.status = FileStatus.ACTIVE
        self.storage_path: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
    
    def update(self, **kwargs):
        """Обновление атрибутов файла"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.modified_at = datetime.now()
        print(f"Файл {self.name} обновлен")
    
    def delete(self):
        """Удаление файла (мягкое удаление)"""
        self.status = FileStatus.DELETED
        self.modified_at = datetime.now()
        print(f"Файл {self.name} помечен как удаленный")
    
    def get_info(self) -> Dict[str, Any]:
        """Получение полной информации о файле"""
        return {
            'name': self.name,
            'owner': self.owner,
            'size': self.size,
            'created': self.created_at.isoformat(),
            'modified': self.modified_at.isoformat(),
            'status': self.status.value,
            'type': self.__class__.__name__,
            'storage_path': self.storage_path,
            'metadata': self.metadata
        }
    
    @abstractmethod
    def convert(self, target_format: str) -> 'BaseFile':
        """
        Конвертация файла в другой формат.
        Должен быть реализован в дочерних классах.
        """
        pass
    
    @abstractmethod
    def extract_features(self) -> Dict[str, Any]:
        """
        Извлечение характеристик из файла.
        Должен быть реализован в дочерних классах.
        """
        pass


class AudioFile(BaseFile):
    """Класс для аудио-файлов с дополнительными аудио-атрибутами"""
    
    def __init__(self, name: str, owner: str, duration: float = 0, 
                 artist: str = "", album: str = "", **kwargs):
        super().__init__(name, owner, **kwargs)
        self.duration = duration  # длительность в секундах
        self.artist = artist
        self.album = album
        self.bitrate: Optional[int] = None
        self.sample_rate: Optional[int] = None
        self.format = name.split('.')[-1] if '.' in name else ''
    
    def convert(self, target_format: str) -> 'AudioFile':
        """
        Создание копии аудио-файла в другом формате.
        
        Args:
            target_format: Целевой формат (mp3, wav, flac)
            
        Returns:
            Новый аудио-файл в целевом формате
        """
        # Создаем новое имя с целевым расширением
        base_name = self.name.rsplit('.', 1)[0] if '.' in self.name else self.name
        new_name = f"{base_name}.{target_format}"
        
        # Создаем новый файл с теми же метаданными
        new_file = AudioFile(
            name=new_name,
            owner=self.owner,
            duration=self.duration,
            artist=self.artist,
            album=self.album,
            size=0  # размер будет рассчитан после конвертации
        )
        
        print(f"Конвертация {self.name} в {target_format} -> {new_name}")
        return new_file
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение аудио-характеристик"""
        return {
            'duration': self.duration,
            'artist': self.artist,
            'album': self.album,
            'bitrate': self.bitrate,
            'sample_rate': self.sample_rate,
            'format': self.format
        }
    
    def play(self):
        """Демонстрация дополнительного действия"""
        print(f"Воспроизведение {self.name} (артист: {self.artist})")


class VideoFile(BaseFile):
    """Класс для видео-файлов с дополнительными видео-атрибутами"""
    
    def __init__(self, name: str, owner: str, duration: float = 0,
                 width: int = 1920, height: int = 1080, **kwargs):
        super().__init__(name, owner, **kwargs)
        self.duration = duration
        self.width = width
        self.height = height
        self.fps: Optional[float] = None
        self.video_codec: Optional[str] = None
        self.audio_codec: Optional[str] = None
        self.format = name.split('.')[-1] if '.' in name else ''
    
    def convert(self, target_format: str) -> 'VideoFile':
        """Конвертация видео в другой формат"""
        base_name = self.name.rsplit('.', 1)[0] if '.' in self.name else self.name
        new_name = f"{base_name}.{target_format}"
        
        new_file = VideoFile(
            name=new_name,
            owner=self.owner,
            duration=self.duration,
            width=self.width,
            height=self.height,
            size=0
        )
        
        print(f"Конвертация {self.name} в {target_format} -> {new_name}")
        return new_file
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение видео-характеристик"""
        return {
            'duration': self.duration,
            'resolution': f"{self.width}x{self.height}",
            'fps': self.fps,
            'video_codec': self.video_codec,
            'audio_codec': self.audio_codec,
            'format': self.format
        }
    
    def take_screenshot(self, time_seconds: float) -> 'ImageFile':
        """Создание скриншота из видео (дополнительное действие)"""
        screenshot_name = f"screenshot_{self.name}_{time_seconds}s.jpg"
        screenshot = ImageFile(
            name=screenshot_name,
            owner=self.owner,
            width=self.width,
            height=self.height
        )
        print(f"Создание скриншота из {self.name} на {time_seconds} секунде")
        return screenshot


class ImageFile(BaseFile):
    """Класс для изображений с дополнительными атрибутами"""
    
    def __init__(self, name: str, owner: str, width: int = 800, 
                 height: int = 600, **kwargs):
        super().__init__(name, owner, **kwargs)
        self.width = width
        self.height = height
        self.color_space: Optional[str] = None
        self.camera_model: Optional[str] = None
        self.format = name.split('.')[-1] if '.' in name else ''
    
    def convert(self, target_format: str) -> 'ImageFile':
        """Конвертация изображения в другой формат"""
        base_name = self.name.rsplit('.', 1)[0] if '.' in self.name else self.name
        new_name = f"{base_name}.{target_format}"
        
        new_file = ImageFile(
            name=new_name,
            owner=self.owner,
            width=self.width,
            height=self.height,
            size=0
        )
        
        print(f"Конвертация {self.name} в {target_format} -> {new_name}")
        return new_file
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение характеристик изображения"""
        return {
            'resolution': f"{self.width}x{self.height}",
            'color_space': self.color_space,
            'camera': self.camera_model,
            'format': self.format
        }
    
    def resize(self, new_width: int, new_height: int) -> 'ImageFile':
        """Изменение размера изображения (дополнительное действие)"""
        resized_name = f"resized_{self.width}x{self.height}_to_{new_width}x{new_height}_{self.name}"
        resized = ImageFile(
            name=resized_name,
            owner=self.owner,
            width=new_width,
            height=new_height
        )
        print(f"Изменение размера {self.name} с {self.width}x{self.height} на {new_width}x{new_height}")
        return resized


class StorageBackend(ABC):
    """
    Абстрактный базовый класс для различных типов хранилищ.
    Определяет интерфейс для работы с файлами в удаленных хранилищах.
    """
    
    @abstractmethod
    def upload(self, file: BaseFile, data: bytes) -> bool:
        """Загрузка файла в хранилище"""
        pass
    
    @abstractmethod
    def download(self, file: BaseFile) -> bytes:
        """Скачивание файла из хранилища"""
        pass
    
    @abstractmethod
    def delete(self, file: BaseFile) -> bool:
        """Удаление файла из хранилища"""
        pass
    
    @abstractmethod
    def list_files(self, path: str = "") -> List[str]:
        """Получение списка файлов в хранилище"""
        pass
    
    @abstractmethod
    def get_url(self, file: BaseFile) -> str:
        """Получение URL для доступа к файлу"""
        pass


class LocalStorage(StorageBackend):
    """Реализация для локального хранилища (файловая система)"""
    
    def __init__(self, base_path: str = "./storage"):
        self.base_path = base_path
        print(f"Инициализировано локальное хранилище: {base_path}")
    
    def upload(self, file: BaseFile, data: bytes) -> bool:
        """Сохранение файла в локальной файловой системе"""
        file.storage_path = f"{self.base_path}/{file.name}"
        print(f"Загрузка {file.name} в локальное хранилище: {file.storage_path}")
        # Здесь была бы реальная запись на диск
        return True
    
    def download(self, file: BaseFile) -> bytes:
        """Чтение файла из локальной файловой системы"""
        print(f"Скачивание {file.name} из локального хранилища")
        # Здесь было бы реальное чтение с диска
        return b"dummy data"
    
    def delete(self, file: BaseFile) -> bool:
        """Удаление файла из локальной файловой системы"""
        print(f"Удаление {file.name} из локального хранилища")
        file.storage_path = None
        return True
    
    def list_files(self, path: str = "") -> List[str]:
        """Получение списка локальных файлов"""
        print(f"Получение списка файлов из {self.base_path}/{path}")
        return ["file1.mp3", "file2.mp4", "image.jpg"]
    
    def get_url(self, file: BaseFile) -> str:
        """Получение локального пути как URL"""
        return f"file://{self.base_path}/{file.name}"


class S3Storage(StorageBackend):
    """Реализация для S3-совместимых хранилищ (AWS S3, MinIO, Yandex Object Storage)"""
    
    def __init__(self, bucket_name: str, endpoint: str = "https://s3.amazonaws.com",
                 access_key: str = "", secret_key: str = ""):
        """
        Инициализация S3 хранилища.
        
        Args:
            bucket_name: Имя бакета
            endpoint: URL эндпоинта S3
            access_key: Ключ доступа
            secret_key: Секретный ключ
        """
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        print(f"Инициализировано S3 хранилище: {bucket_name} на {endpoint}")
    
    def upload(self, file: BaseFile, data: bytes) -> bool:
        """Загрузка файла в S3 бакет"""
        s3_path = f"s3://{self.bucket_name}/{file.name}"
        file.storage_path = s3_path
        print(f"Загрузка {file.name} в S3: {s3_path}")
        # Здесь был бы реальный upload в S3
        return True
    
    def download(self, file: BaseFile) -> bytes:
        """Скачивание файла из S3"""
        print(f"Скачивание {file.name} из S3 бакета {self.bucket_name}")
        # Здесь было бы реальное скачивание из S3
        return b"dummy data"
    
    def delete(self, file: BaseFile) -> bool:
        """Удаление файла из S3"""
        print(f"Удаление {file.name} из S3 бакета {self.bucket_name}")
        file.storage_path = None
        return True
    
    def list_files(self, path: str = "") -> List[str]:
        """Получение списка файлов в S3 бакете"""
        print(f"Получение списка файлов из s3://{self.bucket_name}/{path}")
        return ["song.mp3", "video.mp4", "photo.jpg"]
    
    def get_url(self, file: BaseFile) -> str:
        """Генерация прямого URL для доступа к файлу в S3"""
        return f"{self.endpoint}/{self.bucket_name}/{file.name}"
    
    def generate_presigned_url(self, file: BaseFile, expires_in: int = 3600) -> str:
        """Генерация временной ссылки на файл (дополнительный метод для S3)"""
        print(f"Генерация временной ссылки для {file.name} (действительна {expires_in} сек)")
        return f"{self.endpoint}/{self.bucket_name}/{file.name}?token=temp_token"


class CloudStorage(StorageBackend):
    """Реализация для облачных хранилищ (Google Drive, Dropbox, OneDrive)"""
    
    def __init__(self, provider: str, credentials: Dict[str, str]):
        """
        Инициализация облачного хранилища.
        
        Args:
            provider: Название провайдера (google_drive, dropbox, onedrive)
            credentials: Данные аутентификации
        """
        self.provider = provider
        self.credentials = credentials
        print(f"Инициализировано облачное хранилище: {provider}")
    
    def upload(self, file: BaseFile, data: bytes) -> bool:
        """Загрузка файла в облако"""
        cloud_path = f"{self.provider}://{file.name}"
        file.storage_path = cloud_path
        print(f"Загрузка {file.name} в {self.provider}")
        # Здесь был бы реальный upload в облако
        return True
    
    def download(self, file: BaseFile) -> bytes:
        """Скачивание файла из облака"""
        print(f"Скачивание {file.name} из {self.provider}")
        return b"dummy data"
    
    def delete(self, file: BaseFile) -> bool:
        """Удаление файла из облака"""
        print(f"Удаление {file.name} из {self.provider}")
        file.storage_path = None
        return True
    
    def list_files(self, path: str = "") -> List[str]:
        """Получение списка файлов в облаке"""
        print(f"Получение списка файлов из {self.provider}/{path}")
        return ["document.pdf", "image.png", "audio.mp3"]
    
    def get_url(self, file: BaseFile) -> str:
        """Получение ссылки на файл в облаке"""
        return f"https://{self.provider}.com/share/{file.name}"
    
    def share(self, file: BaseFile, email: str) -> str:
        """Расшаривание файла (дополнительный метод для облака)"""
        print(f"Открыт доступ к {file.name} для {email}")
        return self.get_url(file)


# =====================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# =====================================================================

def demo_media_files():
    """Демонстрация работы с медиа-файлами"""
    print("\n=== ДЕМОНСТРАЦИЯ РАБОТЫ С МЕДИА-ФАЙЛАМИ ===\n")
    
    # 1. СОЗДАНИЕ ФАЙЛОВ
    print("--- СОЗДАНИЕ ФАЙЛОВ ---")
    # Создаем аудио-файл
    song = AudioFile(
        name="summer_song.mp3",
        owner="Анна",
        duration=210.5,
        artist="Земфира",
        album="Прости меня моя любовь",
        size=5242880  # 5 MB
    )
    print(f"✓ Создан аудио-файл: {song.name}")
    
    # Создаем видео-файл
    video = VideoFile(
        name="vacation.mp4",
        owner="Анна",
        duration=3600,
        width=1920,
        height=1080,
        size=157286400  # 150 MB
    )
    print(f"✓ Создан видео-файл: {video.name}")
    
    # Создаем изображение
    photo = ImageFile(
        name="holiday.jpg",
        owner="Петр",
        width=4032,
        height=3024,
        camera_model="iPhone 13",
        size=4194304  # 4 MB
    )
    print(f"✓ Создано изображение: {photo.name}\n")
    
    # 2. ПОЛУЧЕНИЕ ИНФОРМАЦИИ
    print("--- ИНФОРМАЦИЯ О ФАЙЛАХ ---")
    song_info = song.get_info()
    print(f"Аудио-файл: {song_info['name']}")
    print(f"  Владелец: {song_info['owner']}")
    print(f"  Размер: {song_info['size']} байт")
    print(f"  Тип: {song_info['type']}")
    
    # Извлечение характеристик
    features = song.extract_features()
    print(f"  Характеристики: {features}\n")
    
    # 3. ДЕЙСТВИЯ С ФАЙЛАМИ
    print("--- ДЕЙСТВИЯ С ФАЙЛАМИ ---")
    # Конвертация
    converted = song.convert("wav")
    print(f"✓ Результат конвертации: {converted.name}")
    
    # Изменение размера изображения
    resized = photo.resize(1920, 1080)
    print(f"✓ Результат изменения размера: {resized.name}")
    
    # Создание скриншота из видео
    screenshot = video.take_screenshot(120)
    print(f"✓ Создан скриншот: {screenshot.name}\n")
    
    # 4. ОБНОВЛЕНИЕ ФАЙЛА
    print("--- ОБНОВЛЕНИЕ ФАЙЛА ---")
    song.update(artist="Земфира Рамазанова", bitrate=320)
    print(f"✓ Аудио-файл обновлен\n")
    
    # 5. УДАЛЕНИЕ ФАЙЛА
    print("--- УДАЛЕНИЕ ФАЙЛА ---")
    video.delete()
    print(f"✓ Видео-файл помечен как удаленный\n")


def demo_storages():
    """Демонстрация работы с различными хранилищами"""
    print("\n=== ДЕМОНСТРАЦИЯ РАБОТЫ С ХРАНИЛИЩАМИ ===\n")
    
    # Создаем тестовый файл
    test_file = AudioFile(
        name="test_song.mp3",
        owner="Тест",
        artist="Test Artist",
        size=1024
    )
    
    # 1. ЛОКАЛЬНОЕ ХРАНИЛИЩЕ
    print("--- ЛОКАЛЬНОЕ ХРАНИЛИЩЕ ---")
    local = LocalStorage(base_path="/media/music")
    
    # Загрузка
    local.upload(test_file, b"audio data")
    # Скачивание
    data = local.download(test_file)
    # Получение URL
    url = local.get_url(test_file)
    print(f"  URL: {url}")
    # Список файлов
    files = local.list_files()
    print(f"  Файлы: {files}")
    # Удаление
    local.delete(test_file)
    print()
    
    # 2. S3 ХРАНИЛИЩЕ
    print("--- S3 ХРАНИЛИЩЕ ---")
    s3 = S3Storage(
        bucket_name="media-bucket",
        endpoint="https://s3.yandex.net",
        access_key="YCA...",
        secret_key="..."
    )
    
    # Загрузка
    s3.upload(test_file, b"audio data")
    # Скачивание
    data = s3.download(test_file)
    # Получение URL
    url = s3.get_url(test_file)
    print(f"  URL: {url}")
    # Временная ссылка
    temp_url = s3.generate_presigned_url(test_file, expires_in=3600)
    print(f"  Временная ссылка: {temp_url}")
    # Удаление
    s3.delete(test_file)
    print()
    
    # 3. ОБЛАЧНОЕ ХРАНИЛИЩЕ
    print("--- ОБЛАЧНОЕ ХРАНИЛИЩЕ (Google Drive) ---")
    cloud = CloudStorage(
        provider="google_drive",
        credentials={"token": "ya29...", "refresh_token": "1//..."}
    )
    
    # Загрузка
    cloud.upload(test_file, b"audio data")
    # Скачивание
    data = cloud.download(test_file)
    # Расшаривание
    share_link = cloud.share(test_file, "user@example.com")
    print(f"  Ссылка для общего доступа: {share_link}")
    # Удаление
    cloud.delete(test_file)


def demo_complete_scenario():
    """Полный сценарий использования: создание, обработка и сохранение в разные хранилища"""
    print("\n=== ПОЛНЫЙ СЦЕНАРИЙ РАБОТЫ ===\n")
    
    # 1. СОЗДАНИЕ МЕДИА-ФАЙЛОВ
    print("ШАГ 1: Создание медиа-файлов")
    podcast = AudioFile(
        name="interview.mp3",
        owner="Радио Ведущий",
        duration=1800,
        artist="Гость студии",
        bitrate=192
    )
    
    cover = ImageFile(
        name="podcast_cover.jpg",
        owner="Радио Ведущий",
        width=3000,
        height=3000
    )
    print(f"✓ Созданы файлы: {podcast.name}, {cover.name}\n")
    
    # 2. ОБРАБОТКА (извлечение характеристик, конвертация)
    print("ШАГ 2: Обработка файлов")
    # Извлекаем характеристики аудио
    audio_features = podcast.extract_features()
    print(f"✓ Характеристики аудио: {audio_features}")
    
    # Конвертируем изображение
    small_cover = cover.resize(500, 500)
    print(f"✓ Создана уменьшенная копия обложки: {small_cover.name}\n")
    
    # 3. СОХРАНЕНИЕ В РАЗНЫЕ ХРАНИЛИЩА
    print("ШАГ 3: Сохранение в разные хранилища")
    
    # Локальное хранилище
    local_storage = LocalStorage()
    local_storage.upload(podcast, b"podcast audio data")
    
    # S3 хранилище для бэкапа
    s3_storage = S3Storage(
        bucket_name="podcast-backup",
        endpoint="https://s3.amazonaws.com"
    )
    s3_storage.upload(podcast, b"podcast audio data")
    
    # Облачное хранилище для обложек
    cloud_storage = CloudStorage(
        provider="google_drive",
        credentials={"token": "user_token"}
    )
    cloud_storage.upload(cover, b"cover image data")
    
    # 4. ПОЛУЧЕНИЕ ДОСТУПА К ФАЙЛАМ
    print("\nШАГ 4: Получение ссылок для доступа")
    local_url = local_storage.get_url(podcast)
    s3_url = s3_storage.get_url(podcast)
    cloud_url = cloud_storage.get_url(cover)
    
    print(f"✓ Локальный доступ: {local_url}")
    print(f"✓ S3 доступ: {s3_url}")
    print(f"✓ Облачный доступ: {cloud_url}")
    
    # 5. УДАЛЕНИЕ (если нужно)
    print("\nШАГ 5: Очистка")
    # Удаляем из локального хранилища
    local_storage.delete(podcast)
    print("✓ Локальная копия удалена")


if __name__ == "__main__":
    """Запуск всех демонстраций"""
    demo_media_files()
    demo_storages()
    demo_complete_scenario()
```

## Структура решения:

### 1. **Классы для медиа-файлов**
- `BaseFile` — абстрактный базовый класс
- `AudioFile` — для аудио
- `VideoFile` — для видео  
- `ImageFile` — для фото

### 2. **Примеры использования**
- Создание файлов
- Обновление (метод `update`)
- Удаление (метод `delete`)
- Действия: конвертация (`convert`), извлечение характеристик (`extract_features`), воспроизведение, изменение размера, создание скриншотов

### 3. **Классы для удаленных хранилищ**
- `StorageBackend` — абстрактный базовый класс
- `LocalStorage` — локальная файловая система
- `S3Storage` — S3-совместимые хранилища
- `CloudStorage` — облачные хранилища (Google Drive, Dropbox и др.)

### 4. **Солько кода потребуется дописать при добавлении новых типов файлов и хранилищ**

## Анализ расширяемости кода

### 1. Добавление нового типа файлов (например, `DocumentFile`)

**Что нужно сделать:**

```python
class DocumentFile(BaseFile):
    """Новый тип файла - документ"""
    
    def __init__(self, name: str, owner: str, pages: int = 0, **kwargs):
        super().__init__(name, owner, **kwargs)
        self.pages = pages
        self.author = kwargs.get('author', '')
        self.format = name.split('.')[-1] if '.' in name else ''
    
    def convert(self, target_format: str) -> 'DocumentFile':
        """Конвертация документа (pdf -> docx и т.д.)"""
        base_name = self.name.rsplit('.', 1)[0] if '.' in self.name else self.name
        new_name = f"{base_name}.{target_format}"
        new_file = DocumentFile(
            name=new_name,
            owner=self.owner,
            pages=self.pages,
            author=self.author
        )
        print(f"Конвертация {self.name} в {target_format}")
        return new_file
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение характеристик документа"""
        return {
            'pages': self.pages,
            'author': self.author,
            'format': self.format
        }
    
    def get_word_count(self) -> int:
        """Специфичный метод для документов"""
        print(f"Подсчет слов в {self.name}")
        return 0
```

**Итог:** 
- ✅ Новый класс = **20-30 строк**
- ✅ Ничего не переписываем в существующих классах
- ✅ Все хранилища работают автоматически (через BaseFile)

---

### 2. Добавление нового типа хранилища (например, `FTPStorage`)

**Что нужно сделать:**

```python
class FTPStorage(StorageBackend):
    """Новый тип хранилища - FTP сервер"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 21):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        print(f"Инициализировано FTP хранилище: {host}")
    
    def upload(self, file: BaseFile, data: bytes) -> bool:
        file.storage_path = f"ftp://{self.host}/{file.name}"
        print(f"Загрузка {file.name} на FTP сервер {self.host}")
        return True
    
    def download(self, file: BaseFile) -> bytes:
        print(f"Скачивание {file.name} с FTP сервера {self.host}")
        return b"dummy data"
    
    def delete(self, file: BaseFile) -> bool:
        print(f"Удаление {file.name} с FTP сервера {self.host}")
        file.storage_path = None
        return True
    
    def list_files(self, path: str = "") -> List[str]:
        print(f"Получение списка файлов с FTP: {self.host}/{path}")
        return ["file1.txt", "file2.pdf"]
    
    def get_url(self, file: BaseFile) -> str:
        return f"ftp://{self.host}/{file.name}"
```

**Итог:**
- ✅ Новый класс = **25-35 строк**
- ✅ Ничего не переписываем в существующих классах
- ✅ Работает со всеми типами файлов автоматически

---

### 3. Сводная таблица расширяемости

| Что добавляем | Где изменения | Объем кода | Влияние на существующий код |
|--------------|---------------|------------|----------------------------|
| **Новый тип файла** (Document, PDF, Excel) | Новый класс-наследник BaseFile | 20-30 строк | 🔵 Ноль - интерфейс уже определен |
| **Новое хранилище** (FTP, WebDAV, Dropbox) | Новый класс-наследник StorageBackend | 25-35 строк | 🔵 Ноль - интерфейс уже определен |
| **Новое действие** для всех файлов | Добавить метод в BaseFile | 1 метод | 🟡 Только в базовый класс |
| **Новое специфичное действие** для аудио | Добавить метод в AudioFile | 1 метод | 🔵 Только в конкретный класс |
| **Изменение логики конвертации** | Переопределить convert в нужном классе | Изменения только в одном методе | 🟢 Локально |

---

### 4. Почему так мало изменений?

**Ключевые решения в архитектуре:**

1. **Абстрактные классы** (`BaseFile`, `StorageBackend`) задают контракт — все наследники обязаны его соблюдать
2. **Полиморфизм** — код работает с `BaseFile` и `StorageBackend`, не зная конкретных типов
3. **Инкапсуляция** — каждый класс отвечает только за свою функциональность
4. **Открытость/закрытость** (OCP) — классы открыты для расширения, закрыты для модификации

**Пример полиморфизма в действии:**
```python
def process_and_save(file: BaseFile, storage: StorageBackend):
    # Неважно, какой это файл (Audio/Video/Image) 
    features = file.extract_features()
    # Неважно, какое хранилище (Local/S3/Cloud)
    storage.upload(file, b"data")
    # Всё работает!
```

---

### 5. Итоговый вывод

**При добавлении нового типа файла:**
- ✅ Пишем **только** новый класс (20-30 строк)
- ✅ Все существующие хранилища работают без изменений
- ✅ Не нужно трогать базовые классы

**При добавлении нового хранилища:**
- ✅ Пишем **только** новый класс (25-35 строк)
- ✅ Все существующие типы файлов работают без изменений
- ✅ Не нужно трогать базовые классы

**Итого:** Архитектура спроектирована так, что расширение происходит **минимальными усилиями** и **без правки существующего кода** — именно этого требует принцип открытости/закрытости (OCP) из SOLID.