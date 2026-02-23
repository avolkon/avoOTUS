# test.py
from homework_05.car import Car
from homework_05.engine import Engine
from homework_05.plane import Plane

def main():
    # Тест автомобиля
    print("ТЕСТ АВТОМОБИЛЯ")
    car = Car(weight=1500, fuel=50, fuel_consumption=0.1)
    engine = Engine(volume=2.0, pistons=4)
    car.set_engine(engine)
    
    car.start()
    print(f"Двигатель запущен: {car.started}")
    
    car.move(100)
    print(f"После поездки топливо: {car.fuel}")
    
    # Тест самолета
    print("\nТЕСТ САМОЛЕТА")
    plane = Plane(weight=5000, fuel=1000, fuel_consumption=5, max_cargo=2000)
    plane.load_cargo(800)
    print(f"Груз на борту: {plane.cargo}")
    
    unloaded = plane.remove_all_cargo()
    print(f"Снято груза: {unloaded}")

if __name__ == "__main__":
    main()
    