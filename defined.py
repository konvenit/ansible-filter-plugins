# Ansible defined filter plugin
# Raises error when variable is not defined or empty
# Optional argument is name of the variable to display in error message
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# - debug: msg="User id is {{ uid | defined }}"
# - debug: msg="User id is {{ uid | defined('uid') }}"
#
# Result1: FAILED! => {"failed": true, "msg": "Variable not defined"}
# Result2: FAILED! => {"failed": true, "msg": "Variable not defined: uid"}
#
from ansible import errors

def defined(value, name=None):
    if name:
        message = "Variable not defined: {}".format(name)
    else:
        message = "Variable not defined"

    if value in (None, ''):
        raise errors.AnsibleFilterError(message)

    return value

class FilterModule(object):
    def filters(self):
        return {
            'defined': defined
        }
