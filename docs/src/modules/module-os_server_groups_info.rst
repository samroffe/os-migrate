==============================
Module - os_server_groups_info
==============================


This module provides for the following ansible plugin:

    * os_server_groups_info


.. ansibleautoplugin::
   :module: plugins/modules/os_server_groups_info.py
   :documentation: true
   :examples: true

Usage
-----

The :doc:`../roles/role-export_server_groups` role invokes this module to
discover server groups prior to exporting them. Its first task is shown
below:

.. literalinclude:: ../../roles/export_server_groups/tasks/main.yml
   :language: yaml
   :lines: 1-9

The module accepts a ``filters`` dictionary that is passed straight to the
OpenStack SDK's :meth:`conn.compute.server_groups` call. For example, an
administrator can set ``filters: {all_projects: true}`` to look up server
groups outside the currently scoped project, while the default behavior only
returns resources visible within the authenticated project.
