import grpc_tools.protoc
import os

def replace_import_path(file_path, old_path, new_path):
    with open(file_path, 'r') as f:
        content = f.read()
    content = content.replace(old_path, new_path)
    with open(file_path, 'w') as f:
        f.write(content)

os.makedirs('gen/python', exist_ok=True)
grpc_tools.protoc.main([
    '--proto_path=./protos',
    '--python_out=./gen/python',
    '--grpc_python_out=./gen/python',
    '--pyi_out=./gen/python',
    './protos/api.proto',
])

## Replaces line 'from protos import api_pb2 as protos_dot_api__pb2' with 'from gen.python.protos import api_pb2 as protos_dot_api__pb2' on api_pb2_grpc.py

replace_import_path('gen/python/protos/api_pb2_grpc.py', 'from protos', 'from gen.python.protos')