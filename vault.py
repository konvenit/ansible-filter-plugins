from __future__ import print_function

# Ansible port filter plugin
# Returns decrypted text from cipher text using secret key file
# Allows to get rid of plain text passwords in ansible repository
# without using ansible-vault and encrypting whole files
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Configuration options in ansible.cfg
# vault_filter_key = vault.key
# vault_filter_salt = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 # do not use this one, generate with '--salt' option
# vault_filter_iterations = 1000000
# vault_password_file = vault.pass # this is from ansible-vault, if specified vault filter will use this password to generate vault filter key
#
# How to use:
# 1. generate salt and put it to ansible.cfg file
#    python filter_plugins/vault.py --salt MY_RANDOM_SALT_STRING
#
# 2. generate key file (you will be asked for password if vault_password_file is not defined)
#    python filter_plugins/vault.py --key
#
# 3. encrypt password to be used in hostvar
#    python filter_plugins/vault.py --encrypt my_secret_password_to_database
#
# 4. store encrypted password in hostvars
#    vars:
#      db_password: {{ 'gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=' | vault }}
#
# 5. when needed you may decrypt password
#    python filter_plugins/vault.py --decrypt gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=
#
# Example variable formats in hostvars:
# password_crypt: gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=
# password_plain: "{{ password_crypt | vault }}"
# password: "{{ 'gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=' | vault }}"

import os
import sys
import argparse
import base64
import getpass
import binascii
import ansible.constants as C
from ansible import errors
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_FILTER_KEY = C.get_config(C.p, C.DEFAULTS, 'vault_filter_key', 'ANSIBLE_VAULT_FILTER_KEY', 'vault.key', ispath=True)
VAULT_FILTER_SALT = C.get_config(C.p, C.DEFAULTS, 'vault_filter_salt', 'ANSIBLE_VAULT_FILTER_SALT', None)
VAULT_FILTER_ITERATIONS = C.get_config(C.p, C.DEFAULTS, 'vault_filter_iterations', 'ANSIBLE_VAULT_FILTER_ITERATIONS', 1000000, integer=True)

vault_filter_key = os.path.abspath(VAULT_FILTER_KEY)

def vault(cipher):
    try:
        f = fernet()
        return f.decrypt(bytes(cipher))
    except IOError:
        raise errors.AnsibleFilterError('vault: could not open secret file: {}. Please run vault.py filter file with --key option first.'.format(vault_filter_key))
    except InvalidToken:
        raise errors.AnsibleFilterError('vault: could not decrypt variable. Invalid secret key.')
    except:
        raise errors.AnsibleFilterError('vault: unknown error: {} {}'.format(sys.exc_type, sys.exc_value))

def fernet():
    with open(vault_filter_key, 'rb') as f:
        key = f.read().rstrip()
        return Fernet(key)

def vault_key():
    if not VAULT_FILTER_SALT:
        print("ERROR: Variable 'vault_filter_salt' is not set in ansible.cfg file. Please generate salt with '--salt' option.")

    if os.path.isfile(vault_filter_key):
        print("ERROR: Vault filter key '{}' already exists. Remove it first to generate new one.".format(vault_filter_key))
        sys.exit(1)

    print("Vault filer key '{}' not found".format(vault_filter_key))
    if C.DEFAULT_VAULT_PASSWORD_FILE:
        print("Generating vault filter key from ansible vault password file")
        with open(C.DEFAULT_VAULT_PASSWORD_FILE, 'rb') as f:
            vault_password = f.read().rstrip()
    else:
        print("Generating vault filter key using user password")
        vault_password = getpass.getpass('Password: ')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=bytes(VAULT_FILTER_SALT),
        iterations=VAULT_FILTER_ITERATIONS,
        backend=default_backend()
    )
    vault_key = base64.urlsafe_b64encode(kdf.derive(vault_password))

    with open(vault_filter_key, 'wb') as f:
        os.chmod(vault_filter_key, 0o600)
        f.write(vault_key + '\n')

class FilterModule(object):
    def filters(self):
        return {
            'vault': vault
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--salt', action='store', help='generate vault filter salt for ansible.cfg config')
    parser.add_argument('--key', action='store_true', help='generate secret key from password prompt or using ansible vault password')
    parser.add_argument('--encrypt', metavar='TEXT', action='store', help='encrypt string from plain text')
    parser.add_argument('--decrypt', metavar='CRYPT', action='store', help='decrypt string from cipher text')
    args = parser.parse_args()

    if args.key:
        vault_key()
    elif args.salt:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(args.salt)
        print("Save following line to ansible.cfg config file under [defaults]:")
        print("vault_filter_salt = {}".format(binascii.b2a_hex(digest.finalize())))
    elif not os.path.isfile(vault_filter_key):
        print ("Vault filter key '{}' not found. Please create it first with '--key' option.".format(vault_filter_key))
        sys.exit(1)
    elif args.encrypt:
        f = fernet()
        print(f.encrypt(args.encrypt))
    elif args.decrypt:
        f = fernet()
        print(f.decrypt(args.decrypt))
