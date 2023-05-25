"""
Convert parcel machine list from json to csv file
----------------------------------------------------

MODE:
    INIT - initial portion of data
    CRON - updated portion of data

Fields and values in json-file:
    t - ? {1, 2}
    d - description
    m - maybe parent id
    q - ? {'', 33, 30}
    f - ? {'', '002', '008', '006', '003', '004', '005', '001', '007'}
    c - city
    g - city in english
    e - street
    r - area
    o - zip
    b - building number
    h - work time weekly
    i - work time by days
    p - ? {0, 1}
    s - ? {1}
    l.a - latitude
    l.o - longitude
"""

MODE = 'CRON'

import os, json

script_dir = os.path.dirname(os.path.realpath(__file__))
src_file = os.path.join(script_dir, 'parcel.machine.json')

if MODE == 'INIT':
    cities = ['wroclaw']
    module_dir = os.path.join(script_dir, '../addons/parcel_machine/data/')
    dst_file = os.path.join(module_dir, 'parcel.machine.csv')
else:
    cities = ['wroclaw', 'torun']
    dst_file = os.path.join(script_dir, 'parcel.machine.csv')

with open(src_file) as data_file:
    data = json.load(data_file)

with open(dst_file, 'w') as f:
    f.write('id,code,description,city,city_eng,street,area,zip,building,latitude,longitude,count')
    seq = 0
    for d in data['items']:
        if d['g'] not in cities:
            continue
        seq += 1
        id = seq
        code = d['n']
        description = d['d'].replace(',', '.')
        city = d['c'].replace(',', '.')
        city_eng = d['g'].replace(',', '.')
        street = d['e'].replace(',', '.')
        area = d['r'].replace(',', '.')
        zip = d['o']
        building = d['b'].replace(',', '.')
        latitude = d['l']['a']
        longitude = d['l']['o']
        f.write(f'\n{id},{code},{description},{city},{city_eng},{street},{area},{zip},{building},{latitude},{longitude},0')
