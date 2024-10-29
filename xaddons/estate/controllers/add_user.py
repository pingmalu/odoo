from odoo import http
from odoo.http import request
import json

class GreetingController(http.Controller):
    @http.route('/api/contact/create', type='json', auth='public', methods=['POST'], csrf=False)
    def add_crm_user(self, **kwargs):
        data = json.loads(request.httprequest.data.decode('utf-8'))

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return {'status': 'error', 'message': 'Name and email are required.'}

        try:
            user = request.env['res.partner'].sudo().create({
                'name': name,
                'email': email,
            })
            return {'status': 'success', 'user_id': user.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
