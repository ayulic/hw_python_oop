


class InfoMessage:
    def __init__(self, 
                training_type: str, 
                duration: int,
                distance: float,
                speed: float,
                calories: int
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        '''
        returns meassage about training
        '''
        message = (
            f'Тип тренировки: {self.training_type}; ' +  
                    f'Длительность: {self.duration:.3f} ч.; ' +  
                    f'Дистанция: {self.distance:.3f} км; ' + 
                    f'Ср. скорость: {self.speed:.3f} км/ч; ' +
                    f'Потрачено ккал: {self.calories:.3f}.'
        )
        return  message


class Training:
    # meters in km
    M_IN_KM: int = 1000
    # walking step length 
    LEN_STEP: float = 0.65 
    MIN_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    
    def get_distance(self) -> float:
        '''
        returns distance in km after training
        '''
        return self.action * self.LEN_STEP / self.M_IN_KM 
    
    def get_mean_speed(self) -> float:
        '''
        returns avg speed during trainig
        '''
        return self.get_distance() / self.duration 


    def get_spent_calories(self):
        '''
        returns spent Kilokalories during training
        '''
        pass


    def show_training_info(self) -> InfoMessage:
        '''
        returns training info
        '''
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories(),)


class Running(Training):
    # constants
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 
    COEFF_MID_SPEED_1 = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.COEFF_MID_SPEED_1)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    # constants
    WEIGHT_COEF_1: float = 0.035
    WEIGHT_COEF_2: float = 0.029

    def __init__(
                self, 
                action: int, 
                duration: float, 
                weight: float,
                height: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    
    def get_spent_calories(self) -> float:
        return (
                    ((self.WEIGHT_COEF_1 * self.weight + 
                    ((self.get_mean_speed())**2  #*self.M_IN_KM/self.MIN_IN_HOUR*60 
                    // self.height)
                    * self.WEIGHT_COEF_2 * self.weight) * 
                    self.duration * self.MIN_IN_HOUR)
                )


class Swimming(Training):
    # constants
    LEN_STEP: float = 1.38
    SWIM_SPEED_COEF: float = 1.1
    SWIM_WEIGHT_COEF: int = 2


    def __init__(
                self, 
                action: int, 
                duration: float, 
                weight: float,
                length_pool: int,
                count_pool: int
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    
    def get_mean_speed(self) -> float:
        '''
        returns avg swimming speed
        '''
        return (
            self.length_pool * self.count_pool 
            / self.M_IN_KM / self.duration  
        )


    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_SPEED_COEF) 
            * self.SWIM_WEIGHT_COEF * self.weight 
            #* self.duration   
        )


def read_package(workout_type: str, data: list):
    '''
    read sensors data 
    '''
    trainings = {
        'SWM':Swimming,
        'RUN':Running,
        'WLK':SportsWalking,
    }
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    '''
    main function
    '''
    print(training.show_training_info().get_message())



if __name__ == '__main__':
    packages = [        
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data)) 