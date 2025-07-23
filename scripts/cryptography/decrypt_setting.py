import os
import sys
from dotenv import load_dotenv

from cryptography.fernet import Fernet

dotenv_path = "config/.env"

load_dotenv(dotenv_path)


def main():
    setting = sys.argv[1]
    fernet = Fernet(os.environ["MASTER_KEY"])
    print(fernet.decrypt(setting.encode("utf-8")))


if __name__ == "__main__":
    main()
