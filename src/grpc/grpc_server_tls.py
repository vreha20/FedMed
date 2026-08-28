"""
TLS-enabled gRPC server for MedCommunication service.
"""
import grpc
from concurrent import futures
import time
import medical_pb2
import medical_pb2_grpc
import os

CERT_DIR = os.path.join(os.path.dirname(__file__), 'certs')
SERVER_CERT = os.path.join(CERT_DIR, 'server.crt')
SERVER_KEY = os.path.join(CERT_DIR, 'server.key')

class MedCommunicationServicer(medical_pb2_grpc.MedCommunicationServicer):
    def SendData(self, request, context):
        return medical_pb2.DataResponse(
            server_message=f"Hello {request.client_id}! Received round {request.round_number}.",
            success=True
        )

def serve(port=50053):
    # Load server certificate and key
    with open(SERVER_CERT, 'rb') as f:
        server_cert = f.read()
    with open(SERVER_KEY, 'rb') as f:
        server_key = f.read()
    # Create SSL credentials
    server_credentials = grpc.ssl_server_credentials(((server_key, server_cert),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    medical_pb2_grpc.add_MedCommunicationServicer_to_server(
        MedCommunicationServicer(), server
    )
    server.add_secure_port(f'[::]:{port}', server_credentials)
    server.start()
    print(f"TLS gRPC server started on port {port}")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
