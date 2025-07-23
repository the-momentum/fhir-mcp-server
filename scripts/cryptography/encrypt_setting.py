import os
import sys
from dotenv import load_dotenv

from cryptography.fernet import Fernet

dotenv_path = "config/.env"

load_dotenv(dotenv_path)

if __name__ == "__main__":
    if "MASTER_KEY" not in os.environ:
        print("Set MASTER_KEY env variable to encrypt")

    f = Fernet(os.environ["MASTER_KEY"])
    print(f.encrypt(sys.argv[1].encode("utf-8")))
