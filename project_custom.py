from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    customer_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    age = fields.Integer(string='Age')

    date_start = fields.Date(string='Start Date')
    date = fields.Date(string='End Date')
    worked_days = fields.Integer(string='Worked Days', compute='_compute_worked_days')

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age != 0 and not (16 <= rec.age <= 25):
                raise ValidationError("Age must be between 16 and 25, or 0.")

    @api.depends('date_start', 'date')
    def _compute_worked_days(self):
        for rec in self:
            if rec.date_start and rec.date:
                delta = (rec.date - rec.date_start).days + 1
                rec.worked_days = max(delta, 0)
            else:
                rec.worked_days = 0
    

    def action_open_create_lead_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Lead',
            'res_model': 'project.lead.wizard', 
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_project_id': self.id,
            }
        }
