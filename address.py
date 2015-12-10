# Ansible address filter plugin
# Returns host name from hostname:port string
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# connection_string: 127.0.0.1:5432
# host: "{{ connection_string | address }}" # host=127.0.0.1

def address(value):
    return value.split(':', 2)[0]

class FilterModule(object):
    def filters(self):
        return {
            'address': address
        }
