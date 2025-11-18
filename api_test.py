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
    
    @http.route('/api/create_lead', type='json', methods=['POST'], csrf=False)
    def create_lead(self, **kw):
        name = kw.get('name')
        email = kw.get('email')
        phone = kw.get('phone')
        user_test = kw.get('user_test')
        user_id = request.uid
        user_obj = request.env['res.users'].sudo().search([('id', '=', user_id)])
        
        vals = {
            'name': name,
            'email_from': email,
            'phone': phone,
            'user_test': user_test,
        }
        
        new_lead = request.env['crm.lead'].with_user(user_obj).create(vals)
        args = {'success': True, 'code':200, 'message':'Lead created successfully..', 'id': new_lead.id}
        return args
    
    @http.route('/api/update_lead', type='json', auth='user')
    def update_lead(self, **kw):
        lead = request.env['crm.lead'].sudo().search([('id', '=', kw['id'])])
        if lead:
            lead.sudo().write(kw)
            args = {'success': True, 'code':200, 'message':'Lead updated..', 'Stage Name': lead.stage_id.name}
            return args
       