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
- Единый интерфейс для операций CRUD
- Поддержка разных типов хранилищ
- Возможность расширения (новые типы файлов, новые хранилища)

---

## 2. Базовая иерархия классов

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class StorageType(Enum):
    """Типы хранилищ"""
    LOCAL = "local"
    S3 = "s3"
    CLOUD = "cloud"
    REMOTE = "remote"


class FileStatus(Enum):
    """Статусы файла"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    SYNCED = "synced"
    ERROR = "error"


class BaseFile(ABC):
    """
    Абстрактный базовый класс для всех типов файлов.
    Содержит общие атрибуты и методы.
    """
    
    def __init__(self, 
                 name: str,
                 owner: str,
                 storage_type: StorageType = StorageType.LOCAL,
                 **kwargs):
        self.name = name
        self.owner = owner
        self.storage_type = storage_type
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.size: Optional[int] = None
        self.path: Optional[str] = None
        self.status: FileStatus = FileStatus.CREATED
        self.metadata: Dict[str, Any] = {}
        
    @abstractmethod
    def read(self) -> bytes:
        """Чтение содержимого файла"""
        pass
    
    @abstractmethod
    def write(self, data: bytes) -> bool:
        """Запись данных в файл"""
        pass
    
    @abstractmethod
    def delete(self) -> bool:
        """Удаление файла"""
        pass
    
    @abstractmethod
    def move(self, new_path: str) -> bool:
        """Перемещение файла"""
        pass
    
    @abstractmethod
    def copy(self, destination_path: str) -> 'BaseFile':
        """Копирование файла"""
        pass
    
    def update_metadata(self, **kwargs) -> None:
        """Обновление метаданных"""
        self.metadata.update(kwargs)
        self.modified_at = datetime.now()
    
    def get_info(self) -> Dict[str, Any]:
        """Получение информации о файле"""
        return {
            "name": self.name,
            "owner": self.owner,
            "size": self.size,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "status": self.status.value,
            "storage_type": self.storage_type.value,
            "path": self.path,
            "metadata": self.metadata
        }


class MediaFile(BaseFile):
    """
    Базовый класс для медиа-файлов.
    Добавляет общие для медиа атрибуты.
    """
    
    def __init__(self, 
                 name: str,
                 owner: str,
                 duration: Optional[float] = None,
                 **kwargs):
        super().__init__(name, owner, **kwargs)
        self.duration = duration  # в секундах
        self.bitrate: Optional[int] = None
        self.codec: Optional[str] = None
        self.file_format: Optional[str] = None
    
    @abstractmethod
    def convert(self, target_format: str) -> 'MediaFile':
        """Конвертация в другой формат"""
        pass
    
    @abstractmethod
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение признаков из медиа-файла"""
        pass


