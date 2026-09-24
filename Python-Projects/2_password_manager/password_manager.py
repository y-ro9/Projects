#!/usr/bin/env python3

"""
🔐 Password Manager
Cybersecurity Project

Features:
- Master password protection
- PBKDF2-HMAC-SHA256 key derivation
- Fernet encryption
- Add / View / Delete credentials
- Secure password generation
- Local encrypted vault

Author: Yash Raj
Date: 2026
"""

import base64
import json
import os
import secrets
import string
from getpass import getpass
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# ============================================================
# Configuration
# ============================================================

VAULT_FILE = Path("vault.dat")
SALT_FILE = Path("vault.salt")

# PBKDF2 iterations
PBKDF2_ITERATIONS = 600_000

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}?"


# ============================================================
# Password Manager Class
# ============================================================

class PasswordManager:
    """Main Password Manager class."""

    def __init__(self):
        self.vault = {}
        self.fernet = None

    # --------------------------------------------------------
    # Key Derivation
    # --------------------------------------------------------

    @staticmethod
    def derive_key(master_password, salt):
        """
        Derive an encryption key from the master password
        using PBKDF2-HMAC-SHA256.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS
        )

        key = kdf.derive(master_password.encode("utf-8"))

        return base64.urlsafe_b64encode(key)

    # --------------------------------------------------------
    # Create New Vault
    # --------------------------------------------------------

    def create_vault(self):
        """Create a new encrypted password vault."""

        print("\n🔐 No vault found.")
        print("Creating a new encrypted password vault...\n")

        while True:

            master_password = getpass("Create master password: ")
            confirm_password = getpass("Confirm master password: ")

            if not master_password:
                print("❌ Master password cannot be empty.")
                continue

            if len(master_password) < 8:
                print("❌ Master password must contain at least 8 characters.")
                continue

            if master_password != confirm_password:
                print("❌ Passwords do not match.")
                continue

            break

        # Generate random salt
        salt = secrets.token_bytes(16)

        # Save salt
        SALT_FILE.write_bytes(salt)

        # Generate encryption key
        key = self.derive_key(master_password, salt)

        # Create Fernet object
        self.fernet = Fernet(key)

        # Empty vault
        self.vault = {}

        # Save encrypted vault
        self.save_vault()

        print("\n✅ Encrypted vault created successfully!")

    # --------------------------------------------------------
    # Unlock Existing Vault
    # --------------------------------------------------------

    def unlock_vault(self):
        """Unlock an existing encrypted vault."""

        print("\n🔓 Existing vault detected.")

        master_password = getpass("Enter master password: ")

        try:

            salt = SALT_FILE.read_bytes()

            key = self.derive_key(master_password, salt)

            self.fernet = Fernet(key)

            encrypted_data = VAULT_FILE.read_bytes()

            decrypted_data = self.fernet.decrypt(encrypted_data)

            self.vault = json.loads(
                decrypted_data.decode("utf-8")
            )

            print("✅ Vault unlocked successfully!")

            return True

        except InvalidToken:

            print("❌ Incorrect master password.")

        except Exception as error:

            print(f"❌ Unable to unlock vault: {error}")

        self.fernet = None

        return False

    # --------------------------------------------------------
    # Save Vault
    # --------------------------------------------------------

    def save_vault(self):
        """Encrypt and save vault to disk."""

        if self.fernet is None:
            print("❌ Vault is locked.")
            return

        data = json.dumps(
            self.vault,
            indent=4
        ).encode("utf-8")

        encrypted_data = self.fernet.encrypt(data)

        temporary_file = Path("vault.tmp")

        temporary_file.write_bytes(encrypted_data)

        os.replace(
            temporary_file,
            VAULT_FILE
        )

    # --------------------------------------------------------
    # Add Credential
    # --------------------------------------------------------

    def add_credential(self):

        print("\n" + "-" * 45)
        print("➕ ADD CREDENTIAL")
        print("-" * 45)

        service = input("Website / Service: ").strip()

        if not service:
            print("❌ Service name cannot be empty.")
            return

        username = input("Username / Email: ").strip()

        if not username:
            print("❌ Username cannot be empty.")
            return

        password = getpass("Password: ")

        if not password:
            print("❌ Password cannot be empty.")
            return

        self.vault[service] = {
            "username": username,
            "password": password
        }

        self.save_vault()

        print(
            f"\n✅ Credential for '{service}' "
            "saved securely."
        )

    # --------------------------------------------------------
    # View Credentials
    # --------------------------------------------------------

    def view_credentials(self):

        print("\n" + "-" * 45)
        print("👁️ VIEW CREDENTIALS")
        print("-" * 45)

        if not self.vault:
            print("📭 Vault is empty.")
            return

        services = sorted(self.vault.keys())

        print("\n📋 Saved Services:\n")

        for number, service in enumerate(services, 1):
            print(f"{number}. {service}")

        print("\nEnter service name to view.")
        print("Press Enter to cancel.")

        service = input("\nService: ").strip()

        if not service:
            return

        if service not in self.vault:

            print("❌ Service not found.")

            return

        credential = self.vault[service]

        print("\n" + "=" * 45)

        print(f"🌐 Service : {service}")
        print(f"👤 Username: {credential['username']}")
        print(f"🔑 Password: {credential['password']}")

        print("=" * 45)

    # --------------------------------------------------------
    # Delete Credential
    # --------------------------------------------------------

    def delete_credential(self):

        print("\n" + "-" * 45)
        print("🗑️ DELETE CREDENTIAL")
        print("-" * 45)

        if not self.vault:

            print("📭 Vault is empty.")

            return

        print("\nSaved Services:\n")

        for service in sorted(self.vault.keys()):

            print(f"• {service}")

        service = input(
            "\nEnter service to delete: "
        ).strip()

        if service not in self.vault:

            print("❌ Service not found.")

            return

        confirmation = input(
            f"Delete '{service}'? (y/N): "
        ).strip().lower()

        if confirmation == "y":

            del self.vault[service]

            self.save_vault()

            print("\n✅ Credential deleted successfully.")

        else:

            print("\n↩️ Deletion cancelled.")

    # --------------------------------------------------------
    # Generate Strong Password
    # --------------------------------------------------------

    @staticmethod
    def generate_password(length=16):

        if length < 12:

            length = 12

        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        numbers = string.digits
        special = SPECIAL_CHARACTERS

        # Guarantee at least one character from each category
        password = [

            secrets.choice(lowercase),

            secrets.choice(uppercase),

            secrets.choice(numbers),

            secrets.choice(special)
        ]

        all_characters = (
            lowercase +
            uppercase +
            numbers +
            special
        )

        # Fill remaining characters
        for _ in range(length - 4):

            password.append(
                secrets.choice(all_characters)
            )

        # Secure shuffle
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    # --------------------------------------------------------
    # Password Generator Interface
    # --------------------------------------------------------

    def generate_and_show(self):

        print("\n" + "-" * 45)
        print("🔑 STRONG PASSWORD GENERATOR")
        print("-" * 45)

        try:

            user_input = input(
                "Password length (default 16): "
            ).strip()

            if user_input:

                length = int(user_input)

            else:

                length = 16

            if length < 12:

                print(
                    "⚠️ Minimum generator length is 12."
                )

                length = 12

            password = self.generate_password(length)

            print("\n🔐 Generated Password:")
            print()
            print(password)

            print(
                "\n⚠️ Save it securely if you intend "
                "to use it."
            )

        except ValueError:

            print("❌ Please enter a valid number.")

    # --------------------------------------------------------
    # Main Menu
    # --------------------------------------------------------

    def main_menu(self):

        while True:

            print("\n")
            print("=" * 50)
            print("🔐 PASSWORD MANAGER")
            print("=" * 50)

            print("1. ➕ Add Credential")
            print("2. 👁️ View Credential")
            print("3. 🗑️ Delete Credential")
            print("4. 🔑 Generate Strong Password")
            print("5. 🚪 Exit")

            print("=" * 50)

            choice = input(
                "\nSelect option (1-5): "
            ).strip()

            if choice == "1":

                self.add_credential()

            elif choice == "2":

                self.view_credentials()

            elif choice == "3":

                self.delete_credential()

            elif choice == "4":

                self.generate_and_show()

            elif choice == "5":

                print("\n🔒 Vault locked.")
                print("👋 Stay Secure!\n")

                break

            else:

                print(
                    "\n❌ Invalid option. "
                    "Please select 1-5."
                )

    # --------------------------------------------------------
    # Application Start
    # --------------------------------------------------------

    def run(self):

        print("\n")
        print("=" * 50)
        print("🔐 PASSWORD MANAGER")
        print("🛡️ Cybersecurity Project")
        print("=" * 50)

        # Check whether vault exists
        if (
            not VAULT_FILE.exists()
            or not SALT_FILE.exists()
        ):

            self.create_vault()

        else:

            if not self.unlock_vault():

                print(
                    "\n🚫 Access denied."
                )

                return

        # Open main menu
        self.main_menu()


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    manager = PasswordManager()

    manager.run()