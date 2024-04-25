import grpc_tools.protoc
import os

def replace_import_path(file_path, old_path, new_path):
    with open(file_path, 'r') as f:
        content = f.read()
    content = content.replace(old_path, new_path)
    with open(file_path, 'w') as f:
        f.write(content)

os.system("python -m grpc_tools.protoc --proto_path=./protos --python_out=./bank-client --grpc_python_out=./bank-client --pyi_out=./bank-client ./protos/api.proto")
