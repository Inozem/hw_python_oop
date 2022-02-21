from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    OUTPUT_MESSAGE = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.OUTPUT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_count = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_count * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Add method: get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__,
                              self.duration_h,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_DEDUCTIBLE: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEED_DEDUCTIBLE)
                * self.weight_kg / self.M_IN_KM * self.duration_h
                * self.H_IN_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
                + (self.get_mean_speed()**2 // self.height_sm)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight_kg)
                * self.duration_h * self.H_IN_M)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_TERM: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool_m * self.count_pool / self.M_IN_KM
                / self.duration_h)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_TERM)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    activity_types: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                 'RUN': Running,
                                                 'WLK': SportsWalking}

    try:
        sport_res = activity_types[workout_type](*data)
        return sport_res
    except KeyError:
        raise KeyError(f'{workout_type} is not in activity_types')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
