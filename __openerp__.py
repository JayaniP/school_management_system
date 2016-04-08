# -*- coding: utf-8 -*-

{
   'name': 'School Management',
   'version': '1.0',
   'category': 'School Management',
   'depends': ['base', 'project', 'sale'],
   'data': [
        'views/school.xml',
        'views/calculator.xml',
        'wizard/wiz_calc_age_view.xml',
        'wizard/wiz_active.xml',
        'school_sequence.xml',
        'views/student_report.xml',
        'views/student_template_report.xml',
        'views/custom_report.xml',
        'views/custom_report_template.xml'
    ],
   'installable': True,
   'auto_install': False,
   'application': True,
}
