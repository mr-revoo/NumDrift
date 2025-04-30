from internal.frameworks.drivers.Adder_pb2_grpc import AdderServicer
from internal.use_cases.addnumbers import AddNumbersUseCase
from internal.frameworks.drivers import Adder_pb2
from internal.adapters.rabbitmq_publisher import RabbitMQPublisher


class GRPCController(AdderServicer):
    def __init__(self):
        self.add_numbers_use_case = AddNumbersUseCase()
        #self.rabbitmq_publisher = RabbitMQPublisher()

    def Add(self, request, context):
        sum_entity = self.add_numbers_use_case.execute(request.num_one, request.num_two)  # Assuming a, b from .proto
        #self.rabbitmq_publisher.publish(sum_entity)
        return Adder_pb2.AddResponse(result=sum_entity)