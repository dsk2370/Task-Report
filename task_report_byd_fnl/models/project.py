# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from openerp import models, fields, api, _
import datetime
import calendar
from datetime import timedelta

class ProjectTaskTypeInh(models.Model):
    _inherit = 'project.task.type'

    # We add this field so that, we can filter between stages as done,open and cancel stage
    stage_type = fields.Selection([('open','Open'), ('done','Done'), ('cancel','Cancel')],string='Stage Type',default='open')
    

class ProjectInherited(models.Model):
    _inherit = "project.task"

    # this field is added in order to detect and save which task were done 
    # on which date so that these date can be used in search filter of report.
    date_done = fields.Datetime(compute='_compute_date_done',string='Done Date',store=True)

    @api.one
    @api.depends('stage_id')
    def _compute_date_done(self):
        if self.stage_id.stage_type == 'done':
            self.date_done = self.date_last_stage_update
        else:
            self.date_done = False
