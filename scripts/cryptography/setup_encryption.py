#!/usr/bin/env python3
"""
Setup script for FHIR MCP Server encryption.

Automates encryption setup:
1. Checks for MASTER_KEY in config/.env
2. Generates a new MASTER_KEY if needed
3. Encrypts sensitive values if they exist
4. Updates the .env file with encrypted values

Usage:
    uv run scripts/cryptography/setup_encryption.py
    docker exec fhir-mcp-server uv run scripts/cryptography/setup_encryption.py
"""

import sys
from pathlib import Path

from cryptography.fernet import Fernet

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def load_env_file(env_path: Path) -> dict[str, str]:
    env_vars = {}

    if not env_path.exists():
        return env_vars

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]

                env_vars[key] = value

    return env_vars


def save_env_file(env_path: Path, env_vars: dict[str, str]):
    env_path.parent.mkdir(parents=True, exist_ok=True)

    existing_lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            existing_lines = f.readlines()

    existing_var_names = set()
    for line in existing_lines:
        if line.strip() and not line.startswith("#") and "=" in line:
            var_name = line.split("=")[0].strip()
            existing_var_names.add(var_name)

    updated_vars = set(env_vars.keys())

    with open(env_path, "w") as f:
        for line in existing_lines:
            if line.strip() and not line.startswith("#") and "=" in line:
                var_name = line.split("=")[0].strip()
                if var_name in updated_vars:
                    f.write(f"{var_name}={env_vars[var_name]}\n")
                else:
                    f.write(line)
            else:
                f.write(line)

        for var_name, var_value in env_vars.items():
            if var_name not in existing_var_names:
                f.write(f"{var_name}={var_value}\n")


def generate_master_key() -> str:
    return Fernet.generate_key().decode("utf-8")


def encrypt_value(value: str, master_key: str) -> str:
    if not value.strip():
        return ""

    fernet = Fernet(master_key.encode("utf-8"))
    encrypted = fernet.encrypt(value.encode("utf-8"))
    return encrypted.decode("utf-8")


def main():
    env_path = project_root / "config" / ".env"

    env_vars = load_env_file(env_path)

    updated_vars = {}

    master_key = env_vars.get("MASTER_KEY", "").strip()
    if not master_key:
        print("🔑 No MASTER_KEY found. Generating new one...")
        master_key = generate_master_key()
        updated_vars["MASTER_KEY"] = f"'{master_key}'"
        print("✅ Generated new MASTER_KEY")
    else:
        print("✅ MASTER_KEY already exists")

    encryption_key = master_key
    if not encryption_key and "MASTER_KEY" in updated_vars:
        encryption_key = updated_vars["MASTER_KEY"].strip("'")

    sensitive_vars = ["LOINC_PASSWORD", "FHIR_SERVER_CLIENT_SECRET", "PINECONE_API_KEY"]

    print("\n🔒 Checking sensitive variables...")

    for var_name in sensitive_vars:
        current_value = env_vars.get(var_name, "").strip()

        if not current_value:
            print(f"⏭️  {var_name}: Empty or not set, skipping...")
            continue

        if current_value.startswith("gAAAAA"):
            print(f"🔐 {var_name}: Already encrypted, skipping...")
            continue

        print(f"🔒 {var_name}: Encrypting...")
        try:
            encrypted_value = encrypt_value(current_value, encryption_key)
            updated_vars[var_name] = f"'{encrypted_value}'"
            print(f"✅ {var_name}: Encrypted successfully")
        except Exception as e:
            print(f"❌ {var_name}: Failed to encrypt - {e}")

    print(f"\n💾 Saving to {env_path}...")
    try:
        save_env_file(env_path, updated_vars)
        print("✅ Environment file updated successfully")
    except Exception as e:
        print(f"❌ Failed to save environment file: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
