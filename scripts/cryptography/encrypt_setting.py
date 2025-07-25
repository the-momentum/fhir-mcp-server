import os
import sys

from cryptography.fernet import Fernet
from dotenv import load_dotenv

dotenv_path = "config/.env"

load_dotenv(dotenv_path)

if __name__ == "__main__":
    if "MASTER_KEY" not in os.environ:
        print("Set MASTER_KEY env variable to encrypt")

    f = Fernet(os.environ["MASTER_KEY"])
    print(f.encrypt(sys.argv[1].encode("utf-8")))
