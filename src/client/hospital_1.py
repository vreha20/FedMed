"""
Launcher for Hospital 1 (client ID 1).
"""
import os
os.environ["CLIENT_ID"] = "1"
from .flower_client_base import start_client

if __name__ == "__main__":
    start_client()