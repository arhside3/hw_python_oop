class InfoMessage:
    
    def __init__(self, 
                 training_type: str, 
                 duration: float, 
                 distance: float, 
                 speed: float, 
                 calories: float) :
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    M_IN_HOUR: float = 60   

    def __init__(self, action: int, duration: float, weight: float) :
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.duration, 
                           self.get_distance(), 
                           self.get_mean_speed(), 
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.geat_mean_speed() + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / M_IN_KM * duration_in_minutes)


class SportsWalking(Training):
    coef_walk: float = 0.035
    coef_walk2: float = 2
    coef_walk3: float = 0.029

    def __init__(self, action: int, duration: float, weight: float, height: int) :
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        return ((coef_walk * self.weight + (self.geat_mean_speed() ** coef_walk2 / self.height)
                 * coef_walk3 * self.weight) * duration_in_minutes)


class Swimming(Training):
    coef_swim: float = 1.1
    coef_swim2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int) :
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) :
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return length_pool * count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
         return (self.get_mean_speed() + coef_swim) * coef_swim2 * self.weight * self.durations


def read_package(workout_type: str) :
    training_types = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking}
    return training_types[workout_type](*data)


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
