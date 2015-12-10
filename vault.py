# Ansible port filter plugin
# Returns decrypted text from cipher text using secret key file
# Allows to get rid of plain text passwords in ansible repository
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Before use generate key file with command
# python filter_plugins/vault.py --key YOUR_SECRET_PASSWORD > vault.key
#
# Example usage:
# password_crypt: gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==
# password_plain: "{{ password_crypt | vault }}"
#
# or even:
# password: "{{ 'gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==' | vault }}"
#
# Filter commands for inline encrypting/decrypting:
# python filter_plugins/vault.py --encrypt 'secret value'
# python filter_plugins/vault.py --decrypt gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==

import os
import sys
import argparse
import base64
from ansible import errors
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KEY = 'vault.key'
SALT = os.urandom(16) # Set non-random salt if you want to recreate the same vault.key using the password in the future

def vault(cipher):
    try:
        f = fernet()
        return f.decrypt(bytes(cipher))
    except IOError:
        raise errors.AnsibleFilterError('vault: could not open secret file: {}. Please run vault.py filter with --key option first and save output to secret file.'.format(os.path.abspath(KEY)))
    except InvalidToken:
        raise errors.AnsibleFilterError('vault: could not decrypt variable. Invalid secret key.')
    except:
        raise errors.AnsibleFilterError('vault: unknown error: {} {}'.format(sys.exc_type, sys.exc_value))

def fernet():
    with open(KEY, 'rb') as f:
        key = f.read().rstrip()
        return Fernet(key)

class FilterModule(object):
    def filters(self):
        return {
            'vault': vault
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', metavar='PASSWORD', action='store', help='generate secret key from password')
    parser.add_argument('--encrypt', metavar='TEXT', action='store', help='encrypt string from plain text')
    parser.add_argument('--decrypt', metavar='CRYPT', action='store', help='decrypt string from cipher text')
    args = parser.parse_args()
    if args.key:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=SALT,
            iterations=1000000,
            backend=default_backend()
        )
        print base64.urlsafe_b64encode(kdf.derive(args.key))
    elif args.encrypt:
        f = fernet()
        print f.encrypt(args.encrypt)
    elif args.decrypt:
        f = fernet()
        print f.decrypt(args.decrypt)
