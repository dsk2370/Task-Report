# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)

# This is wizard to take user form the UI for filtering the Report

class TaskReportWizardByd(models.TransientModel):
    _name = "task.report.wizard.byd"
    _description = "Task Report Wizard"

    user_ids =  fields.Many2many('res.users', string='Assigned to',select=True)
    
    @api.multi
    def show_report(self):
        for rec in self:
            if not rec.user_ids:
                All_Task = self.env['project.task'].search([])
            else:
                All_Task = self.env['project.task'].search([('user_id','in',rec.user_ids.ids)])
            if All_Task:
                _logger.info("-------all-task------%s",All_Task)
                rep_obj = self.env['task.report.byd']
                rep_obj.search([])
                self.env.cr.execute('delete from task_report_byd')
                for task in All_Task:
                    
                    rep_obj.create({
                        'task_id': task.id  
                    })
            return {
                'name': _('Task Report'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'task.report.byd',
                # 'view_id': self.env.ref('task_report_byd.view_task_report_byd_tree').id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
                
