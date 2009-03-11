#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard


class ProductCostHistory(ModelSQL, ModelView):
    'History of Product Cost'
    _name = 'product.product.cost_history'
    _description = __doc__

    template = fields.Many2One('product.template', 'Product')
    date = fields.DateTime('Date')
    cost_price = fields.Numeric('Cost Price')

    def __init__(self):
        super(ProductCostHistory, self).__init__()
        self._order.insert(0, ('date', 'DESC'))

    def table_query(self, context=None):
        property_obj = self.pool.get('ir.property')
        return ('SELECT ' \
                    '(EXTRACT(EPOCH FROM COALESCE(write_date, create_date)) ' \
                        '* (10 ^ (SELECT FLOOR(LOG(MAX(id))) + 1 ' \
                            'FROM "' + property_obj._table + '"))) ' \
                        '+ id AS id, ' \
                    'COALESCE(write_date, create_date) AS date, ' \
                    'TRIM(\',\' FROM SUBSTRING(res FROM \',.*\'))::INTEGER ' \
                        'AS template, ' \
                    'TRIM(\',\' FROM value)::NUMERIC AS cost_price ' \
                'FROM "' + property_obj._table + '__history" ' \
                'WHERE name = \'cost_price\' ' \
                    'AND res LIKE \'product.template,%%\' ' \
                'GROUP BY id, COALESCE(write_date, create_date), res, value',
                [])

ProductCostHistory()


class OpenProductCostHistory(Wizard):
    'Open Product Cost History'
    _name = 'product.product.cost_history.open'
    states = {
        'init': {
            'result': {
                'type': 'action',
                'action': '_open',
                'state': 'end',
            },
        },
    }

    def _open(self, cursor, user, data, context=None):
        model_data_obj = self.pool.get('ir.model.data')
        act_window_obj = self.pool.get('ir.action.act_window')
        product_obj = self.pool.get('product.product')

        model_data_ids = model_data_obj.search(cursor, user, [
            ('fs_id', '=', 'act_product_cost_history_form'),
            ('module', '=', 'product_cost_history'),
            ('inherit', '=', False),
            ], limit=1, context=context)
        model_data = model_data_obj.browse(cursor, user, model_data_ids[0],
                context=context)
        res = act_window_obj.read(cursor, user, model_data.db_id, context=context)

        product = product_obj.browse(cursor, user, data['id'], context=context)
        res['domain'] = str([('template', '=', product.template.id)])
        return res

OpenProductCostHistory()
