from grpc_tools import protoc

# Set the input directory containing the .proto file
proto_include = "."
# Set the output directory for generated Python files
python_output = "."
grpc_python_output = "."

# Specify the .proto file
proto_file = "test.proto"

# Use protoc to generate Python files
protoc.main(
    (
        "",
        f"-I{proto_include}",
        f"--python_out={python_output}",
        f"--grpc_python_out={grpc_python_output}",
        f"{proto_file}",
    )
)
