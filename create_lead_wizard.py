# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProjectLeadWizard(models.TransientModel):
    _name = 'project.lead.wizard'
    _description = 'Wizard to Create CRM Lead from Project'

    name = fields.Char(string="Lead Name", required=True)
    project_id = fields.Many2one('project.project', string="Project")

    def action_create_lead(self):
        self.env['crm.lead'].create({
            'name': self.name,
            'description': f'Created from Project: {self.project_id.name}',
        })
        return {'type': 'ir.actions.act_window_close'}
            