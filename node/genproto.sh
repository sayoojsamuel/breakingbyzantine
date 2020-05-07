#!/usr/bin/env bash

echo -n "Generating Protobuf files..."
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/byzantine.proto

# The .proto files are in /protoc/ directory
# The generated python class files will be in the current directory
#protoc -I./protos --python_out=. --grpc_python_out=. protos/byzantine.proto
