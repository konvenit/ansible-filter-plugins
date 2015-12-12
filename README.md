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

It is completely save to keep salt value in ansible.cfg - you can push it to your repository.

It is *NOT* save to keep vault key in repository! Add it to .gitignore
