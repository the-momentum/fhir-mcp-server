import os
import sys

from cryptography.fernet import Fernet
from dotenv import load_dotenv

dotenv_path = "config/.env"

load_dotenv(dotenv_path)


def main() -> None:
    setting = sys.argv[1]
    fernet = Fernet(os.environ["MASTER_KEY"])
    print(fernet.decrypt(setting.encode("utf-8")))


if __name__ == "__main__":
    main()
