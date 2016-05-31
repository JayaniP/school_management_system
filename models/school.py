# -*- coding: utf-8 -*-
from openerp import api , fields, models
from openerp.exceptions import except_orm, ValidationError
from datetime import datetime as dtime
from openerp import tools
from openerp.tools.translate import _
from openerp.osv import osv
import re
import time


class admission(models.Model):
    _name = "school.admission"
    _rec_name = 'fname'
    _order = 'fname'

    @api.depends('bdate')
    def calc_age(self):
        if self.bdate:
            age = (dtime.now()- dtime.strptime 
                  (self.bdate, "%Y-%m-%d")).days/365
            self.age = age

    name = fields.Char('Student Reference', required=False, copy=False,
                       readonly=True)
    image = fields.Binary('Image')
    fname = fields.Char('First Name')
    mname = fields.Char('Middle Name')
    lname = fields.Char('Last Name')
    student_ids = fields.Many2one('school.attedence', 'Students')
    contact = fields.Char("Contact No")
    email = fields.Char("EmailID")
    batch = fields.Selection([('fb', '2016'), ('sb', '2017'), ('tb', '2018'),
                              ('fb', '2019'), ('fib', '2020')], 'Batch')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], 'Gender')
    bdate = fields.Date("BirthDate")
    # by default compute fields are not created in database
    # store = True if you wish to create a field in database
    age = fields.Integer(compute='calc_age', string='Age', store=True)
    appno = fields.Integer('Application No')
    appdate = fields.Date('Application Date',
                          default=time.strftime("%Y-%m-%d"))
    admissiondate = fields.Date('Admission Date')
    std = fields.Selection([('f', '1st Std'), ('s', '2th Std'),
            ('t', '3th Std'), ('fo', '4th Std'), ('fi', '5th Std'),
            ('six', '6th Std'), ('se', '7th Std'), ('e', '8th Std'),
            ('n', '9th Std'), ('ten', '10th Std'), ('ele', '11th Std'),
            ('twe', '12th Std')], 'Standard')
    street = fields.Text("Address")
    city = fields.Selection([('p', 'Patan'), ('a', 'Ahmedabad'),
            ('b', 'Baroda'), ('s', 'Surat'), ('r', 'Rajkot'),
            ('m', 'Mahesana'), ('g', 'Gandhinagar'), ('mb', 'Mumbai'),
            ('bn', 'Banglore'), ('pu', 'Pune'), ('d', 'Delhi'),
            ('my', 'Mysoor')], 'City')
    country = fields.Many2one('res.country', 'Country')
    country_code = fields.Char('Country Code', related='country.code')
    # Related fields are not created in database same as compute / function
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  related='country.currency_id')
    state = fields.Many2one('res.country.state', 'State')
    zip = fields.Char("Zip")
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence')
    year = fields.Selection([('fb', '2016'), ('sb', '2017'), ('tb', '2018'),
                             ('fb', '2019'), ('fib', '2020')], 'Year')
    status = fields.Selection([('details', 'Details'), ('started', 'Started'),
         ('progress', 'In progress'), ('finished', 'Done')], default='details')

    sql_constraints = [('number_uniq', 'unique(contact)',
            'Contact number must be unique per Student!'),
            ('email_uniq', 'unique(email)',
             'Email must be unique per Student!')]

    @api.constrains('email', 'age', 'contact', 'bdate')
    def check_data(self):
        for res in self:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                     res.email) == None:
                raise ValidationError(_('Enter valid email'))
            if len(str(res.contact)) < 10:
                raise ValidationError(_('Enter valid contact'))
            if res.age >= 20:
                raise ValidationError(_('Age must be less than 20'))
            if (time.strftime("%Y-%m-%d") < res.bdate):
                raise ValidationError(_('Birthdate will not be in future.'))

    @api.one
    def details_progressbar(self):
        self.write({
            'status': 'details',
          })

    @api.one
    def started_progressbar(self):
        self.write({
           'status': 'started'
         })

    @api.one
    def progress_progressbar(self):
        self.write({
          'status': 'progress'
        })

    @api.one
    def done_progressbar(self):
        self.write({
           'status': 'finished',
        })

    @api.multi
    #def name_get(self, cr, uid, ids, context=None)
    def name_get(self):
        lst = []
        for student in self:
            fname = student.fname
            lname = student.lname
            name = fname + ' [' + (lname and lname or '/') + ']'
            lst.append((student.id, name))
        return lst

    @api.model
    #def name_search(self, cr, uid, name, args=None, operator='ilike',
