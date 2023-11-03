# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class Publisher(models.Model):
    _name = 'book.publisher'
    _inherit = 'mail.thread'

    _description = 'books.publisher'

    name = fields.Char(string="Name Book", tracking=True)
    id = fields.Integer(string="Id")
    email = fields.Char(string='Email', size=256, tracking=True)
    phone_number = fields.Char(string='Phone Number', size=20, tracking=True)
    date_publisher = fields.Date(string="Date Of Publisher", tracking=True)
    count_books = fields.Integer(string="Count Of Books", tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consulation', 'In Consulation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default="draft", string='state', required=True)



    def action_in_consultation(self):

        for rec in self:
            rec.state = 'done'

    def action_done(self):

        for rec in self:
            rec.state = 'in_consulation'

    def action_cancel(self):

        for rec in self:
            rec.state = 'done'

    def action_draft(self):

        for rec in self:
            rec.state = 'cancel'


