# -*- coding: utf-8 -*-
import datetime
import calendar

import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta
from collections import defaultdict
from openerp import fields

from openerp import http
from openerp.http import request
import json

# A simple JSON Rest Controller is deployed in order to return the report data
# hard coded API Key is used for basic security
class website_task_report(http.Controller):
    
    @http.route(['/api/v1/<string:api_key>/get_task_report'], auth="public",website=False,
            type="json",
            csrf=False,
            methods = ['POST'])
    def get_task_report(self, api_key=None, **kwargs):
        # TODO Add token based auth 
        if api_key == 'hello1238888':
            task_owners = request.env['res.users'].sudo().search([('share','=',False)])
            dat_lst = []
            res_lst = []
            _logger.info("===========%s",task_owners)
            if task_owners:
                for owner in task_owners:
                    qdata_list = []
                    today_date  = datetime.datetime.now()
                    start_of_month = today_date.replace(day = 1)
                    end_of_month = today_date.replace(day = calendar.monthrange(today_date.year, today_date.month)[1])
                    date_7_days_ago = datetime.datetime.now() - timedelta(days=7)
                    open_count_objs = request.env['project.task'].sudo().read_group([('user_id','=',owner.id),('stage_id','not in',(7,8))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
                    delay_count_objs = request.env['project.task'].sudo().read_group([('user_id','=',owner.id),('date_deadline','<',fields.date.today())], fields=['id','project_id'], groupby=['project_id'],lazy=False)
                    fm_count_objs = request.env['project.task'].sudo().read_group([('user_id','=',owner.id),('stage_id','=',7),('date_done','>=',str(start_of_month)),('date_done','<=',str(end_of_month))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
                    fw_count_objs = request.env['project.task'].sudo().read_group([('user_id','=',owner.id),('stage_id','=',7),('date_done','>=',str(date_7_days_ago)),('date_done','>=',str(today_date))], fields=['id','project_id'], groupby=['project_id'],lazy=False)
                    _logger.info("===========%s",open_count_objs)
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
                                'This Month': ln['__count'],
                                })
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
                        qdata = {}
                        
                        for dat in r1:
                            qdata.update({ "Project" : str(dat['Project'])})
                            
                            if dat.has_key('Open Tasks'):
                                qdata.update({"Open Tasks" : str(dat['Open Tasks'])}) 
                            else:
                                qdata.update({"Open Tasks" : '0'})
                            
                            if dat.has_key('Delay Tasks'):
                                qdata.update({"Delay Tasks" : str(dat['Delay Tasks'])})
                            else:
                                qdata.update({"Delay Tasks" : '0'})
                            
                            if dat.has_key('This Month'):
                                qdata.update({"This Month" : str(dat['This Month'])})
                            else:
                                qdata.update({"This Month" : '0'})
                                
                            if dat.has_key('Last Week'):
                                qdata.update({"Last Week" : str(dat['Last Week'])})
                            else:
                                qdata.update({"Last Week" : '0'})
                            qdata_list.append(qdata)
                    res_lst.append({
                            'owner' : owner.name,
                            'task_details': qdata_list,
                        })
                return json.dumps(res_lst) 
        else:
            return json.dumps({"result":"Invalid API Key"}) 
