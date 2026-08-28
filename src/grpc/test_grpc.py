"""
Test script to verify gRPC communication between client and server.
"""

import threading
import time
import grpc_server
import grpc_client

def start_server(port):
    # We need to modify grpc_server.serve to accept a port.
    # Currently, grpc_server.serve(port) already accepts a port.
    grpc_server.serve(port=port)

def test_communication():
    port = 50052
    # Start server in a background thread.
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()
    # Give the server a moment to start.
    time.sleep(2)
    # Run the client with the same port.
    grpc_client.run(client_id="Hospital1", round_number=1, message="Test from Hospital 1", port=port)
    # Give a moment for the response.
    time.sleep(1)
    print("Test completed.")

if __name__ == '__main__':
    test_communication()