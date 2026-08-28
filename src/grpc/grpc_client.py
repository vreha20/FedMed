"""
Simple gRPC client for MedCommunication service.
"""

import grpc
import medical_pb2
import medical_pb2_grpc

def run(client_id="1", round_number=1, message="Hello Server", port=50051):
    # Connect to the gRPC server.
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = medical_pb2_grpc.MedCommunicationStub(channel)
        response = stub.SendData(medical_pb2.DataRequest(
            client_id=client_id,
            round_number=round_number,
            message=message
        ))
    print(f"Received from server: {response.server_message}")
    print(f"Success: {response.success}")

if __name__ == '__main__':
    run()