class AudioFile(MediaFile):
    """
    Класс для аудио-файлов.
    Специфичные метаданные: битрейт, частота дискретизации, etc.
    """
    
    def __init__(self, 
                 name: str,
                 owner: str,
                 **kwargs):
        super().__init__(name, owner, **kwargs)
        self.sample_rate: Optional[int] = None  # Гц
        self.channels: Optional[int] = None  # моно/стерео
        self.artist: Optional[str] = None
        self.album: Optional[str] = None
        self.genre: Optional[str] = None
        self.track_number: Optional[int] = None
        self.year: Optional[int] = None
    
    def read(self) -> bytes:
        """Реализация чтения аудио-файла"""
        # Здесь будет логика чтения
        pass
    
    def write(self, data: bytes) -> bool:
        """Реализация записи аудио-файла"""
        # Здесь будет логика записи
        pass
    
    def delete(self) -> bool:
        """Реализация удаления"""
        # Здесь будет логика удаления
        pass
    
    def move(self, new_path: str) -> bool:
        """Реализация перемещения"""
        # Здесь будет логика перемещения
        pass
    
    def copy(self, destination_path: str) -> 'AudioFile':
        """Реализация копирования"""
        # Здесь будет логика копирования
        pass
    
    def convert(self, target_format: str) -> 'AudioFile':
        """Конвертация аудио в другой формат (mp3 -> wav, etc.)"""
        # Здесь будет логика конвертации
        pass
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение аудио-признаков (MFCC, спектрограмма, etc.)"""
        # Здесь будет логика извлечения признаков
        return {
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "bitrate": self.bitrate,
            "codec": self.codec
        }
    
    def get_id3_tags(self) -> Dict[str, Any]:
        """Получение ID3 тегов"""
        # Здесь будет логика чтения тегов
        pass


class VideoFile(MediaFile):
    """
    Класс для видео-файлов.
    Специфичные метаданные: разрешение, FPS, etc.
    """
    
    def __init__(self, 
                 name: str,
                 owner: str,
                 **kwargs):
        super().__init__(name, owner, **kwargs)
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.fps: Optional[float] = None  # кадры в секунду
        self.aspect_ratio: Optional[str] = None
        self.video_codec: Optional[str] = None
        self.audio_tracks: int = 0
        self.subtitles: bool = False
    
    def read(self) -> bytes:
        pass
    
    def write(self, data: bytes) -> bool:
        pass
    
    def delete(self) -> bool:
        pass
    
    def move(self, new_path: str) -> bool:
        pass
    
    def copy(self, destination_path: str) -> 'VideoFile':
        pass
    
    def convert(self, target_format: str) -> 'VideoFile':
        """Конвертация видео (mp4 -> avi, etc.)"""
        pass
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение видео-признаков (гистограммы, motion vectors, etc.)"""
        return {
            "resolution": f"{self.width}x{self.height}",
            "fps": self.fps,
            "duration": self.duration,
            "video_codec": self.video_codec,
            "audio_tracks": self.audio_tracks
        }
    
    def extract_audio(self) -> AudioFile:
        """Извлечение аудиодорожки из видео"""
        # Здесь будет логика извлечения
        pass
    
    def take_screenshot(self, time_seconds: float) -> 'ImageFile':
        """Создание скриншота из видео"""
        # Здесь будет логика создания скриншота
        pass


class ImageFile(MediaFile):
    """
    Класс для изображений.
    Специфичные метаданные: размер, цветовое пространство, EXIF, etc.
    """
    
    def __init__(self, 
                 name: str,
                 owner: str,
                 **kwargs):
        super().__init__(name, owner, **kwargs)
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.color_space: Optional[str] = None  # RGB, CMYK, etc.
        self.dpi: Optional[int] = None
        self.compression: Optional[str] = None
        self.exif_data: Dict[str, Any] = {}
        self.camera_model: Optional[str] = None
        self.timestamp: Optional[datetime] = None
        self.gps_coordinates: Optional[tuple] = None
    
    def read(self) -> bytes:
        pass
    
    def write(self, data: bytes) -> bool:
        pass
    
    def delete(self) -> bool:
        pass
    
    def move(self, new_path: str) -> bool:
        pass
    
    def copy(self, destination_path: str) -> 'ImageFile':
        pass
    
    def convert(self, target_format: str) -> 'ImageFile':
        """Конвертация изображения (jpg -> png, etc.)"""
        pass
    
    def extract_features(self) -> Dict[str, Any]:
        """Извлечение признаков изображения (гистограммы, ключевые точки, etc.)"""
        return {
            "resolution": f"{self.width}x{self.height}",
            "color_space": self.color_space,
            "has_exif": bool(self.exif_data),
            "camera": self.camera_model
        }
    
    def resize(self, new_width: int, new_height: int) -> 'ImageFile':
        """Изменение размера изображения"""
        # Здесь будет логика изменения размера
        pass
    
    def apply_filter(self, filter_name: str) -> 'ImageFile':
        """Применение фильтра к изображению"""
        # Здесь будет логика применения фильтров
        pass
```

---

## 3. Классы для работы с хранилищами

```python
from abc import ABC, abstractmethod
import os
from pathlib import Path


