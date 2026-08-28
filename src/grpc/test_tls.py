"""
Test script to verify TLS gRPC communication between client and server.
"""
import threading
import time
import grpc_server_tls
import grpc_client_tls

def start_server(port):
    grpc_server_tls.serve(port=port)

def test_communication():
    port = 50054
    # Start server in a background thread.
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()
    # Give the server a moment to start.
    time.sleep(2)
    # Run the client with the same port.
    grpc_client_tls.run(client_id="Hospital1", round_number=1, message="Test TLS from Hospital 1", port=port)
    # Give a moment for the response.
    time.sleep(1)
    print("TLS test completed.")

if __name__ == '__main__':
    test_communication()
