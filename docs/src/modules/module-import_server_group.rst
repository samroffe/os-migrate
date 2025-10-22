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

Server group names are not unique within a project. When OS-Migrate detects
multiple matches for the requested name, the importer treats the lookup as
"not found" and creates a fresh server group so migrations can succeed even in
tenants that already contain similarly named resources.