#                   context=None, limit=100):
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            students = self.search(args + [('lname', '=', name)])
            if not students:
                students = self.search(args + [('lname', 'ilike', name)])
            return students.name_get()
        return super(admission, self).name_search(name, args=args,
                                operator=operator, limit=limit)

    @api.onchange('state')
    def change_state(self):
        """
        This will fill the country from selected state.
        """
        state = self.state
        self.country = state and state.country_id and state.country_id.id or False
#        if state and state.country_id:
#            # Fill country from selected state
#            self.country = state.country_id.id
#        else:
#            self.country = False

#    def create(self, cr, uid, vals, context=None):
#        return super(admission, self).create(cr, uid, vals)
#v8
    @api.multi
    def create_data(self, vals):
        for res in self:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].get('school.admission')

    @api.multi
    def write_data(self, vals):
        for res in self:
            res.write(vals)

    @api.multi
    def calc_del(self):
        for res in self:
            res.unlink()

    @api.multi
    def search_data(self):
        for res in self:
            sdata = res.search([('lname', 'ilike', 'patel')])

    @api.multi
    def read_data(self):
        for res in self:
            rdata = res.read(['fname', 'lname', 'mname', 'contact', 'email'])

#v7
#    @api.v7
#    def write(self, cr, uid, ids, vals, context=None):
#       searchid = self.search(cr, uid, [('fname','ilike','jayani')],
#                        context=context)
#       br=self.browse(cr, uid, searchid, context = context)
#       students = self.read(cr, uid,searchid, context = context)
#       self.recorddel(cr, uid)
#       return super(admission, self).write(cr, uid, ids, vals)

#    def recorddel(self,cr, uid):
#        self.pool['school.faculty'].unlink(cr,uid,[2])

#    @api.v7
#    def browse(self, cr, uid, ids,context=None):
#       students = self.browse(cr, uid, lname, context = context)
#       return super(admission,self)

#    @api.v7
#    def search(self, cr, uid, args, offset=0, limit=None, order=None,
#                  context=None, count=False):
#       #res = super(admission, self).search(cr, uid, args, offset=offset,
#                  limit=limit, order=order, context=context, count=count)
#       ids=self.search(cr, uid, [('fname','=','jayani')],context=context)

#    @api.v7
#    def read(self, cr, user, ids, fields=None, context=None,
#                 load='_classic_read'):
#        ids = obj.search(cr, uid, [('fname','=','jayani')], context=context)
#        res = super(admission, self).read(cr, user,ids,fields=fields,
#               context=context,load=load)
#        return res

#    @api.v7
#    def unlink(self, cr, uid, ids, context=None):
#        res = super(admission, self).unlink(self, cr, uid, context=context)
#        return re

#    @api.model
#    def search(self, args, offset=0, limit=None, order=None, count=False):
#        res = super(admission, self).search(args, offset=offset, limit=limit,
#             order=order, count=count)
#        return res

#    @api.multi
#    def write(self, vals):
#        return super(admission, self).write(vals)


class school_event(models.Model):
    _name = "school.event"

    evname = fields.Selection([('p', 'Painintg'), ('d', 'Drama'),
                ('s', 'Singing'), ('da', 'Dancing'), ('q', 'Quiz'),
                ('so', 'Solo')], 'Event Name')
    org = fields.Many2many('school.admission', 'student_event_rel', 'event_id',
                    'student_id', 'Students')

    @api.multi
    def write(self, vals):
        for org in self.org:
            return super(school_event, self).write(vals)


