#!/usr/bin/python


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: os_server_groups_info

short_description: Get server groups info

extends_documentation_fragment:
  - os_migrate.os_migrate.openstack

version_added: "2.9.0"

author: "OpenStack tenant migration tools (@os-migrate)"

description:
  - "List server group information"

options:
  filters:
    description:
      - Options for filtering the server group info. Values are forwarded
        directly to ``conn.compute.server_groups``.
      - Set ``all_projects`` to ``true`` to search across all projects (admin
        only); otherwise only server groups visible within the scoped project
        are returned.
    required: false
    type: dict
  availability_zone:
    description:
      - Availability zone.
    required: false
    type: str
  cloud:
    description:
      - Cloud resource from clouds.yml file
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: List server groups information in the current project
  os_server_groups_info:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject

- name: List server groups accessible to an administrator across projects
  os_server_groups_info:
    cloud: admin_cloud
    filters:
      all_projects: true
"""

RETURN = r"""
openstack_server_groups:
    description: has all the openstack information about the server groups
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: str
"""

from ansible.module_utils.basic import AnsibleModule

# Import openstack module utils from ansible_collections.openstack.cloud.plugins as per ansible 3+
try:
    from ansible_collections.openstack.cloud.plugins.module_utils.openstack import (
        openstack_full_argument_spec,
        openstack_cloud_from_module,
    )
except ImportError:
    # If this fails fall back to ansible < 3 imports
    from ansible.module_utils.openstack import (
        openstack_full_argument_spec,
        openstack_cloud_from_module,
    )


def main():

    argument_spec = openstack_full_argument_spec(
        filters=dict(required=False, type="dict", default={}),
    )
    # TODO: check the del
    # del argument_spec['cloud']

    module = AnsibleModule(argument_spec)
    sdk, cloud = openstack_cloud_from_module(module)
    try:
        server_groups = list(
            map(
                lambda r: r.to_dict(),
                cloud.compute.server_groups(**module.params["filters"]),
            )
        )
        module.exit_json(changed=False, openstack_server_groups=server_groups)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
