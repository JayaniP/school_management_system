# -*- coding: utf-8 -*-
from openerp import api, fields, models
from openerp.report import report_sxw

class report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        print "#############################"
        super(report_parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'hello_world': self.hello_world
        })

    def hello_world(self):
        print "fghghjghj"
        return 'AAAAAAAAAAA'


class object_report(models.AbstractModel):
    _name = 'report.school_managemnet_system.report_template'
    _inherit = 'report.abstract_report'
    _template = 'school_managemnet_system.report_template'
    _wrapped_report_class = report_parser
