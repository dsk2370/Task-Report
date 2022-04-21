# -*- coding: utf-8 -*-
{
    'name': 'Project Task Report',
    'version': '8.0.1',
    'author': 'Sagar Jayswal',
    'website': 'https://sagarcs.com',
    'license': 'AGPL-3',
    'category': 'Project',
    'depends': [
       'base','web','project'
    ],
    
    'data': [
        'security/ir.model.access.csv',
        'view/assets.xml',
        'view/report_view.xml',
        'view/project_inherit.xml',
    ],
    'post_init_hook': 'my_post_init_hook',
    
}
