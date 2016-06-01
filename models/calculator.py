# -*- coding: utf-8 -*-
from openerp import api, fields, models


class cal(models.Model):
    _name = "calculator.cal"
    res = fields.Integer("Result")

#    one=fields.Integer("o",default="1")
#    two=fields.Integer("t",default="2")
#    three=fields.Integer("th",default="3")
#    four=fields.Integer("fo",default="4")
#    five=fields.Integer("fi",default="5")
#    six=fields.Integer("s",default="6")
#    sevon=fields.Integer("se",default="7")
#    eight=fields.Integer("ei",default="8")
#    nine=fields.Integer("ni",default="9")
#    zero=fields.Integer("z",default="0")

    @api.multi
    def calc_res(self):
        self._context.get('value')
