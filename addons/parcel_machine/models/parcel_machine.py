# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ParcelMachine(models.Model):
    """ Model for a Parcel Machine.
        Parcel Machine is an automated postal box that allows users
        for a self-service collection of parcels and oversize letters
        as well as the dispatch of parcels.
    """
    _name = 'parcel.machine'
    _description = 'Parcel Machine'
    _rec_name = 'code'
    _order = 'code'
    _rec_names_search = ['code', 'city', 'street', 'building', 'zip', 'description']

    code = fields.Char('Code', required=True)
    description = fields.Char('Description')
    city = fields.Char('City', required=True)
    city_eng = fields.Char('City in English', required=True)
    street = fields.Char('Street', required=True)
    area = fields.Char('Area', required=True)
    zip = fields.Char('Post code (zip)', required=True)
    building = fields.Char('Building number')
    latitude = fields.Char('Latitude', required=True)
    longitude = fields.Char('Longitude', required=True)
    sale_order_ids = fields.One2many(comodel_name='sale.order', inverse_name='parcel_machine_id', string='Orders for this Parcel Machine')
    count = fields.Integer(string="Order Count", compute='_compute_count', store=True)

    #=== COMPUTE METHODS ===#

    @api.depends('sale_order_ids')
    def _compute_count(self):
        for wizard in self:
            wizard.count = len(wizard.sale_order_ids)

    def _cron_update_from_csv(self, fname='parcel.machine.csv'):
        last_id = 0
        self._cr.execute('SELECT max(parcel_machine.id) FROM parcel_machine')
        res = self._cr.fetchone()
        if res:
            last_id = res[0]

        with open(fname) as f:
            line = f.readline()
            while line:
                line = f.readline()
                if not line:
                    break

                d = line.split(',')
                id = int(d[0])
                code = d[1]
                description = d[2]
                city = d[3]
                city_eng = d[4]
                street = d[5]
                area = d[6]
                zip = d[7]
                building = d[8]
                latitude = d[9]
                longitude = d[10]

                pm = self.env['parcel.machine'].search(domain=[('code', '=', code)], limit=1)
                if pm:
                    if (pm['description'] != description) or (pm['city'] != city) or (pm['city_eng'] != city_eng) or (pm['street'] != street) or (pm['area'] != area) or \
                        (pm['zip'] != zip) or (pm['building'] != building) or (pm['latitude'] != latitude) or (pm['longitude'] != longitude):
                        pm.write({
                            'description': description, 
                            'city': city, 
                            'city_eng': city_eng, 
                            'street': street, 
                            'area': area, 
                            'zip': zip, 
                            'building': building, 
                            'latitude': latitude, 
                            'longitude': longitude
                            })
                else:
                    if id > last_id:
                        last_id = id
                    else:
                        last_id += 1
                    self.env['parcel.machine'].create({
                        'id': last_id, 
                        'code': code, 
                        'description': description, 
                        'city': city, 
                        'city_eng': city_eng, 
                        'street': street, 
                        'area': area, 
                        'zip': zip, 
                        'building': building, 
                        'latitude': latitude, 
                        'longitude': longitude,
                        'count': 0
                        })
                    self.env['parcel.machine'].flush_model()
