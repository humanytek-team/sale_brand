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


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = 'sale.order'

    brand = fields.Char('Brand',
                            compute='_compute_brand_id',
                            search='_search_brand',
                            readonly=True)

    @api.one
    def _compute_brand_id(self):
        if self.order_line:
            if self.order_line[0].product_id.product_brand_id:
                self.brand = self.order_line[0].product_id.product_brand_id.name

    @api.multi
    def _search_brand(self, operator, value):
        SaleOrder = self.env['sale.order']
        orders = SaleOrder.search([])
        list_ids = []
        for order in orders:
            if order.order_line:
                if order.order_line[0].product_id.product_brand_id:
                    brand = order.order_line[0].product_id.product_brand_id.name
                    if operator == '=':
                        if brand == value:
                            list_ids.append(order.id)
                    elif operator == '!=':
                        if brand != value:
                            list_ids.append(order.id)
        return [('id', 'in', list_ids)]