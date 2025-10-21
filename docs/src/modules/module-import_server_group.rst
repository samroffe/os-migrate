============================
Module - import_server_group
============================


This module provides for the following ansible plugin:

    * import_server_group


.. ansibleautoplugin::
   :module: plugins/modules/import_server_group.py
   :documentation: true
   :examples: true

When importing resources, administrators can pass ``filters`` through the
module arguments to control how OS-Migrate searches for existing server groups.
For example, ``filters: {all_projects: true}`` expands the lookup to all
projects instead of only the project tied to the authentication scope.
