from internal.frameworks.drivers.Adder_pb2_grpc import AdderServicer
from internal.use_cases.addnumbers import AddNumbersUseCase
from internal.frameworks.drivers import Adder_pb2
from internal.adapters.rabbitmq_publisher import RabbitMQPublisher
from internal.adapters.database_initalizer import InitDB
from internal.adapters.outbox_repository import OutBoxRepository
from internal.entities.outbox_message import Outbox


class GRPCController(AdderServicer):
    def __init__(self):
        self.add_numbers_use_case = AddNumbersUseCase()
        self.db = InitDB()
        self.outbox_repository = OutBoxRepository(self.db)

    def Add(self, request, context):
        result = self.add_numbers_use_case.execute(request.num_one, request.num_two)
        
        # Store the result in outbox
        outbox_message = Outbox(payload=result)
        self.outbox_repository.mess = outbox_message
        self.outbox_repository.store(result)
        
        return Adder_pb2.AddResponse(result=result)