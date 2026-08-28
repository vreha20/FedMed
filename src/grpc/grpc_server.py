"""
Simple gRPC server for MedCommunication service.
"""

import grpc
from concurrent import futures
import time
import medical_pb2
import medical_pb2_grpc

class MedCommunicationServicer(medical_pb2_grpc.MedCommunicationServicer):
    def SendData(self, request, context):
        # Simply echo back a response.
        return medical_pb2.DataResponse(
            server_message=f"Hello {request.client_id}! Received round {request.round_number}.",
            success=True
        )

def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    medical_pb2_grpc.add_MedCommunicationServicer_to_server(
        MedCommunicationServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"gRPC server started on port {port}")
    try:
        while True:
            time.sleep(86400)  # sleep for a day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()