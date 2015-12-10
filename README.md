# Ansible filter plugins

## address ##
Returns host name from `hostname:port` string

Example usage:
```
connection_string: 127.0.0.1:5432
host: "{{ connection_string | address }}" # host=127.0.0.1
```

See also [port](#port).

## byattr ##
Returns dict from list of dicts by attribute.

Example usage:
```
users:
  - { name: john, uid: 1000, comment: John Doe }
  - { name: bob,  uid: 1001, comment: Bob Smith }

john: "{{ users | byattr('name', 'john') }}"
john_uid:  "{{ john.uid }}"
```

## filename ##
Returns filename from path and trims `.j2` extension if available.

Example usage:
```
- name: Copy all template files at once
  template:
    src={{ item }}
    dest=/etc/service/conf.d/{{ item | filename }}
    owner=root
    group=root
    mode=0600
  with_fileglob: ../templates/service/*.j2
```

## port ##
Returns port number from `hostname:port` string

Example usage:
```
connection_string: 127.0.0.1:5432
port: "{{ connection_string | port }}" # port=5432
```

## vault ##
Returns decrypted text from cipher text using secret key file. Allows to get rid of plain text passwords in ansible repository.

Before first use generate key file with command:

```python filter_plugins/vault.py --key YOUR_SECRET_PASSWORD > vault.key```

Example usage:

```
password_crypt: gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==
password_plain: "{{ password_crypt | vault }}"
```
or even:

```
password: "{{ 'gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==' | vault }}"
```

Filter commands for inline encrypting/decrypting:


```
python filter_plugins/vault.py --encrypt 'secret value'
python filter_plugins/vault.py --decrypt gAAAAABWaAzLMEGfSUlgU3gDKJZmclNZrhr3Kz0Ev9zKCeskdkaGzdDTwC1XKtHeF1jClHRJ7SFJXYxo5l0wx1nX_4g7zA5nrw==
```
