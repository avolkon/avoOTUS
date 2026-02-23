"""
Базовый модуль для всех транспортных средств.
Содержит абстрактный класс Vehicle с основной логикой.
"""

from abc import ABC
from exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):
    """
    Базовый класс для всех транспортных средств.
    
    Атрибуты:
        weight (float): Вес транспортного средства
        started (bool): Флаг запущен ли двигатель
        fuel (float): Текущее количество топлива
        fuel_consumption (float): Расход топлива на единицу расстояния
    """
    
    def __init__(self, weight: float = 0, fuel: float = 0, fuel_consumption: float = 0):
        """
        Инициализация транспортного средства.
        
        Args:
            weight: Вес транспортного средства (по умолчанию 0)
            fuel: Начальное количество топлива (по умолчанию 0)
            fuel_consumption: Расход топлива на единицу расстояния (по умолчанию 0)
        """
        self.weight = weight
        self.started = False  # Двигатель изначально заглушен
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption
    
    def start(self):
        """
        Запуск двигателя.
        
        Проверяет наличие топлива и запускает двигатель.
        Если топлива нет, выбрасывает исключение LowFuelError.
        
        Raises:
            LowFuelError: Если количество топлива меньше или равно 0
        """
        if not self.started:  # Проверяем, не запущен ли уже двигатель
            if self.fuel <= 0:  # Проверяем наличие топлива
                raise LowFuelError("Недостаточно топлива для запуска двигателя")
            self.started = True  # Запускаем двигатель
    
    def move(self, distance: float):
        """
        Движение на заданное расстояние.
        
        Проверяет, что топлива достаточно для преодоления дистанции,
        и уменьшает количество топлива.
        
        Args:
            distance: Расстояние, которое нужно преодолеть
            
        Raises:
            NotEnoughFuel: Если топлива недостаточно для преодоления дистанции
        """
        # Расчитываем необходимое количество топлива
        required_fuel = distance * self.fuel_consumption
        
        # Проверяем, что топлива достаточно
        if required_fuel > self.fuel:
            raise NotEnoughFuel(
                f"Недостаточно топлива. Требуется: {required_fuel}, "
                f"доступно: {self.fuel}"
            )
        
        # Уменьшаем количество топлива
        self.fuel -= required_fuel
