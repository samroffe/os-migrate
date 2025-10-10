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
