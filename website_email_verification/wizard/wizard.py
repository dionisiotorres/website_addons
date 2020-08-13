from odoo import api, fields, models, _

class WizardMessage(models.TransientModel):
    _name = "wizard.message"
	
    text = fields.Text('Message')