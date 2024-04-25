## Instalação das ferramentes GRPC para Go

```
sudo apt install protobuf-compiler
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
```

Atualizando o PATH para executar os comandos

```
export PATH="$PATH:$(go env GOPATH)/bin"
```

## Gerando os arquivos
```
$ protoc --go_out=./gen/go/protos --go_opt=paths=source_relative \
    --go-grpc_out=.gen/go/protos --go-grpc_opt=paths=source_relative \
    protos/clerk/clerkapi.proto
```