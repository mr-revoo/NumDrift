from concurrent import futures
from internal.frameworks.drivers import Adder_pb2_grpc
from internal.adapters.grpc_controller import GRPCController
import grpc 


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    controller_instance = GRPCController()
    Adder_pb2_grpc.add_AdderServicer_to_server(controller_instance, server)
    server.add_insecure_port('localhost:50051')
    server.start()
    print("Server started on localhost:50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()