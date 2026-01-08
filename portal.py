from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.tools.translate import _
import json

class DisplayPropertyPortal(CustomerPortal):
  
    @http.route(['/my/properties'], type='http', auth='user', website=True)
    def portal_my_properties(self, **kw):
        """Display a list of properties for the logged-in user."""
        user = request.env.user
        properties = request.env['estate.property'].search([('sales_agent_id', '=', user.id)])
        
        values = {
            'properties': properties,
        }
        return request.render('estate_manager.portal_my_properties', values)
