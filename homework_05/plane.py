"""
Модуль с классом Plane для представления самолета.
"""

from homework_05.base import Vehicle
from homework_05.exceptions import CargoOverload


class Plane(Vehicle):
    """
    Класс самолета, наследующий базовый класс Vehicle.
    
    Добавляет возможность перевозки груза с контролем максимальной нагрузки.
    
    Атрибуты:
        cargo (float): Текущий вес груза на борту
        max_cargo (float): Максимально допустимый вес груза
    """
    
    def __init__(self, weight: float = 0, fuel: float = 0, 
                 fuel_consumption: float = 0, max_cargo: float = 0):
        """
        Инициализация самолета.
        
        Args:
            weight: Вес самолета
            fuel: Начальное количество топлива
            fuel_consumption: Расход топлива
            max_cargo: Максимальная грузоподъемность
        """
        # Вызываем конструктор родительского класса
        super().__init__(weight, fuel, fuel_consumption)
        # Устанавливаем специфичные для самолета атрибуты
        self.max_cargo = max_cargo
        self.cargo = 0  # Изначально груза нет
    
    def load_cargo(self, cargo_weight: float):
        """
        Загружает груз на борт самолета.
        
        Проверяет, что после загрузки не будет превышена максимальная грузоподъемность.
        
        Args:
            cargo_weight: Вес груза для загрузки
            
        Raises:
            CargoOverload: Если после загрузки превышен max_cargo
        """
        # Проверяем, не будет ли перегруза после загрузки
        if self.cargo + cargo_weight > self.max_cargo:
            raise CargoOverload(
                f"Невозможно загрузить {cargo_weight}. "
                f"Текущий груз: {self.cargo}, максимум: {self.max_cargo}"
            )
        
        # Добавляем груз
        self.cargo += cargo_weight
    
    def remove_all_cargo(self) -> float:
        """
        Полностью разгружает самолет.
        
        Returns:
            float: Вес груза, который был снят с борта
        """
        # Сохраняем текущий вес груза для возврата
        previous_cargo = self.cargo
        # Обнуляем груз
        self.cargo = 0
        # Возвращаем вес снятого груза
        return previous_cargo
    