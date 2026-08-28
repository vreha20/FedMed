"""
TLS-enabled gRPC client for MedCommunication service.
"""
import grpc
import medical_pb2
import medical_pb2_grpc
import os

CERT_DIR = os.path.join(os.path.dirname(__file__), 'certs')
SERVER_CERT = os.path.join(CERT_DIR, 'server.crt')

def run(client_id="1", round_number=1, message="Hello Server", port=50053):
    # Load server certificate to trust
    with open(SERVER_CERT, 'rb') as f:
        trusted_certs = f.read()
    # Create SSL credentials
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    with grpc.secure_channel(f'localhost:{port}', credentials) as channel:
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
