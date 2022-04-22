from openerp import models, fields, api,SUPERUSER_ID

# we introduced this new hook to run after install to create a record for view rendering
def my_post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['task.report'].create({'name':'Report'})
    # setting the stages to type done and cancel 
    done_stage_id = env['project.task.type'].search([('name','=','Done')],limit=1)
    cancel_stage_id = env['project.task.type'].search([('name','=','Cancel')],limit=1)
    if done_stage_id:
        done_stage_id.write({'stage_type':'done'})
    if cancel_stage_id:
        cancel_stage_id.write({'stage_type':'cancel'})
    # updating all task done date 
    all_done_tasks = env['project.task'].search([('stage_id.stage_type','=','done')])
    if all_done_tasks:
        for task in all_done_tasks:
            task.write({'date_done':task.date_last_stage_update})
