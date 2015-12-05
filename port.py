# Ansible port filter plugin
# Returns port number from hostname:port string
#
# Example usage:
# connection_string: 127.0.0.1:5432
# port: "{{ connection_string | port }}" # port=5432
#
# Marcin Hlybin, ahes@sysadmin.guru

def port(value):
    return value.split(':', 2)[1]

class FilterModule(object):
    def filters(self):
        return {
            'port': port
        }