class faculty(models.Model):
    _name = "school.faculty"
    _rec_name = 'fname'

    image = fields.Binary('Image')
    fname = fields.Char('First Name')
    mname = fields.Char('Middle Name')
    lname = fields.Char('Last Name')
    contact = fields.Integer("Contact No")
    email = fields.Char("EmailID")
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], 'Gender')
    bdate = fields.Date("BirthDate")
    street = fields.Text("Address")
    city = fields.Selection([('p', 'Patan'), ('a', 'Ahmedabad'),
            ('b', 'Baroda'), ('s', 'Surat'), ('r', 'Rajkot'),
            ('m', 'Mahesana'), ('g', 'Gandhinagar'), ('mb', 'Mumbai'),
        ('bn', 'Banglore'), ('pu', 'Pune'), ('d', 'Delhi'), ('my', 'Mysoor')])
    country = fields.Many2one('res.country', 'Country')
    country_code = fields.Char('Country Code', related='country.code')
    state = fields.Many2one('res.country.state', 'State')
    zip = fields.Char("Zip")

    @api.multi
    def name_get(self):
        lst = []
        for faculty in self:
            fname = faculty.fname
            lname = faculty.lname
            name = fname + ' ' + (lname and lname or 'None')
            lst.append((faculty.id, name))
        return lst

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            f = self.search(args + [('lname', '=', name)])
            if not f:
                f = self.search(args + [('lname', 'ilike', name)])
            return f.name_get()
        return super(faculty, self).name_search(name, args=args,
                        operator=operator, limit=limit)

    @api.model
    def create(self, vals):
        vals.update({'mname': vals.get('mname', '') + ' - SCS'})
        return super(faculty, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(faculty, self).write(vals)


class attendence(models.Model):
    _name = "school.attedence"

    date = fields.Date('Date')
    s = fields.One2many('school.admission', 'student_ids', 'Stud')

    @api.multi
    def write(self, vals):
        s = vals.get('s')
        if not s:
            s = []
        s.append([0, 0, {'fname': '11', 'lname': '22', 'mname': '333'}])
        vals.update({'s': s})
        res = super(attendence, self).write(vals)
        return res


class library(models.Model):
    _name = "school.library"

    bname = fields.Selection([('a', 'MathsPuzzles'), ('d', 'EnglishGrammer'),
     ('e', 'EnglishVocabulary'), ('g', 'GeneralKnowledge'), ('m', 'Magazine'),
        ('sc', 'Science')], 'Book Name')
    bauthor = fields.Selection([('a', 'AshokPatel'), ('sc', 'ShaileshGajjar'),
        ('e', 'ChimnalalMunshi'), ('d', 'Dr.Chatrvedi'), ('m', 'Manan Vyas'),
        ('g', 'Praafful Vyas')], 'Book Auther')
    idate = fields.Date('Issue Date')
    rdate = fields.Date('Return Date')
    des = fields.Text('Book Description')

    @api.onchange('bname')
    def change_book(self):
        bname = self.bname
        self.bauthor = bname


class exam(models.Model):
    _name = "school.exam"

    ename = fields.Selection([('i', 'Internal'), ('e', 'External')])
    subject = fields.Selection([('m', 'Maths'), ('e', 'English'),
                                ('s', 'Science'), ('p', 'Physics'),
                                ('c', 'Chemistry'), ('b', 'Biology'),
                                ('sc', 'SocialScience')], 'Subject')
    stime = fields.Datetime('Exam Start Time')
    endtime = fields.Datetime("Exam End Time")
    student_id = fields.Many2one('school.admission', 'Student')

    @api.multi
    def calc_result(self):
        stud_obj = self.env['school.result']
        for res in self:
            students = stud_obj.search([('result_id', '=', res.student_id.id)])
            if students:
                return {
                   'name': _("Result"),
                   'view_mode': 'form',
                   'res_id': students.id,
                   'view_type': 'form',
                   'res_model': 'school.result',
                   'type': 'ir.actions.act_window',
                   'nodestroy': True,
                   'target': 'current',
                    }
            else:
                raise ValidationError(_('This student have no result record'))

    @api.constrains('stime', 'endtime')
    def check_dates(self):
        if self.stime >= self.endtime:
            raise ValidationError(_('Exam Start Date Should be less'
                                  'than the Exam End Date!'))


class assignment(models.Model):
    _name = "school.assignment"
    _description = 'School Assignment'
    # to show the records order by
    _order = 'subject desc'

    subject = fields.Selection([('m', 'Maths'), ('e', 'English'),
         ('s', 'Science'), ('p', 'Physics'), ('c', 'Chemistry'),
         ('b', 'Biology'), ('sc', 'SocialScience')])
    std = fields.Selection([('f', '1st Std'), ('s', '2th Std'),
        ('t', '3th Std'), ('fo', '4th Std'), ('fi', '5th Std'),
        ('six', '6th Std'), ('se', '7th Std'), ('e', '8th Std'),
        ('n', '9th Std'), ('ten', '10th Std'), ('ele', '11th Std'),
        ('twe', '12th Std')])
    div = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'),
                             ('e', 'E')])
    assign = fields.Many2many('school.admission', 'assignment_student_rel',
                              'assignment_id', 'student_id', 'Assignment')
    idate = fields.Date("Issue Date",)
    rdate = fields.Date("Return Date")
    faculty_id = fields.Many2one('school.faculty', 'Faculty Name')
