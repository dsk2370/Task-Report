from openerp.tests.common import TransactionCase
import datetime

class TestTaskDoneStage(TransactionCase):
    """Here we will test that wen we make the stage of task as done after
     setting one of the stage's stage_type as done if it gets the done_date or not."""

    def setUp(self):
        super(TestTaskDoneStage, self).setUp()
        
        self.task_model = self.registry('project.task')
        self.stage_model = self.registry('project.task.type')
        
    def test_case(self):
        cr, uid = self.cr, self.uid
        # lets search done the stage First
        stage_id = self.stage_model.search(cr, uid, [('name', '=', 'Done')])[0]
        if stage_id:
            stage_id.write({'stage_type':'done'})
        # lets create demo task 
        task_id = self.task_model.create(cr, uid, dict(name="Test Task"))
        # lets update demo task's state 
        if task_id:
            task_id.write({'stage_id':stage_id.id})
        # lets check if the date is in today's date
        today_date  = str(datetime.datetime.now().date())
        res =  str(datetime.datetime.strptime(task_id.date_done, "%Y-%m-%d %H:%M:%S").date())
        self.assertEquals(today_date,res, "The done date must be equal to today")