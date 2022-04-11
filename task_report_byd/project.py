import logging
_logger = logging.getLogger(__name__)
from openerp import models, fields, api, _
from datetime import date, datetime
class ProjectInherited(models.Model):
    _inherit = "project.task"
    _description = "Task Report"
    _order = "id desc"

    # this field is added in order to detect and save which task were compleded on which date
    
    date_done = fields.Datetime(compute='_compute_date_done',string='Done Date',store=True)

    @api.depends('stage_id')
    def _compute_date_done(self):
        for rec in self:
            if rec.stage_id == 7:
                rec.date_done = rec.date_last_stage_update
            else:
                rec.date_done = False
