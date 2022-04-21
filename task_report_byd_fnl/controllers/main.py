# -*- coding: utf-8 -*-
import datetime
import calendar
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta
import collections

from openerp import http
from openerp.http import request
import json
FILETYPE_BASE64_MAGICWORD = {
    b'/': 'jpg',
    b'R': 'gif',
    b'i': 'png',
    b'P': 'svg+xml',
}


class website_task_report(http.Controller):
    # A simple JSON Rest Controller is deployed in order to return the report data as asked in the test requirement
    # hard coded API Key is used for basic security
    @http.route(['/api/v1/<string:api_key>/get_task_report'], auth="public",website=False,
            type="json",
            csrf=False,
            methods = ['POST'])
    def get_task_report(self, api_key=None, **kwargs):
        # TODO Add token based auth for better security
        if api_key == 'hello1238888':
            today_date  = datetime.datetime.now().date()
            start_of_month = today_date.replace(day = 1)
            end_of_month = today_date.replace(day = calendar.monthrange(today_date.year, today_date.month)[1])
            date_7_days_ago = (datetime.datetime.now() - timedelta(days=7)).date()
            # This is sample format of query result.
            # we need to have left join here because project name and user name is not stored in their table
            # these names are stored on other tables i.e account_analytic_account and res_partner
            #      user      |   project   | open_count | delay_count | month_count | week_count 
            # ---------------+-------------+------------+-------------+-------------+------------
            request.env.cr.execute("""SELECT rp.name as user,al.name as project,
                sum(case when pty.stage_type not in ('done','cancel') then 1 else 0 end) AS open_count,
                sum(case when pty.stage_type not in ('done','cancel') and pt.date_deadline < %s then 1 else 0 end) 
                AS delay_count,
                sum(case when pt.date_done >= %s  and pt.date_done <= %s 
                and pty.stage_type = 'done'  then 1 else 0 end) AS month_count,
                sum(case when pt.date_done >= %s  and pt.date_done <= %s 
                and pty.stage_type = 'done'  then 1 else 0 end) AS week_count
                FROM project_task pt 
                LEFT JOIN  project_project pp ON pt.project_id = pp.id
                LEFT JOIN account_analytic_account al ON al.id = pp.analytic_account_id
                LEFT JOIN res_users ru ON ru.id = pt.user_id
                LEFT JOIN res_partner rp ON rp.id = ru.partner_id
                LEFT JOIN  project_task_type pty ON pt.stage_id = pty.id
                group by rp.name,al.name;""",(str(today_date),str(start_of_month),str(end_of_month),str(date_7_days_ago),str(today_date),))
            result = request.env.cr.dictfetchall()
            if result:
                _logger.info("===========%s",result)
                # here we have got the results grouped by user and project but still its not very json compatible
                #we are spliting the result by user and them by group project for each user for better json
                dres = collections.defaultdict(list)
                for d in result:
                    dres[d['user']].append(d)
                result_list = dres.values() 
                # this list has final result 
                qlist = []
                for data in result_list:
                    qdata = {}
                    qdata.update({'owner': data[0]['user']})
                    # list for projects for each owner
                    plist = []
                    for dtm in data:
                        del dtm['user']
                        plist.append(dtm)
                    qdata.update({'projects':plist})
                    qlist.append(qdata)
                # converting the result to json format
                _logger.info("===qlist====%s",qlist)
                # res = json.dumps(qlist)
                return (json.dumps(qlist)) 
        else:
            res = {"result":"Invalid API Key"}
            return json.dumps(res)       
             
    
    # We have introduced this controller in order to get tasks to show in report initially with no filter.
    @http.route('/get/tasks', type='http', auth='user')
    def get_all_task(self):
        res=[]
        tasks=request.env['project.task'].search([],order='id desc')
        if tasks:
            for task in tasks:
                # We are forming the image url to display.
                img_link = 'data:image/%s;base64,%s' % (
                    FILETYPE_BASE64_MAGICWORD.get(task.user_id.image[:1], 'png'),
                    task.user_id.image.decode())
                res.append({'img_link':[img_link,task.user_id.name,task.user_id.id],
                            'name': task.name,
                            'date_deadline': task.date_deadline,
                            'project':task.project_id.name,
                            'status': task.stage_id.name})
        return http.request.make_response(json.dumps(res,{
            'Cache-Control': 'no-cache', 
            'Content-Type': 'JSON; charset=utf-8',
            'Access-Control-Allow-Origin':  '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, X-Requested-With',

            })) 
    
    # We have introduced this controller in order to get data in popup for each user.
    @http.route('/get/<string:user_id>/user_data', type='http', auth='user')
    def get_all_task_by_user(self,user_id=None):
        if user_id:
            today_date  = datetime.datetime.now().date()
            start_of_month = today_date.replace(day = 1)
            end_of_month = today_date.replace(day = calendar.monthrange(today_date.year, today_date.month)[1])
            date_7_days_ago = (datetime.datetime.now() - timedelta(days=7)).date()
            #This is query which return the count of open task, delayed task, done this month,done last week 
            #for each user. This query is called when we click on user picture in report (Only once).
            #Query results are like:
            # project_id | open_count | delay_count | month_count | week_count 
            # ------------+------------+-------------+-------------+------------
            request.env.cr.execute("""SELECT al.name as project,
                        sum(case when pty.stage_type not in ('done','cancel') then 1 else 0 end) AS open_count,
                        sum(case when pty.stage_type not in ('done','cancel') and pt.date_deadline < %s then 1 else 0 end) 
                        AS delay_count,
                        sum(case when pt.date_done >= %s  and pt.date_done <= %s 
                        and pty.stage_type = 'done'  then 1 else 0 end) AS month_count,
                        sum(case when pt.date_done >= %s  and pt.date_done <= %s
                        and pty.stage_type = 'done'  then 1 else 0 end) AS week_count
                        FROM project_task pt 
                        LEFT JOIN project_project pp ON pt.project_id = pp.id
                        LEFT JOIN account_analytic_account al ON al.id = pp.analytic_account_id
                        LEFT JOIN res_users ru ON ru.id = pt.user_id
                        LEFT JOIN res_partner rp ON rp.id = ru.partner_id
                        LEFT JOIN  project_task_type pty ON pt.stage_id = pty.id
                        where pt.user_id = %s
                        group by al.name;""",(str(today_date),str(start_of_month),str(end_of_month),str(date_7_days_ago),str(today_date),user_id,))
            result = request.env.cr.dictfetchall()
            if result:
                return http.request.make_response(json.dumps(result,{
                'Cache-Control': 'no-cache', 
                'Content-Type': 'JSON; charset=utf-8',
                'Access-Control-Allow-Origin':  '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, X-Requested-With',
                })) 
            else:
                res = {"result":"something went wrong"}
                return http.request.make_response(json.dumps(res,{
                'Cache-Control': 'no-cache', 
                'Content-Type': 'JSON; charset=utf-8',
                'Access-Control-Allow-Origin':  '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, X-Requested-With',
                }))             
    
    