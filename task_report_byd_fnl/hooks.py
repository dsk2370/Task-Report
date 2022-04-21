from openerp import models, fields, api,SUPERUSER_ID

# we introduced this new hook to run after install to create a record for view rendering
def my_post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['task.report'].create({'name':'Report'})
