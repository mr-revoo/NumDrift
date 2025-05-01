from concurrent import futures
from internal.frameworks.drivers import Adder_pb2_grpc
from internal.adapters.grpc_controller import GRPCController
import grpc
from internal.adapters.database_initalizer import InitDB
from internal.adapters.outbox_repository import OutBoxRepository
from internal.adapters.rabbitmq_publisher import RabbitMQPublisher
from internal.use_cases.outbox_processing import OutBoxProcessor
import threading

def serve():
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    controller_instance = GRPCController()
    Adder_pb2_grpc.add_AdderServicer_to_server(controller_instance, server)
    server.add_insecure_port('localhost:50051')
    
    # Start the outbox processor in a separate thread
    db = InitDB()
    outbox_repository = OutBoxRepository(db)
    publisher = RabbitMQPublisher(queuename="sums")
    outbox_processor = OutBoxProcessor(
        repository=outbox_repository,
        publisher=publisher,
        interval=5.0,  
        clustersize=10
    )
    
    processor_thread = threading.Thread(target=outbox_processor.start, daemon=True)
    processor_thread.start()
    
    server.start()
    print("Server started on localhost:50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()