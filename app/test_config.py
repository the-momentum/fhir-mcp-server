#!/usr/bin/env python3
"""
Test script to check configuration loading
"""


def test_config():
    print("🔧 Testing Configuration Loading")
    print("=" * 40)

    try:
        from app.config import settings

        print("✅ Settings loaded successfully")
        print(f"LOINC_USERNAME: {settings.LOINC_USERNAME}")
        print(f"LOINC_PASSWORD type: {type(settings.LOINC_PASSWORD)}")
        print(f"LOINC_PASSWORD value: {repr(settings.LOINC_PASSWORD)}")

        if isinstance(settings.LOINC_PASSWORD, str):
            print("✅ LOINC_PASSWORD is properly decrypted to string")
        else:
            print(f"❌ LOINC_PASSWORD is not a string - it's {type(settings.LOINC_PASSWORD)}")

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_config()
