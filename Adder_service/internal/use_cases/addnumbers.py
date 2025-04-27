from internal.entities.Sum import Sum
class AddNumbersUseCase:
    def execute(self, number1, number2):
        Sum.result = number1 + number2
        return Sum.result