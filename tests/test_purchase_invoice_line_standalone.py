# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends, test_menu_action
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class PurchaseInvoiceLineStandaloneTestCase(unittest.TestCase):
    'Test PurchaseInvoiceLineStandalone module'

    def setUp(self):
        trytond.tests.test_tryton.install_module(
                'purchase_invoice_line_standalone')

    def test0005views(self):
        'Test views'
        test_view('purchase_invoice_line_standalone')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0007menu_actions(self):
        'Test menu actions'
        test_menu_action('purchase_invoice_line_standalone')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseInvoiceLineStandaloneTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_purchase_invoice_line_standalone.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='UTF-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
