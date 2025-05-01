from internal.frameworks.drivers import Adder_pb2, Adder_pb2_grpc
import grpc

def run(a, b):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = Adder_pb2_grpc.AdderStub(channel)
        request = Adder_pb2.AddRequest(num_one=a, num_two=b)
        print(f"Sending request: {request}") 
        response = stub.Add(request)
        print(f"Received response: {response}")  
    return response

print(run(1200,50))