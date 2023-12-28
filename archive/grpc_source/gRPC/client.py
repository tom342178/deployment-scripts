import argparse
import grpc
import dummy_pb2
import dummy_pb2_grpc
import json
import time


def create_channel(conn:str, credentials:dict=None):
    """
    Create a gRPC channel against another machine.
    """
    channel = None
    if credentials is not None:
        try:
            channel = grpc.secure_channel(target=conn, credentials=credentials)
        except Exception as error:
            print(f"Failed to create a secure channel against {conn} (Error: {error})")
            exit(1)
    else:
        try:
            channel = grpc.insecure_channel(target=conn)
        except Exception as error:
            print(f"Failed to create an insecure channel against {conn} (Error: {error})")
            exit(1)
    if channel is None:
        print(f"Failed to create a channel connection against {conn}")
        exit(1)

    return channel


def __close_channel(channel):
    try:
        channel.close()
    except Exception as error:
        print(f"Failed to close channel (Error: {error})")


def set_stub(channel):
    """
    Create a service connection.
    """
    try:
        return dummy_pb2_grpc.SerializeServiceStub(channel)
    except Exception as error:
        print(f"Failed to create a stub against the channel (Error: {error})")
        exit(1)


def execute_service(stub):
    """
    Execute the service.
    """
    deserialized_data_list = []`
    try:
        response = stub.GetSampleData(dummy_pb2.Empty())
    except Exception as error:
        print(f"Failed to execute the service (Error: {error})")
    else:
        try:
            serialized_data_list = response.serialized_data
        except Exception as error:
            print(f"Failed to get serialized data (Error: {error})")
        else:
            deserialized_data_list = [json.loads(data) for data in serialized_data_list]

    return deserialized_data_list


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--conn', type=str, default='127.0.0.1:50051')
    args = parse.parse_args()

    # Create a channel to connect to the server
    channel = create_channel(conn=args.conn)

    # Associate the stub with the server and allow the client to make RPC calls
    stub = set_stub(channel=channel)

    while True:
        # Execute the service
        # try:
        deserialized_data = execute_service(stub=stub)
        print(deserialized_data)
        time.sleep(30)
        # except KeyboardInterrupt:
        #     __close_channel(channel=channel)

    # __close_channel(channel=channel)


if __name__ == '__main__':
    main()
