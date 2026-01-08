from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    
    # Define the fields
    name = fields.Char('The Property Title', required=True)
    property_code = fields.Char('The sequence code', readonly=True)
    expected_price = fields.Float('The listing price')
    available_on_web = fields.Boolean('Available on Web')
    sales_agent_id = fields.Many2one('res.users', 'Sales Agent')
    creation_date = fields.Date('Creation Date', default=fields.Date.today)
    sales_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Sales State') 
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    commission_amount = fields.Float(string='Commission Amount', compute='_compute_commission', store=True)
    # Automatically create property_code
    @api.model
    def create(self, vals):
        if not vals.get('property_code'):
            vals['property_code'] = self.env['ir.sequence'].next_by_code('estate.property.code')
        return super(EstateProperty, self).create(vals)

    # Compute the commission amount based on expected price
    @api.depends('expected_price')
    def _compute_commission(self):
        for record in self:
            if record.expected_price:
                record.commission_amount = record.expected_price * 0.06

    # Prevent negative price
    @api.constrains('expected_price')
    def _check_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError('The expected price cannot be negative.')

    # Automatically set sales_state to 'draft' when expected_price is modified
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        if self.expected_price:
            self.sales_state = 'draft'

    # Ensure that property names are unique
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError(f"The property name '{record.name}' must be unique.")
            
  # Action method to print the report
    def action_print_property_report(self):
        return self.env.ref('estate_manager.action_report_property').report_action(self)