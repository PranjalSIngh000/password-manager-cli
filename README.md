# Password Manager CLI

A command-line password manager with AES-256 encryption, PBKDF2 key derivation, and SQLite storage. Built with Python.

## Installation
git clone https://github.com/PranjalSIngh000/password-manager-cli
cd password-manager-cli
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Usage
python cli.py init
python cli.py add github.com yourname
python cli.py get github.com
python cli.py list
python cli.py delete github.com

## Security Design
- Master password never stored — key derived via PBKDF2-SHA256 (480,000 iterations, OWASP 2023 spec)
- Each entry encrypted with AES-128-CBC + HMAC via Fernet
- Password input always via getpass (never echoed to terminal)
- Password generation uses Python secrets module (CSPRNG)
- SQLite DB stores only ciphertext — safe to back upgit