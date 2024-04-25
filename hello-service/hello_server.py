from concurrent import futures
import grpc
from gen.python.protos import api_pb2, api_pb2_grpc
from grpc_reflection.v1alpha import reflection



class Hello(api_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        return api_pb2.HelloResponse(greet="Hello, {}!".format(request.name))

def main():
    serve()


def serve():
    port = "8000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_HelloServiceServicer_to_server(Hello(), server)
    SERVICE_NAMES = (
        api_pb2.DESCRIPTOR.services_by_name["HelloService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    print("Server started, listening on port {}".format(port))
    server.wait_for_termination()

if __name__ == "__main__":
    main()
