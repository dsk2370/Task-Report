from openerp import models, fields, api
import datetime

# This is a basic class with just one record with aim to create kanban view.
class TaskReport(models.Model):
    _name = 'task.report'
     
    name = fields.Char('Name',required=True)