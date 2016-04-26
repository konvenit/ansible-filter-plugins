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

## defined ##
Raises error when variable is not defined or empty
Optional argument is name of the variable to display in error message

Example usage:
```
  - debug: msg="User id is {{ uid | defined }}"
  - debug: msg="User id is {{ uid | defined('uid') }}"

  Result1: FAILED! => {"failed": true, "msg": "Variable not defined"}
  Result2: FAILED! => {"failed": true, "msg": "Variable not defined: uid"}
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

## merge ##

Merges dict keys with defaults key __all__ recursively with merge lists support and excludes. See sample usage for details.

See `README` file in plugin directory for more details.

## port ##
Returns port number from `hostname:port` string

Example usage:
```
connection_string: 127.0.0.1:5432
port: "{{ connection_string | port }}" # port=5432
```

## todict ##
Returns list of dicts from list or list of lists

Example usage:
```
users:
  - [ 'user1', 'pwd1' ]
  - [ 'user2', 'pwd2' ]
users_dict: "{{ users | todict('name', 'password') }}"
```

Result is:
```
users_dict:
  - { name: user1, password: pwd1 }
  - { name: user2, password: pwd2 }
```

## tolist ##
Returns list from string or list

Example usage:

```
backup_templates: duplicity
backup_templates: ['duplicity', 'lvm']
- name: Copy backup templates
  template:
    src={{ item }}.j2
    dest=/etc/backup.d/{{ item }}
    owner=root
    group=root
    mode=0600
  with_items: "{{ backup_templates | tolist }}"
```

## vault ##

Returns decrypted text from cipher text using secret key file. Allows to get rid of plain text passwords in ansible repository without using ansible-vault nor encrypting whole files.

See `README` file in plugin directory for more details.

## zip ##

Aggregates matching elements from lists or lists of dicts.

See `README` file in filter directory
