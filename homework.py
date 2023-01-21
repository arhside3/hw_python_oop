from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # длина шага при ходьбе
    M_IN_KM = 1000  # перевод из метров в километры
    MIN_IN_H = 60  # перевод из минут в часы

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Рассчитывает среднюю скорость движения в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получает среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получает количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # множитель при средней скорости
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # ее сдвиг

    def get_spent_calories(self) -> float:
        """Получает количество затраченных калорий."""

        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035  # множитель при средней скорости
    CF_WALK = 2  # просто коэфицент для формулы
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029  # ее сдвиг
    KMH_IN_MSEC = 0.278  # перевод в метры секунды
    CM_IN_M = 100  # перевод рост в метрах

    def __init__(
        self, action: int, duration: float, weight: float, height: int
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получает количество затраченных калорий."""

        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_SWIM = 1.1  # множитель при средней скорости
    CF_SW = 2  # просто коэфицент для формулы
    LEN_STEP = 1.38  # длина гребка

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получает среднюю скорость движения."""

        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получает количество затраченных калорий."""

        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SWIM)
            * self.CF_SW
            * self.weight
            * self.duration
        )


TYPE_DICT = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data) -> Training:
    """Читает данные полученные от датчиков."""
    try:
        return TYPE_DICT[workout_type](*data)
    except (KeyError, TypeError):
        print("Ошибка давай по новой")


def main(training: Training):
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
