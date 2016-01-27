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
Returns decrypted text from cipher text using secret key file. Allows to get rid of plain text passwords in ansible repository without using `ansible-vault` and encrypting whole files

Configuration options in ansible.cfg - notice section name *filters*:

```
[filters]
vault_filter_key = vault.key # might be relative or absolute path
vault_filter_salt = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 # generate random salt with '--salt' option
vault_filter_iterations = 1000000 # PBKDF2-SHA512 iterations
vault_filter_generate_key = yes # automatically generate vault key during playbook runtime

[defaults]
vault_password_file = vault.pass # this is from ansible-vault, if specified vault filter will use this password to generate vault filter key
```

How to use:

* generate random salt and put it to ansible.cfg file: `python filter_plugins/vault.py --salt`
* generate key file (you will be asked for password if vault_password_file is not defined): `python filter_plugins/vault.py --key`
* encrypt password to be used in hostvar: `python filter_plugins/vault.py --encrypt my_secret_password_to_database`
* store encrypted password in hostvars:
```
    vars:
      db_password: {{ 'gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=' | vault }}
```
* when needed you may decrypt password: `python filter_plugins/vault.py --decrypt gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=`

If you set you set `vault_filter_generate_key = yes` and `vault_password_file` option is present and vault filter salt is defined in ansible.cfg vault key file will be generated automatically without any message while playbook is running. This option can be useful with Ansible Tower. It might be a good idea to remove vault key in post_tasks in your playbook.

Example variable formats in hostvars:

```
password_crypt: gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=
password_plain: "{{ password_crypt | vault }}"
password: "{{ 'gAAAAABWasKsAvkyCqmc_8p57vGHOHkAG4nU4vo8t6n6C-j3hItbiwC1BRLnrHBJtrDP1Rz2wG1HULRG_zkXF596H0dn-69S92Ky3ixDOCAGesFptH1-glQ=' | vault }}"
```

It is completely safe to keep salt value in ansible.cfg - you can push it to your repository.

It is *NOT* safe to keep vault key in repository! Add it to .gitignore

## zip ##
Returns lists merged together with element pairing. Works for regular lists and for lists of dicts as well.

Arguments available:

*longest=True* (default False)

Can be used when one list is longer than another. Result will be exteneded
to the number of elements of the longest list. Works also for lists of dicts.

See `test_zip.py` file to understand it thoroughly.

Examples:
```
{{ var1 | zip(var2, longest=True) }}

var1:
  - { name: hello, password: world }
var2:
 - { id: 1000 }
 - { id: 2000 }

var_zip: "{{ var1 | zip(var2, longest=True) }}"
Result:
var_zip:
  - { name: hello, password: world, id: 1000 }
  - { id: 2000 }

var_zip: "{{ var1 | zip(var2, longest=False) }}"
Result:
var_zip:
  - { name: hello, password: world, id: 1000 }
```

*fillvalue=None* (default None/null)

When used with longest surplus elements with this value.

See test_zip.py file to understand it thoroughly.

Examples:
```
var1: ['a', 'b', 'c']
var2: ['d', 'e']

var_zip: "{{ var1 | zip(var2, longest=True, fillvalue='NoLetter') }}"
Result:
var_zip:
  - ['a', 'd']
  - ['b', 'e']
  - ['c', 'NoLetter']
```

### Example filter usage ###
```
users:
  - { name: user1, password: hello }
  - { name: user2, password: world }
uids:
  - { uid: 1000 }
  - { uid: 2000 }
users_with_uids: "{{ users | zip(uids) }}"
```

Result would be:
```
users_with_uids:
  - { name: user1, password: hello, uid: 1000 }
  - { name: user2, password: world, uid: 2000 }
```

### Sample playbook usage ###

NOTE: Additional filter 'todict' is used.
```
- hosts: localhost
  vars:
    users:
      - { name: user1 }
      - { name: user2 }
  tasks:
    - name: Get uids for users
      command: id -u {{ item.name }}
      register: uid_results
      with_items: users

    - set_fact:
        uids: "{{ uid_results.results | map(attribute='stdout') | todict('uid') }}"

    - set_fact:
        users: "{{ users | zip(uids) }}"

    - name: Show users with uids
      debug: var=users
```

Result:
```
TASK [Show users with uids] ****************************************************
ok: [localhost] => {
    "users": [
        {
            "name": "user1",
            "uid": "1000"
        },
        {
            "name": "user2",
            "uid": "2000"
        }
    ]
}
```
