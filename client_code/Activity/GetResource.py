import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .Dependency import Module1
#
#    Module1.say_hello()
#

resources = {dep['resource'] for dep in anvil.server.call('get_resources')}

resources = sorted(list(resources))
