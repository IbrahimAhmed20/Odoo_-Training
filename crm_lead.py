# -*- coding: utf-8 -*-

from odoo import models, fields

class CrmLead(models.Model):
    
    _inherit = 'crm.lead' 
    next_call_date = fields.Date(string='Next Call Date')

