# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Next Call Date field
    next_call_date = fields.Date(string='Next Call Date')

    # User Test field with specific selection options
    user_test = fields.Selection(
        [('admin', 'Admin'), ('demo', 'Demo')],
        string="User Test",
        required=True,
        groups="crm_custom.crm_lead_group_manager,crm_custom.crm_lead_group_user"
    )
    
    # Action to open the Print Lead Wizard
    def action_print_leads(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'print.lead.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
