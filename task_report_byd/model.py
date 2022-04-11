# -*- coding: utf-8 -*-
import datetime
import calendar

import logging
_logger = logging.getLogger(__name__)
from openerp import models, fields, api, _
from datetime import timedelta
from collections import defaultdict
import json


class TaskReportByd(models.Model):
    _name = "task.report.byd"
    _description = "Task Report"
    _order = "id desc"

    #base Report Model to incorporate the required values
    task_id = fields.Many2one('project.task',string='Task',readonly=True,required=True)
    project_id = fields.Many2one('project.project',related='task_id.project_id',string='Project',readonly=True)
    stage_id = fields.Many2one('project.task.type',related='task_id.stage_id', string='Stage',domain="[('project_ids', '=', project_id)]", readonly=True)
    user_id =  fields.Many2one('res.users',related='task_id.user_id', string='Assigned to', readonly=True,store=True)
    date_deadline = fields.Date('Deadline',related='task_id.date_deadline', readonly=True)
    manager_id = fields.Many2one('res.users',related='task_id.manager_id', string='Manager', readonly=True)
    image = fields.Binary(related='user_id.image',string="Task Owner",readonly=True)
    name = fields.Char(related='user_id.name',string='Owner Name',readonly=True)
    qdata = fields.Text(compute='_compute_data',string='Query Data',readonly=True)

    @api.multi
    def _compute_data(self):
        for rec in self:             
            today_date  = datetime.datetime.now()
            start_of_month = today_date.replace(day = 1)
            end_of_month = today_date.replace(day = calendar.monthrange(today_date.year, today_date.month)[1])
            date_7_days_ago = datetime.datetime.now() - timedelta(days=7)
            open_count_objs = self.env['project.task'].read_group([('user_id','=',rec.user_id.id),('stage_id','not in',(7,8))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
            delay_count_objs = self.env['project.task'].read_group([('user_id','=',rec.user_id.id),('date_deadline','<',fields.date.today())], fields=['id','project_id'], groupby=['project_id'],lazy=False)
            fm_count_objs = self.env['project.task'].read_group([('user_id','=',rec.user_id.id),('stage_id','=',7),('date_done','>=',str(start_of_month)),('date_done','<=',str(end_of_month))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
            fw_count_objs = self.env['project.task'].read_group([('user_id','=',rec.user_id.id),('stage_id','=',7),('date_done','>=',str(date_7_days_ago)),('date_done','>=',str(today_date))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
            dat_lst = [] 
            if open_count_objs:
                for ln in open_count_objs:
                    dat_lst.append({
                        'Project': ln['project_id'][1],
                        'Open Tasks': ln['__count'],
                        })
            if delay_count_objs:
                for ln in delay_count_objs:
                    dat_lst.append({
                       'Project': ln['project_id'][1],
                        'Delay Tasks': ln['__count'],
                        })
            if fm_count_objs:
                for ln in fm_count_objs:
                    dat_lst.append({
                        'Project': ln['project_id'][1],
                        'This Month': ln['__count'],})
            if fw_count_objs:
                for ln in fw_count_objs:
                    dat_lst.append({
                        'Project': ln['project_id'][1],
                        'Last Week': ln['__count']})
            if dat_lst:
                d = defaultdict(dict)
                for item in dat_lst:
                    d[item['Project']].update(item)
                r1 = list(d.values())
                qdata = ''
                for dat in r1:
                    qdata += '\n'
                    qdata += "Project: " + str(dat['Project'])
                    if dat.has_key('Open Tasks'):
                        qdata += '  Open Tasks: ' + str(dat['Open Tasks'])
                    else:
                        qdata += '  Open Tasks: ' + '0' 

                    if dat.has_key('Delay Tasks'):
                        qdata += '  Delay Tasks: ' + str(dat['Delay Tasks'])
                    else:
                        qdata += '  Delay Tasks: ' + '0'

                    if dat.has_key('This Month'):
                        qdata += '  This Month: ' + str(dat['This Month'])
                    else:
                            qdata += '  This Month: ' + '0'

                    if dat.has_key('Last Week'):
                        qdata += '  Last Week: ' + str(dat['Last Week'])
                    else:
                        qdata += '  Last Week: ' + '0'
                # TODO improvise the view of the data on popup and add line breaks 
                rec.qdata = qdata