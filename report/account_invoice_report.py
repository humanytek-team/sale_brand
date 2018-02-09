# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class AccountInvoiceReport(models.Model):
    _name = "account.invoice.report"
    _inherit = 'account.invoice.report'

    @api.one
    def _compute_brand(self):
        if self.account_id:
            AccountInvoice = self.env['account.invoice']
            invoices = AccountInvoice.search([
                                    ('account_id', '=', self.account_id),])
            if invoices:
                if invoices[0].invoice_line_ids:
                    if invoices[0].invoice_line_ids[0].product_id:

                        if invoices[0].invoice_line_ids[0].product_id.product_brand_id:
                            self.brand = invoices[0].invoice_line_ids[0].product_id.product_brand_id.name

    @api.multi
    def _search_brand(self, operator, value):
        AccountInvoiceReport = self.env['account.invoice.report']
        AccountInvoice = self.env['account.invoice']
        invoices_report = AccountInvoiceReport.search([])
        list_ids = []
        for invoice_report in invoices_report:
            invoices = AccountInvoice.search([
                ('account_id', '=', invoice_report.account_id.id)])
            if invoices:

                if invoices[0].invoice_line_ids:
                    if invoices[0].invoice_line_ids[0].product_id:
                        if invoices[0].invoice_line_ids[0].product_id.product_brand_id:
                            brand = invoices[0].invoice_line_ids[0].product_id.product_brand_id.name
                            if operator == '=':
                                if brand == value:
                                    list_ids.append(invoice_report.id)
                            elif operator == '!=':
                                if brand != value:
                                    list_ids.append(invoice_report.id)
        return [('id', 'in', list_ids)]

    brand = fields.Char(string="Brand", compute='_compute_brand',
                            search='_search_brand',
                            readonly=True,
                            #store=True
                            )
