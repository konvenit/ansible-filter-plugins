# Ansible address filter plugin
# Returns host name from hostname:port string
#
# Example usage:
# connection_string: 127.0.0.1:5432
# host: "{{ connection_string | address }}" # host=127.0.0.1
#
# Marcin Hlybin, ahes@sysadmin.guru

def address(value):
    return value.split(':', 2)[0]

class FilterModule(object):
    def filters(self):
        return {
            'address': address
        }
