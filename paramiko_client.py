#! /usr/bin/env python3
import argparse
import paramiko
import pathlib

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("key", nargs=2, type=str)
    return parser.parse_args()

def main():
    args = parse_args()
    key = pathlib.Path(args.key[1])
    if not key.exists():
        raise FileNotFoundError
    
    client = paramiko.SSHClient()
    rsa = paramiko.RSAKey.from_private_key_file(str(key))
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("127.0.0.1", port = 2222, pkey=rsa, username="user")
    stdin, stdout, stderr = client.exec_command("echo Hello World")
    print(stdout.read().decode())
    client.close()
    

    # Alternate: Context manager
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect("127.0.0.1", port = 2222, pkey=rsa, username="user")
        stdin, stdout, stderr = ssh_client.exec_command("echo This is using context manager")
        print(stdout.read().decode())

if __name__ == "__main__":
    main()