class StorageBackend(ABC):
    """
    Абстрактный класс для различных типов хранилищ.
    Определяет интерфейс для работы с файлами независимо от места хранения.
    """
    
    @abstractmethod
    def save(self, file: BaseFile, data: bytes) -> bool:
        """Сохранение файла в хранилище"""
        pass
    
    @abstractmethod
    def load(self, file: BaseFile) -> bytes:
        """Загрузка файла из хранилища"""
        pass
    
    @abstractmethod
    def delete(self, file: BaseFile) -> bool:
        """Удаление файла из хранилища"""
        pass
    
    @abstractmethod
    def exists(self, file: BaseFile) -> bool:
        """Проверка существования файла"""
        pass
    
    @abstractmethod
    def get_size(self, file: BaseFile) -> int:
        """Получение размера файла"""
        pass
    
    @abstractmethod
    def list_files(self, path: str) -> list:
        """Список файлов в директории"""
        pass


class LocalStorage(StorageBackend):
    """
    Реализация для локального хранилища.
    Работает с файловой системой.
    """
    
    def __init__(self, base_path: str = "./"):
        self.base_path = Path(base_path)
    
    def save(self, file: BaseFile, data: bytes) -> bool:
        """Сохраняет файл локально"""
        # Здесь будет логика сохранения на диск
        pass
    
    def load(self, file: BaseFile) -> bytes:
        """Загружает файл с диска"""
        # Здесь будет логика загрузки с диска
        pass
    
    def delete(self, file: BaseFile) -> bool:
        """Удаляет локальный файл"""
        # Здесь будет логика удаления
        pass
    
    def exists(self, file: BaseFile) -> bool:
        """Проверяет существование локального файла"""
        return (self.base_path / file.path).exists()
    
    def get_size(self, file: BaseFile) -> int:
        """Получает размер локального файла"""
        return (self.base_path / file.path).stat().st_size
    
    def list_files(self, path: str) -> list:
        """Список файлов в локальной директории"""
        return [str(p) for p in (self.base_path / path).iterdir() if p.is_file()]


class S3Storage(StorageBackend):
    """
    Реализация для S3-совместимых хранилищ.
    Работает с AWS S3, MinIO, etc.
    """
    
    def __init__(self, 
                 bucket_name: str,
                 endpoint_url: Optional[str] = None,
                 access_key: Optional[str] = None,
                 secret_key: Optional[str] = None):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        # Здесь будет инициализация S3 клиента
    
    def save(self, file: BaseFile, data: bytes) -> bool:
        """Сохраняет файл в S3 bucket"""
        # Здесь будет логика загрузки в S3
        pass
    
    def load(self, file: BaseFile) -> bytes:
        """Загружает файл из S3"""
        # Здесь будет логика скачивания из S3
        pass
    
    def delete(self, file: BaseFile) -> bool:
        """Удаляет файл из S3"""
        # Здесь будет логика удаления из S3
        pass
    
    def exists(self, file: BaseFile) -> bool:
        """Проверяет существование файла в S3"""
        # Здесь будет логика проверки в S3
        pass
    
    def get_size(self, file: BaseFile) -> int:
        """Получает размер файла из S3"""
        # Здесь будет логика получения размера из S3
        pass
    
    def list_files(self, path: str) -> list:
        """Список файлов в S3 prefix"""
        # Здесь будет логика листинга S3
        pass
    
    def generate_presigned_url(self, file: BaseFile, expires_in: int = 3600) -> str:
        """Генерирует временную ссылку на файл"""
        # Здесь будет логика генерации presigned URL
        pass


