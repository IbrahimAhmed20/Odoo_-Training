from odoo import models, fields, api
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string='Type Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The property type name must be unique.')
    ]
    
