# Ansible byattr filter plugin
# Returns dict from list of dicts by attribute.
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# users:
#   - { name: john, uid: 1000, comment: John Doe }
#   - { name: bob,  uid: 1001, comment: Bob Smith }
#
# john: "{{ users | byattr('name', 'john') }}"
# john_uid:  "{{ john.uid }}"

def byattr(list, key, value, many=False):
    output = filter(lambda d: d[key] == value, list)
    if many:
        return output
    else:
        return output[0]

class FilterModule(object):
    def filters(self):
        return {
            'byattr': byattr
        }
