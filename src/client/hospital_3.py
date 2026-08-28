"""
Launcher for Hospital 3 (client ID 3).
"""
import os
os.environ["CLIENT_ID"] = "3"
from .flower_client_base import start_client

if __name__ == "__main__":
    start_client()