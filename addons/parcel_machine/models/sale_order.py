# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_inpost = fields.Boolean('Delivery InPost', default=False)
    parcel_machine_id = fields.Many2one('parcel.machine', string='Parcel Delivery Address',
        help='Parcel Machine address for delivery.')
    zip = fields.Char(string="Postal code (zip)", compute='_compute_zip')

    @api.onchange('partner_id')
    def _onchange_partner_id_inpost(self):
        self.delivery_inpost = False
        self.parcel_machine_id = False


    #=== COMPUTE METHODS ===#

    @api.depends('partner_id')
    def _compute_zip(self):
        for wizard in self:
            wizard.zip = wizard.partner_id.zip
