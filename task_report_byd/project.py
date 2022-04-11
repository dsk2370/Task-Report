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

    @api.one
    @api.depends('stage_id')
    def _compute_date_done(self):
        if self.stage_id.id == 7:
            self.date_done = self.date_last_stage_update
        else:
            self.date_done = False
