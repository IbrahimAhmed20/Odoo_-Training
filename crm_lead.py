# -*- coding: utf-8 -*-

from odoo import models, fields ,api

class CrmLead(models.Model):
    
    _inherit = 'crm.lead'
    
    next_call_date = fields.Date(string='Next Call Date')
    user_test = fields.Selection([
        ('admin', 'Admin'),
        ('demo', 'Demo')
    ], string="User Test")

 