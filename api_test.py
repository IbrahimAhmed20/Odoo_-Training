import json
import werkzeug.wrappers
from odoo.exceptions import AccessError, MissingError, AccessDenied
from odoo import http
from odoo.http import request

class Accesstoken(http.Controller):
    @http.route('/api/login', type='json', auth='none', methods=['POST'], csrf=False)
    def get_accesstoken(self, **kw):
        data = kw or request.get_json_data()
        
        username = data.get('login')
        password = data.get('password')
        db = request.session.db or request.env.cr.dbname
        
        user = request.env['res.users'].sudo().search([('login', '=ilike', username)], limit=1)
        if not user:
            response = {
                'status': 'error',
                'message': 'Invalid credentials {user not found}'
            }
            return response
        try:
            uid = request.session.authenticate(db, username, password)
            if uid:
                response = {
                    'status': 'success',
                    'uid': uid,
                    'session_id': request.session.sid,
                }
            else:
                response = {'status': 'error', 'message': 'Invalid credentials'}
                
                return response
            
        except AccessDenied:
            response = {'status': 'error', 'error': 'Invalid credentials'}
            return response
        except Exception as e:       
         response = {'status': 'error', 'message': str(e)}
        return response
    

class PropertyApiController(http.Controller):

    @http.route('/api/v1/properties',type='json',auth='public',methods=['GET'],csrf=False)
    def get_properties(self):
        # Search for properties available on the web
        properties = request.env['estate.property'].sudo().search([
            ('available_on_web', '=', True)
        ])

        # Read all available fields
        data = properties.read()

        return data