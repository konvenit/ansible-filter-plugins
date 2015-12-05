# Ansible filename filter plugin
# Returns filename from path and cuts .j2 extension if available.
#
# Example usage:
# - name: Copy all template files at once
#   template:
#     src={{ item }}
#     dest=/etc/service/conf.d/{{ item | filename }}
#     owner=root
#     group=root
#     mode=0600
#   with_fileglob: ../templates/service/*.j2
#
# Marcin Hlybin, ahes@sysadmin.guru

import os

def filename(path):
    file = os.path.basename(path)
    if file.endswith('.j2'):
        return file[:-3]
    else:
        return file

class FilterModule(object):
    def filters(self):
        return {
            'filename': filename
        }
