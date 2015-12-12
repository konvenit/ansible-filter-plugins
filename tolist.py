# Ansible tolist filter plugin
# Returns list from string or list
#
# Marcin Hlybin, ahes@sysadmin.guru
#
# Example usage:
# backup_templates: duplicity
# backup_templates: ['duplicity', 'lvm']
# - name: Copy backup templates
#   template:
#     src={{ item }}.j2
#     dest=/etc/backup.d/{{ item }}
#     owner=root
#     group=root
#     mode=0600
#   with_items: "{{ backup_templates | tolist }}"

def tolist(value):
    if type(value) != list:
        return [value]
    else:
        return value

class FilterModule(object):
    def filters(self):
        return {
            'tolist': tolist
        }
