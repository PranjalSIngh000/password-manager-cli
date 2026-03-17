import argparse
import getpass
import os
import secrets
import string
from crypto import derive_key, generate_salt, encrypt, decrypt
from db import init_db, add_entry, get_entry, get_all_entries, delete_entry
from rich.console import Console
from rich.table import Table

console = Console()

SALT_FILE = "salt.key"

def load_or_create_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = generate_salt()
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def get_master_key():
    password = getpass.getpass("Enter master password: ")
    salt = load_or_create_salt()
    return derive_key(password, salt)

def cmd_init():
    init_db()
    load_or_create_salt()
    print("Vault initialised successfully!")

def cmd_add(site, username):
    key = get_master_key()
    import getpass
    password = getpass.getpass("Enter password to store: ")
    add_entry(site, username, password, key)
    print(f"Password for {site} saved successfully!")

def cmd_get(site):
    key = get_master_key()
    result = get_entry(site, key)
    if result is None:
        print(f"No entry found for {site}")
    else:
        username, password = result
        print(f"Username : {username}")
        print(f"Password : {password}")

def cmd_list():
    rows = get_all_entries()
    if not rows:
        console.print("[yellow]No entries found.[/yellow]")
        return
    table = Table(title="Stored Passwords")
    table.add_column("Site", style="cyan")
    table.add_column("Username", style="green")
    table.add_column("Added", style="dim")
    for row in rows:
        table.add_row(row[0], row[1], row[2])
    console.print(table)

def cmd_delete(site):
    confirm = getpass.getpass("Enter master password to confirm: ")
    salt = load_or_create_salt()
    key = derive_key(confirm, salt)
    delete_entry(site)
    print(f"Entry for {site} deleted.")

def generate_password(length: int = 20) -> str:
    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(pool) for _ in range(length))

def cmd_generate(site, username):
    key = get_master_key()
    password = generate_password()
    add_entry(site, username, password, key)
    console.print(f"[green]Generated and saved password for {site}[/green]")
    console.print(f"[cyan]Password: {password}[/cyan]")    

def main():
    parser = argparse.ArgumentParser(prog='pm', description='Password Manager CLI')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('init')

    add_p = sub.add_parser('add')
    add_p.add_argument('site')
    add_p.add_argument('username')

    get_p = sub.add_parser('get')
    get_p.add_argument('site')

    sub.add_parser('list')

    del_p = sub.add_parser('delete')
    del_p.add_argument('site')

    args = parser.parse_args()

    if args.command == 'init':
        cmd_init()
    elif args.command == 'add':
        cmd_add(args.site, args.username)
    elif args.command == 'get':
        cmd_get(args.site)
    elif args.command == 'list':
        cmd_list()
    elif args.command == 'delete':
        cmd_delete(args.site)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()