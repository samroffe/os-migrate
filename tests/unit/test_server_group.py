from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

import openstack

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import (
    const,
    server_group,
)


def sdk_server_group():
    return openstack.compute.v2.server_group.ServerGroup(
        id="uuid-server-group",
        project_id="uuid-project",
        user_id="uuid-user",
        name="test-group",
        policies=["soft-anti-affinity", "anti-affinity"],
        members=["server-b", "server-a"],
    )


def serialized_server_group():
    return {
        const.RES_TYPE: const.RES_TYPE_SERVERGROUP,
        const.RES_PARAMS: {
            "name": "test-group",
            "policies": ["anti-affinity"],
        },
        const.RES_INFO: {
            "id": "uuid-server-group",
            "project_id": "uuid-project",
            "user_id": "uuid-user",
            "policies": ["anti-affinity"],
            "members": ["server-a"],
        },
    }


class TestServerGroup(unittest.TestCase):
    def test_serialize_server_group(self):
        sg = server_group.ServerGroup.from_sdk(None, sdk_server_group())
        params, info = sg.params_and_info()

        self.assertEqual(sg.type(), const.RES_TYPE_SERVERGROUP)
        self.assertEqual(params["name"], "test-group")
        self.assertEqual(params["policies"], ["anti-affinity", "soft-anti-affinity"])
        self.assertEqual(info["id"], "uuid-server-group")
        self.assertEqual(info["project_id"], "uuid-project")
        self.assertEqual(info["user_id"], "uuid-user")
        self.assertEqual(info["policies"], ["anti-affinity", "soft-anti-affinity"])
        self.assertEqual(info["members"], ["server-a", "server-b"])

    def test_serialize_server_group_handles_none_lists(self):
        sdk_obj = openstack.compute.v2.server_group.ServerGroup(
            id="uuid-empty-group",
            project_id="uuid-project",
            user_id="uuid-user",
            name="empty-group",
            policies=None,
            members=None,
        )

        sg = server_group.ServerGroup.from_sdk(None, sdk_obj)
        params, info = sg.params_and_info()

        self.assertEqual(params["policies"], [])
        self.assertEqual(info["policies"], [])
        self.assertEqual(info["members"], [])

    def test_server_group_never_needs_update(self):
        ser = server_group.ServerGroup.from_data(serialized_server_group())
        other_data = serialized_server_group()
        other_data[const.RES_PARAMS]["policies"] = ["soft-anti-affinity"]
        target = server_group.ServerGroup.from_data(other_data)

        self.assertFalse(ser._needs_update(target))

    def test_sdk_params_drop_identifiers(self):
        ser = server_group.ServerGroup.from_data(serialized_server_group())
        ser.params()["id"] = "provided-id"
        ser.params()["uuid"] = "provided-uuid"
        ser.params_from_sdk = ["name", "policies", "id", "uuid"]

        sdk_params = ser._to_sdk_params({})

        self.assertEqual(sorted(sdk_params.keys()), ["name", "policies"])
        self.assertEqual(sdk_params["name"], "test-group")
        self.assertEqual(sdk_params["policies"], ["anti-affinity"])

    def test_find_sdk_res_ignores_duplicate_matches(self):
        class FakeCompute:
            @staticmethod
            def find_server_group(name_or_id, **kwargs):  # pylint: disable=unused-argument
                raise openstack.exceptions.DuplicateResource("duplicate")

        class FakeConnection:
            compute = FakeCompute()

        result = server_group.ServerGroup._find_sdk_res(
            FakeConnection(), "test-group", None
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
