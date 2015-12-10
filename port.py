# Ansible port filter plugin
# Returns port number from hostname:port string
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# connection_string: 127.0.0.1:5432
# port: "{{ connection_string | port }}" # port=5432

def port(value):
    return value.split(':', 2)[1]

class FilterModule(object):
    def filters(self):
        return {
            'port': port
        }
