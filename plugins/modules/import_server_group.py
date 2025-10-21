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
module: import_server_group

short_description: Import OpenStack server group

extends_documentation_fragment:
  - os_migrate.os_migrate.openstack

version_added: "2.9.0"

author: "OpenStack tenant migration tools (@os-migrate)"

description:
  - "Import OpenStack server group from an OS-Migrate YAML structure"
notes:
  - "OpenStack assigns server group UUIDs when creating the resource; imports
    cannot request a specific UUID and a new one will always be generated."
  - "See the Compute API reference for the supported request body fields:
    https://docs.openstack.org/api-ref/compute/?expanded=create-server-group-detail#create-server-group"

options:
  auth:
    description:
      - Required if 'cloud' param not used.
    required: false
    type: dict
  auth_type:
    description:
      - Auth type plugin for OpenStack. Can be omitted if using password authentication.
    required: false
    type: str
  region_name:
    description:
      - OpenStack region name. Can be omitted if using default region.
    required: false
    type: str
  data:
    description:
      - Data structure with server group parameters as loaded from OS-Migrate YAML file.
    required: true
    type: dict
  filters:
    description:
      - Options for filtering existing resources to be looked up, e.g. by project.
      - Set ``all_projects`` to ``true`` to search across all projects when
        checking for an existing server group (admin only).
    required: false
    type: dict
  availability_zone:
    description:
      - Availability zone.
    required: false
    type: str
  cloud:
    description:
      - Clouds resource from clouds.yml
      - Required if 'auth' param not used.
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Import my server group into /opt/os-migrate/server_groups.yml
  os_migrate.os_migrate.import_server_group:
    cloud: destination_cloud
    data:
      type: openstack.compute.ServerGroup
      params:
        name: my-server-group
        policies:
          - anti-affinity
"""

RETURN = r"""
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

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import (
    server_group,
)


def run_module():
    argument_spec = openstack_full_argument_spec(
        data=dict(type="dict", required=True),
        filters=dict(type="dict", required=False, default={}),
    )
    # TODO: check the del
    # del argument_spec['cloud']

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        # TODO: Consider check mode. We'd fetch the resource and check
        # if the file representation matches it.
        # supports_check_mode=True,
    )

    sdk, conn = openstack_cloud_from_module(module)
    ser_server_group = server_group.ServerGroup.from_data(module.params["data"])
    result["changed"] = ser_server_group.create_or_update(
        conn, module.params["filters"]
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