class CloudStorage(StorageBackend):
    """
    Реализация для облачных хранилищ (Google Drive, Dropbox, etc.).
    """
    
    def __init__(self, 
                 provider: str,  # 'google_drive', 'dropbox', 'onedrive'
                 credentials: Dict[str, Any]):
        self.provider = provider
        self.credentials = credentials
        # Здесь будет инициализация API клиента
    
    def save(self, file: BaseFile, data: bytes) -> bool:
        """Сохраняет файл в облако"""
        # Здесь будет логика загрузки в облако
        pass
    
    def load(self, file: BaseFile) -> bytes:
        """Загружает файл из облака"""
        # Здесь будет логика скачивания из облака
        pass
    
    def delete(self, file: BaseFile) -> bool:
        """Удаляет файл из облака"""
        # Здесь будет логика удаления из облака
        pass
    
    def exists(self, file: BaseFile) -> bool:
        """Проверяет существование файла в облаке"""
        # Здесь будет логика проверки в облаке
        pass
    
    def get_size(self, file: BaseFile) -> int:
        """Получает размер файла из облака"""
        # Здесь будет логика получения размера из облака
        pass
    
    def list_files(self, path: str) -> list:
        """Список файлов в облачной директории"""
        # Здесь будет логика листинга в облаке
        pass
    
    def share(self, file: BaseFile, email: str, permission: str = 'read') -> bool:
        """Расшаривает файл в облаке"""
        # Здесь будет логика шаринга
        pass


class StorageFactory:
    """
    Фабрика для создания нужного типа хранилища.
    """
    
    @staticmethod
    def create_storage(storage_type: StorageType, **kwargs) -> StorageBackend:
        if storage_type == StorageType.LOCAL:
            return LocalStorage(**kwargs)
        elif storage_type == StorageType.S3:
            return S3Storage(**kwargs)
        elif storage_type == StorageType.CLOUD:
            return CloudStorage(**kwargs)
        elif storage_type == StorageType.REMOTE:
            # Можно добавить FTP/SSH реализацию
            pass
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
```

---

## 4. Файловый менеджер

```python
class FileManager:
    """
    Класс для управления файлами.
    Координирует работу с разными типами файлов и хранилищ.
    """
    
    def __init__(self):
        self.files: Dict[str, BaseFile] = {}  # path -> file
        self.storages: Dict[StorageType, StorageBackend] = {}
    
    def register_storage(self, storage_type: StorageType, storage: StorageBackend):
        """Регистрирует хранилище"""
        self.storages[storage_type] = storage
    
    def create_file(self, 
                   file_type: str,
                   name: str,
                   owner: str,
                   storage_type: StorageType = StorageType.LOCAL,
                   **kwargs) -> BaseFile:
        """Создает новый файл"""
        if file_type == 'audio':
            file = AudioFile(name, owner, storage_type=storage_type, **kwargs)
        elif file_type == 'video':
            file = VideoFile(name, owner, storage_type=storage_type, **kwargs)
        elif file_type == 'image':
            file = ImageFile(name, owner, storage_type=storage_type, **kwargs)
        else:
            raise ValueError(f"Unknown file type: {file_type}")
        
        self.files[file.path] = file
        return file
    
    def save_file(self, file: BaseFile, data: bytes) -> bool:
        """Сохраняет файл в соответствующее хранилище"""
        storage = self.storages.get(file.storage_type)
        if not storage:
            raise ValueError(f"Storage not registered: {file.storage_type}")
        return storage.save(file, data)
    
    def load_file(self, file: BaseFile) -> bytes:
        """Загружает файл из хранилища"""
        storage = self.storages.get(file.storage_type)
        if not storage:
            raise ValueError(f"Storage not registered: {file.storage_type}")
        return storage.load(file)
    
    def delete_file(self, file: BaseFile) -> bool:
        """Удаляет файл"""
        storage = self.storages.get(file.storage_type)
        if not storage:
            raise ValueError(f"Storage not registered: {file.storage_type}")
        return storage.delete(file)
    
    def move_file(self, file: BaseFile, new_path: str, new_storage: Optional[StorageType] = None) -> bool:
        """Перемещает файл (возможно между хранилищами)"""
        # Логика перемещения
        pass
    
    def copy_file(self, file: BaseFile, destination_path: str) -> BaseFile:
        """Копирует файл"""
        # Логика копирования
        pass
    
    def sync_file(self, file: BaseFile, target_storage: StorageType) -> bool:
        """Синхронизирует файл между хранилищами"""
        # Логика синхронизации
        pass
```

---

## 5. Примеры использования

```python
# Пример 1: Создание и работа с аудио-файлом в локальном хранилище

