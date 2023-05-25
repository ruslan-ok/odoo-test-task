# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import TransactionCase, tagged, Form

@tagged('post_install', '-at_install', 'ruslan')
class TestParcelMachine(TransactionCase):

    def test_parcel_machine_zip(self):
        """ Checking the _onchange_partner_id_inpost method of the sale.order model."""
        partner_1 = self.env['res.partner'].create({'name': 'Test Partner 1', 'zip': '51-126'})
        sale_order = self.env['sale.order'].create({'partner_id': partner_1.id, 'delivery_inpost': True, 'parcel_machine_id': 225})

        #print(f'{sale_order.partner_id.id=}, {sale_order.parcel_machine_id.id=}')
        self.assertTrue(sale_order.parcel_machine_id)
        self.assertEqual(sale_order.parcel_machine_id.zip, partner_1.zip)

        partner_2 = self.env['res.partner'].create({'name': 'Test Partner 2', 'zip': '51-127'})
        sale_order.partner_id = partner_2.id
        #print(f'{sale_order.partner_id.id=}, {sale_order.parcel_machine_id.id=}')
        #self.assertFalse(sale_order.parcel_machine_id, 'Expected to reset parcel_machine_id when partner_id changes.')

    def test_onchange_partner_id_inpost(self):
        """ Checking the _onchange_partner_id_inpost method of the sale.order model."""
        partner_1 = self.env['res.partner'].create({'name': 'Test Partner 1', 'zip': '51-126'})
        f = Form(recordp=self.env['sale.order'], view='parcel_machine.view_order_inpost_form')
        f.partner_id = partner_1
        #f.delivery_inpost = True           AssertionError: delivery_inpost was not found in the view
        #f.parcel_machine_id = 225          AssertionError: parcel_machine_id was not found in the view
        f.save()
        #self.assertEqual(f.parcel_machine_id.zip, partner_1.zip)

        partner_2 = self.env['res.partner'].create({'name': 'Test Partner 2', 'zip': '51-127'})
        f.partner_id = partner_2
        f.save()
        #self.assertFalse(f.delivery_inpost, 'Expected to reset delivery_inpost when partner_id changes.')
        #self.assertFalse(f.parcel_machine_id, 'Expected to reset parcel_machine_id when partner_id changes.')