#    country = fields.Many2one('res.country', 'Country')
#    country_code = fields.Char('Country Code', related='country.code')
#    # Related fields are not created in database same as compute / function
#    currency_id = fields.Many2one('res.currency', 'Currency',
#                    related='country.currency_id')

    @api.constrains('idate', 'rdate')
    def check_dates(self):
        if self.idate >= self.rdate:
            raise ValidationError(_('Issue Date Should be less than'
                        'the Return Date!'))


class result(models.Model):
    _name = "school.result"

    result_id = fields.Many2one('school.admission', 'Student')
    div = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'),
                            ('e', 'E')])
    ename = fields.Selection([('i', 'Internal'), ('e', 'External')])
    std = fields.Selection([('f', '1st Std'), ('s', '2th Std'),
        ('t', '3th Std'), ('fo', '4th Std'), ('fi', '5th Std'),
        ('six', '6th Std'), ('se', '7th Std'), ('e', '8th Std'),
        ('n', '9th Std'), ('ten', '10th Std'), ('ele', '11th Std'),
        ('twe', '12th Std')])
    year = fields.Selection([('fb', '2016'), ('sb', '2017'), ('tb', '2018'),
        ('fb', '2019'), ('fib', '2020')])
    totalmarks = fields.Integer('Total Marks')
    obtainmarks = fields.Integer('obtain Marks')
    percentage = fields.Integer('Percentage')
    res = fields.Char('Result')

    _sql_constraints = [('c_obtainmarks', 'CHECK (obtainmarks<totalmarks)',
                         'Obtain marks is not more than Total marks')]

    #v7
#    def calc_res(self, cr, uid, ids, context=None):
#        for res in self.browse(cr, uid, ids, context=context):
#            per = res.obtainmarks * 100 / res.totalmarks
#            result =''
#            if per >= 35:
#               result = 'Pass'
#            else:
#               result = 'Fail'
#            self.write(cr,uid,[res.id],{'percentage': per, 'res': result},
#                                   context=context)
    #v8
    @api.multi
    def calc_res(self):
        for res in self:
            per = res.obtainmarks * 100 / res.totalmarks
            if per >= 35:
                result = 'Pass'
            else:
                result = 'Fail'
            res.write({'percentage': per, 'res': result})
        return True

    @api.multi
    def calc_del(self):
        for res in self:
            res.unlink()
        return True
#class school_school(models.Model):
#    _name="school.school"
#    _table="school"


class school_result(models.Model):
    _inherit = "school.result"
    grade = fields.Char("Grade")


class project(models.Model):
    _name = "school.project"

#    _inherits = {
#                 'school.assignment':"faculty_id"
#                 'account.analytic.account': "analytic_account_id",
#                }

    faculty_id = fields.Many2one('school.faculty', 'Faculty Name',
                    required=True, delegate=True)
    id = fields.Integer("EnterID")
    analytic_account_id = fields.Many2one('project.project',
            'Contract/Analytic', help="Link this project to an analytic account if you need financial management on projects."
                 "It enables you to connect projects with budgets, planning, cost and revenue analysis, timesheets on projects, etc.",
            ondelete="cascade", auto_join=True, delegate=True)

#    def schedule_tasks(self, cr, uid, ids, context=None):
#        task= super(project,self).schedule_tasks(self, cr, uid, ids,
#               context=None)
#        return task

#    def copy_quotation(self, cr, uid, ids, context=None):
#        amount_val= super(project,self).copy_quotation(self, cr, uid, ids,
#                 context=None)
#        return amount_val


class calender_view(models.Model):
    _name = 'calender.view'

    name = fields.Char('Name')
    user_id = fields.Many2one('res.users', 'Users')
    from_datetime = fields.Datetime('From Datetime')
    to_datetime = fields.Datetime('To Datetime')
