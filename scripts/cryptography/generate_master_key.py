from cryptography.fernet import Fernet


def main() -> None:
    print(Fernet.generate_key())


if __name__ == "__main__":
    main()
