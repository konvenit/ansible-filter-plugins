# Ansible zip filter plugin
# Returns lists merged together with element pairing
# Works for regular lists and for lists of dicts as well
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Arguments available:
#
# longest=True (default False)
# Can be used when one list is longer than another. Result will be exteneded
# to the number of elements of the longest list. Works also for lists of dicts.
# See test_zip.py file to understand it thoroughly.
#
# Examples:
# {{ var1 | zip(var2, longest=True) }}
#
# var1:
#   - { name: hello, password: world }
# var2:
#  - { id: 1000 }
#  - { id: 2000 }
#
# var_zip: "{{ var1 | zip(var2, longest=True) }}"
# Result:
# var_zip:
#   - { name: hello, password: world, id: 1000 }
#   - { id: 2000 }
#
# var_zip: "{{ var1 | zip(var2, longest=False) }}"
# Result:
# var_zip:
#   - { name: hello, password: world, id: 1000 }
#
#
# fillvalue=None (default None)
# When used with longest surplus elements with this value
# See test_zip.py file to understand it thoroughly.
#
# var1: ['a', 'b', 'c']
# var2: ['d', 'e']
#
# var_zip: "{{ var1 | zip(var2, longest=True, fillvalue='NoLetter') }}"
# Result:
# var_zip:
#   - ['a', 'd']
#   - ['b', 'e']
#   - ['c', 'NoLetter']
#
# Example filter usage:
# users:
#   - { name: user1, password: hello }
#   - { name: user2, password: world }
# uids:
#   - { uid: 1000 }
#   - { uid: 2000 }
# users_with_uids: "{{ users | zip(uids) }}"
#
# Result would be:
# users_with_uids:
#  - { name: user1, password: hello, uid: 1000 }
#  - { name: user2, password: world, uid: 2000 }
#
# Sample playbook usage:
# NOTE: Additional filter 'todict' is used
#
# - hosts: localhost
#   vars:
#     users:
#       - { name: user1 }
#       - { name: user2 }
#   tasks:
#     - name: Get uids for users
#       command: id -u {{ item.name }}
#       register: uid_results
#       with_items: users
#
#     - set_fact:
#         uids: "{{ uid_results.results | map(attribute='stdout') | todict('uid') }}"
#
#     - set_fact:
#        users: "{{ users | zip(uids) }}"
#
#     - name: Show users with uids
#       debug: var=users
#
# Result:
#
# TASK [Show users with uids] ****************************************************
# ok: [localhost] => {
#     "users": [
#         {
#             "name": "user1",
#             "uid": "1000"
#         },
#         {
#             "name": "user2",
#             "uid": "2000"
#         }
#     ]
# }

from itertools import izip, izip_longest

def zipped(list1, list2, longest=False, fillvalue=None):
    if all([type(x) is dict for x in list1]):
        if longest:
            list1 = fill_list_with_empty_dicts(list1, length=len(list2))

        for idx, item in enumerate(list1):
            try:
                item2 = list2[idx]
                if type(item2) is dict:
                    list1[idx].update(item2)
            except IndexError:
                break
        return list1
    else:
        if longest:
            return list(izip_longest(list1, list2, fillvalue=fillvalue))

        return list(izip(list1, list2))

def fill_list_with_empty_dicts(array, length):
    if len(array) < length:
        diff = length - len(array)
        for i in range(0, diff):
            array.append({})

    return array


class FilterModule(object):
    def filters(self):
        return {
            'zip': zipped
        }
