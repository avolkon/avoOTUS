"""
Домашнее задание: Пишем классы и плодим наследников.
Пакет с реализацией транспортных средств и исключений.
"""

# Импортируем модули, чтобы они были доступны при импорте пакета
from . import base
from . import car
from . import engine
from . import exceptions
from . import plane

# Явно указываем, какие имена будут доступны при импорте *
__all__ = [
    "base",      # Базовый класс Vehicle
    "car",       # Класс Car
    "engine",    # Датакласс Engine
    "exceptions", # Пользовательские исключения
    "plane",     # Класс Plane
]
