from __future__ import absolute_import, division, print_function

__metaclass__ = type

import openstack

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import (
    const,
    resource,
)


class ServerGroup(resource.Resource):

    resource_type = const.RES_TYPE_SERVERGROUP
    sdk_class = openstack.compute.v2.server_group.ServerGroup

    info_from_sdk = [
        "id",
        "project_id",
        "user_id",
        "policies",
        "members",
    ]
    params_from_sdk = [
        "name",
        "policies",
    ]

    def _data_from_sdk_and_refs(self, sdk_res, refs):
        super()._data_from_sdk_and_refs(sdk_res, refs)
        self._sort_param("policies")
        self._sort_info("policies")
        self._sort_info("members")

    def _needs_update(self, target):  # pylint: disable=unused-argument
        # Server groups cannot be updated once created. If a server group with
        # the same name already exists we keep it as-is regardless of
        # differences.
        return False

    def _to_sdk_params(self, refs):
        sdk_params = super()._to_sdk_params(refs)
        # The Compute API does not accept caller-specified identifiers when
        # creating server groups; it generates them instead. Drop any values
        # provided under ``id`` or ``uuid`` so that we rely on Nova's
        # assignment and avoid unsupported request fields.
        sdk_params.pop("id", None)
        sdk_params.pop("uuid", None)
        return sdk_params

    @staticmethod
    def _create_sdk_res(conn, sdk_params):
        return conn.compute.create_server_group(**sdk_params)

    @staticmethod
    def _find_sdk_res(conn, name_or_id, filters=None):
        return conn.compute.find_server_group(name_or_id, **(filters or {}))

    @staticmethod
    def _update_sdk_res(conn, sdk_res, sdk_params):  # pylint: disable=unused-argument
        return sdk_res
