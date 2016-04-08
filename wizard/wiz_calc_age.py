# -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime as dtime


class wiz_calc_age(models.TransientModel):
    _name = 'wiz.calc.age'
    fname = fields.Char('Student Name')
    bdate = fields.Date("BirthDate")
    # by default compute fields are not created in database
    # store = True if you wish to create a field in database
    age = fields.Integer()
    country = fields.Many2one('res.country', 'Country')

    @api.multi
    def calc_age(self):
        # calculate the age of the students
        # search all the students
        # calculate age from dob
        # update the age of all the students
        stud_obj = self.env['school.admission']
        for res in self:
            sdata = stud_obj.search([('fname', 'ilike', res.fname)])
            print sdata
            for i in sdata:
                if i.bdate:
                    age = (dtime.now() - dtime.strptime(i.bdate, "%Y-%m-%d")).days/365
                    print i.bdate
                    i.age = age

    @api.multi
    def calc_country(self):
        stud = self.env['school.admission']
        for res in self:
            sdata = stud.search([('fname', 'ilike', res.fname)])
            print sdata
            for i in sdata:
                i.country = res.country.id
