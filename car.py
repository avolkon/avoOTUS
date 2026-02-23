"""
Модуль с классом Car для представления легкового автомобиля.
"""

from base import Vehicle
from engine import Engine


class Car(Vehicle):
    """
    Класс легкового автомобиля, наследующий базовый класс Vehicle.
    
    Добавляет возможность установки двигателя.
    
    Атрибуты:
        engine (Engine): Экземпляр двигателя, установленного в автомобиль
    """
    
    def __init__(self, weight: float = 0, fuel: float = 0, fuel_consumption: float = 0):
        """
        Инициализация автомобиля.
        
        Args:
            weight: Вес автомобиля
            fuel: Начальное количество топлива
            fuel_consumption: Расход топлива
        """
        # Вызываем конструктор родительского класса для установки базовых атрибутов
        super().__init__(weight, fuel, fuel_consumption)
        # Добавляем новый атрибут для хранения двигателя
        self.engine = None
    
    def set_engine(self, engine: Engine):
        """
        Устанавливает двигатель в автомобиль.
        
        Args:
            engine: Экземпляр класса Engine для установки
        """
        self.engine = engine
