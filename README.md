# ansible-filter_plugins
Ansible filter plugins

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
