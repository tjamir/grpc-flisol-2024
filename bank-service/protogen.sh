#!/bin/bash

mkdir -p gen/go/protos

mkdir -p bank-server/internal/api


protoc \
--proto_path=${PWD}/protos \
--go_out=bank-server/internal/api \
--go_opt=paths=source_relative \
--go-grpc_out=bank-server/internal/api \
--go-grpc_opt=paths=source_relative \
${PWD}/protos/api.proto

python protogen.py