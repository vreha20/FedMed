"""
Launcher for Hospital 2 (client ID 2).
"""
import os
os.environ["CLIENT_ID"] = "2"
from .flower_client_base import start_client

if __name__ == "__main__":
    start_client()