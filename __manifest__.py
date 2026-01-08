# -*- coding: utf-8 -*-
{
    'name': 'Estate Manager',
    'version': '1.0',
    'summary': 'Real Estate Property Management',
    'description': 'A module for managing real estate properties',
    'category': 'Real Estate',
    'author': 'Ibrahim',
    'website': 'https://www.example.com',
    'depends': ['base', 'website'],
    'data': [
        'security/security.xml',  # Security and Access Control
        'security/ir.model.access.csv',  # Access rights for models
        'views/templates.xml',  # Report action and template registration
        'views/estate_property_views.xml',  # Views for property records
        'views/estate_property_menus.xml',  # Menus for the estate module
        'views/estate_property_sequence.xml',  # Sequences, if applicable (e.g., for property codes)
    ],
    'application': True,
    'installable': True,
}

