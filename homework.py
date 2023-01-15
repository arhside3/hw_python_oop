class InfoMessage():

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; ',
                f'Длительность: {self.duration} ч.; ',
                f'Дистанция: {self.distance} км; ',
                f'Ср. скорость: {self.speed} км/ч; ',
                f'Потрачено ккал: {self.calories}.')


class Training():
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    CALORIES_M: float = 18
    CALORIES_S: float = 1.79

    def get_spent_calories(self):
        cal = self.CALORIES_M * self.get_mean_speed() - self.CALORIES_S
        calories = cal * self.weight / self.M_IN_KM * self.duration * 60
        return calories


class SportsWalking(Training):
    coef_walk: float = 0.035
    coef_walk2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_1 = self.coef_walk * self.weight
        calories_2 = self.get_mean_speed()**2 // self.height
        calories_3 = calories_2 * self.coef_walk2 * self.weight
        calories = (calories_1 + calories_3) * self.duration * 60
        return calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    coef_swim: float = 1.1
    coef_swim2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / super().M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self):
        calories_1 = self.get_mean_speed() + self.coef_swim
        calories = calories_1 * self.coef_swim2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    type_dict = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
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
