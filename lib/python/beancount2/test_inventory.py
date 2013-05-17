"""
Unit tests for the inventory class.
"""
import unittest

from beancount2.data import Amount, AmountS, Lot
from beancount2.inventory import Inventory


class TestInventory(unittest.TestCase):

    def test_add(self):
        inv = Inventory()
        inv.add(AmountS('100.00', 'USD'))
        print(inv)

        inv.add(AmountS('25.01', 'USD'))
        print(inv)

        inv.add(AmountS('12.73', 'CAD'))
        print(inv)

        inv.add(AmountS('-84.03', 'USD'))
        print(inv)

        self.assertRaises(ValueError, inv.add, AmountS('-40.99', 'USD'))


    def test_add_withcost(self):
        inv = Inventory()
        inv.add(AmountS('100.00', 'USD'), AmountS('100', 'USD'))
        print(inv)

        invcopy = inv.copy()
        self.assertRaises(ValueError, invcopy.add, AmountS('-100.00', 'USD'), AmountS('100.01', 'USD'))
        print(inv)

        invcopy = inv.copy()
        self.assertRaises(ValueError, invcopy.add, AmountS('-100.01', 'USD'), AmountS('100.00', 'USD'))
        print(inv)

    def test_get_costs(self):
        inv = Inventory()
        inv.add(AmountS('10.00', 'USD'), AmountS('1.05', 'CAD'))
        print(inv.get_amounts())
        print(inv.get_costs())

        inv = Inventory()
        inv.add(AmountS('100', 'AAPL'), AmountS('404.00', 'USD'))
        print(inv.get_amounts())
        print(inv.get_costs())