# Инициализация
file_manager = FileManager()
local_storage = LocalStorage(base_path="/home/user/media")
file_manager.register_storage(StorageType.LOCAL, local_storage)

# Создание аудио-файла
audio = file_manager.create_file(
    file_type='audio',
    name='concert.mp3',
    owner='john_doe',
    duration=180.5,
    artist='The Beatles',
    album='Live',
    sample_rate=44100,
    channels=2
)

# Сохранение файла
with open('local_file.mp3', 'rb') as f:
    data = f.read()
file_manager.save_file(audio, data)

# Обновление метаданных
audio.update_metadata(genre='Rock', year=2023)

# Конвертация в другой формат
wav_audio = audio.convert('wav')

# Получение информации
info = audio.get_info()
print(info)

# Удаление
file_manager.delete_file(audio)
```

```python
# Пример 2: Работа с разными хранилищами

# Настройка S3 хранилища
s3_storage = S3Storage(
    bucket_name='my-media-bucket',
    endpoint_url='https://s3.amazonaws.com',
    access_key='AKIA...',
    secret_key='...'
)
file_manager.register_storage(StorageType.S3, s3_storage)

# Настройка облачного хранилища
cloud_storage = CloudStorage(
    provider='google_drive',
    credentials={'token': '...', 'refresh_token': '...'}
)
file_manager.register_storage(StorageType.CLOUD, cloud_storage)

# Создание видео-файла в S3
video = file_manager.create_file(
    file_type='video',
    name='movie.mp4',
    owner='jane_doe',
    storage_type=StorageType.S3,
    width=1920,
    height=1080,
    fps=30,
    duration=5400
)

# Сохранение в S3
file_manager.save_file(video, video_data)

# Создание скриншота и сохранение в облако
screenshot = video.take_screenshot(time_seconds=120)
screenshot.storage_type = StorageType.CLOUD
file_manager.save_file(screenshot, screenshot_data)

# Синхронизация между хранилищами
file_manager.sync_file(video, StorageType.CLOUD)
```

```python
# Пример 3: Пакетная обработка

class BatchProcessor:
    """Класс для пакетной обработки файлов"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def process_audio_files(self, files: List[AudioFile], operation: str):
        for file in files:
            if operation == 'convert_to_wav':
                result = file.convert('wav')
                self.file_manager.save_file(result, b'')
            elif operation == 'extract_features':
                features = file.extract_features()
                print(f"Features for {file.name}: {features}")
    
    def batch_resize_images(self, images: List[ImageFile], width: int, height: int):
        for img in images:
            resized = img.resize(width, height)
            self.file_manager.save_file(resized, b'')
    
    def generate_report(self, files: List[BaseFile]) -> Dict:
        """Генерирует отчет по файлам"""
        report = {
            'total_files': len(files),
            'total_size': sum(f.size for f in files if f.size),
            'by_type': {},
            'by_owner': {}
        }
        
        for file in files:
            # Сбор статистики
            pass
        
        return report
```

---

## 6. Ключевые принципы проектирования

### SOLID в данной иерархии:

1. **Single Responsibility**:
   - `BaseFile` — только представление файла
   - `StorageBackend` — только операции с хранилищем
   - `FileManager` — только координация

2. **Open/Closed**:
   - Новые типы файлов — наследование от `MediaFile`
   - Новые хранилища — реализация `StorageBackend`
   - Новые операции — методы в конкретных классах

3. **Liskov Substitution**:
   - Любой `MediaFile` можно использовать вместо `BaseFile`
   - Любой `StorageBackend` работает в `FileManager`

4. **Interface Segregation**:
   - Тонкие интерфейсы для каждого типа
   - Специфичные методы только в нужных классах

5. **Dependency Inversion**:
   - `FileManager` зависит от абстракций `StorageBackend`
   - Конкретные файлы зависят от абстрактного хранилища

### Паттерны проектирования:
- **Factory** — `StorageFactory` для создания хранилищ
- **Strategy** — разные стратегии хранения
- **Composite** — иерархия файлов
- **Observer** — отслеживание изменений файлов