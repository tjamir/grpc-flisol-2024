
# Setup de ambiente deV GRPC em python

```
python -m pip install --user virtualenv
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

# Instalação do gRPC

```
python -m pip install grpcio grpcio-tools grpcio-reflection
```

# Editando o arquivo protobuf

Abrir o arquivo no caminho: `protos/api.proto`

```
syntax = "proto3";

package helloservice;

message HelloRequest {
    string name = 1;
}

message HelloResponse {
    string greet = 1;
}

service HelloService {
    rpc SayHello(HelloRequest) returns (HelloResponse) {}
}
```

## Gerando os arquivos necessários

```
python protogen.py
```

Inspecionar os arquivos gerados
gen/python/protos/api_pb2.py
gen/python/protos/api_pb2_grpc.py

## Analisando o hello_server.py

```python
from concurrent import futures
import grpc
from gen.python.protos import api_pb2, api_pb2_grpc
from grpc_reflection.v1alpha import reflection

## Implementação do serviço
class Hello(api_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        return api_pb2.HelloResponse(greet="Hello, {}!".format(request.name))

def main():
    serve()

## Servidor gRPC
def serve():
    port = "8000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ## Registra o serviço no servidor
    api_pb2_grpc.add_HelloServiceServicer_to_server(Hello(), server)
    SERVICE_NAMES = (
        api_pb2.DESCRIPTOR.services_by_name["HelloService"],
        reflection.SERVICE_NAME,
    )
    ## Habilita o reflection
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:{}".format(port))
    ## Inicia o servidor
    server.start()
    print("Server started, listening on port {}".format(port))
    server.wait_for_termination()

if __name__ == "__main__":
    main()

```

## Rodando e testando o servidor

```
python hello_server.py
```

### Testando utilizando o gRPC UI   

Instação do gRPC UI

```
go install github.com/fullstorydev/grpcui/cmd/grpcui@latest
```

Rodando o gRPC UI
```
grpcui -port 8000
```

### Desafio

Modificar a Hello Request para receber dois parâmetros: A saudação e o nome. Como resposta a api deve retornar uma mensagem de saudação com o nome.

Exemplo:

Saudação: Bom dia
Nome: João

Resposta: Bom dia, João!
