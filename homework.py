from dataclasses import dataclass
import csv


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.

    Returns:
        get_message: выводит сообщение об тренировке
    """

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
    """Базовый класс тренировки.

    Attributes:
        LEN_STEP: длина шага при ходьбе (измеряется в метрах)
        M_IN_KM: множитель для перевода из метров в километры
        MIN_IN_H: множитель для перевода из минут в часы

    Returns:
        __init__: получаем переменные
        get_distance: рассчитывает среднюю скорость движение в км
        get_mean_speed: Получает среднюю скорость движения
        get_spent_calories: Получает количество затраченных калорий
        show_training_info: Возвращает инфу(сообщение о выполненной тренировке)
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
    ) -> None:
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
        """Получает количество затраченных калорий.

        Raises:
            Exception-1: Исключение, возникающее в случаях, когда наследник
            класса не переопределил метод, который должен был

            Exception-2: Исключение должно подниматься методами
            пользовательских базовых классов как индикатор того,
            что наследникам требуется переопределить такие методы
        """

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Формирует информационное сообщение о выполненной тренировке.

        Raises:
            Exception: функция возращает время, дистанцию(функцию),
            среднюю скорость(функцию), и расход калорий(функцию)
        """

        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег.

    Attributes:
        CALORIES_MEAN_SPEED_MULTIPLIER: множитель при средней скорости
        CALORIES_MEAN_SPEED_SHIFT: ее сдвиг

    Returns:
        get_spent_calories: Получает количество затраченных калорий
    """

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

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
    """Тренировка: спортивная ходьба.

    Attributes:
        CALORIES_WEIGHT_MULTIPLIER: множитель при средней скорости
        CALORIES_MEAN_WALK_SHIFT: просто коэфицент для формулы
        CALORIES_SPEED_HEIGHT_MULTIPLIER: ее сдвиг
        KMH_IN_MSEC: перевод в метры секунды
        CM_IN_M: перевод рост в метрах

    Returns:
        __init__: получаем переменные
        get_spent_calories: Получает количество затраченных калорий
    """

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_MEAN_WALK_SHIFT = 2
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # множитель для перевода в метры секунды
    CM_IN_M = 100

    def __init__(
        self, action: float, duration: float, weight: float, height: float
    ) -> None:
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
    """Тренировка: плавание.

     Attributes:
        CALORIES_MEAN_SPEED_SWIM: множитель при средней скорости
        CALORIES_MEAN_SWIM_MULTIPLIER: просто коэфицент для формулы
        LEN_STEP = 1.38: длина гребка (измеряется в метрах)

    Returns:
        __init__: получаем переменные
        get_mean_speed: Получает среднюю скорость движения
        get_spent_calories: Получает количество затраченных калорий
    """

    CALORIES_MEAN_SPEED_SWIM = 1.1
    CALORIES_MEAN_SWIM_MULTIPLIER = 2
    LEN_STEP = 1.38

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
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
            * self.CALORIES_MEAN_SWIM_MULTIPLIER
            * self.weight
            * self.duration
        )


TYPE_DICT = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: str) -> Training:
    """Читает данные полученные от датчиков.

    Args:
        workout_type: тип тренировки
        data: параметр для инициализации класса
    """

    try:
        return TYPE_DICT[workout_type](*data)
    except (KeyError, TypeError) as err:
        raise Exception(f'Неправильные входные данные: {err}')


def main(training: Training) -> float:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    with open('packag.csv') as reader:
        packages = csv.reader()

    for workout_type, data in packages:
        try:
            main(
                read_package(
                    workout_type, data,
                    list(float)
                ),
            )
        except (KeyError, TypeError, ValueError) as err:
            print(f'Неправильные входные данные: {err}')
