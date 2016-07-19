# Ansible todict filter plugin
# Returns list of dicts from list or list of lists
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# users:
#   - [ 'user1', 'pwd1' ]
#   - [ 'user2', 'pwd2' ]
# users_dict: "{{ users | todict('name', 'password') }}"
#
# Result is:
# users_dict:
#   - { name: user1, password: pwd1 }
#   - { name: user2, password: pwd2 }

def todict(array, *keys):
    output = []
    for item in array:
        if type(item) is not list:
            item = [item]
        d = dict.fromkeys(keys)
        for idx, k in enumerate(keys):
            try:
                v = item[idx]
            except IndexError:
                v = None
            d.update({ k: v })
        output.append(d)

    return output

class FilterModule(object):
    def filters(self):
        return {
            'todict': todict,
            'to_dict': todict
        }
