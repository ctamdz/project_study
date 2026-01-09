# -*- coding: utf-8 -*-
{
    'name': "Enmasys Project Study",

    'summary': "Project Study Management",

    'description': """
        Module để quản lý Project Study.
        - Tạo và quản lý các Study
        - Theo dõi trạng thái (To Do, In Progress, Review, Done)
        - Gán người phụ trách, deadline, tags
    """,

    
    'category': 'Services/Project Study',
    'version': '17.0.1.0.0',

  
    'depends': ['project'],

     'data': [
        'security/project_study_security.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/study_views.xml',
        'views/study_report_views.xml',
        'views/study_menus.xml',
    ],

    # Module icon
    'icon': '/project_study/static/description/icon.png',

    'installable': True,
    'application': True,  
    'auto_install': False,
    'license': 'LGPL-3',
}
