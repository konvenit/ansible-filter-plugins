from ansible import errors

def isfalse(value, name=None):
    if name:
        message = name
    else:
        message = "Variable is false"

    if value:
        return value
    else:
        raise errors.AnsibleFilterError(message)

class FilterModule(object):
    def filters(self):
        return {
            'isfalse': isfalse
        }
