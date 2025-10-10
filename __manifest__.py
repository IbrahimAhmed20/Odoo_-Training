# -*- coding: utf-8 -*-
{
    'name': 'crm_custom',
    'author': 'Ibrahim',
    'version': '1.0',
    'summary': 'New custom module',
    'category': 'Project',  
    'depends': [
        'base',
        'crm',
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}