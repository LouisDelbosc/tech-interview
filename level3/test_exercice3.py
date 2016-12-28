import exercice as ex
import json
import unittest

class TestExercice3(unittest.TestCase):

    def setUp(self):
        self.articles = [
            { "id": 1, "name": "water", "price": 100 },
            { "id": 2, "name": "honey", "price": 200 },
            { "id": 3, "name": "mango", "price": 400 },
            { "id": 4, "name": "tea", "price": 1000 },
        ]

        self.carts = [
            {
                "id": 1,
                "items": [
                    { "article_id": 1, "quantity": 2 },
                    { "article_id": 2, "quantity": 2 },
                    { "article_id": 4, "quantity": 1 }
                ]
            },
            {
                "id": 2,
                "items": [
                    { "article_id": 2, "quantity": 1 },
                    { "article_id": 4, "quantity": 3 }
                ]
            },
        ]

        self.delivery_fees = [
            {
                "eligible_transaction_volume": {
                    "min_price": 0,
                    "max_price": 1000
                },
                "price": 800
            },
            {
                "eligible_transaction_volume": {
                    "min_price": 2000,
                    "max_price": None
                },
                "price": 100
            }
        ]

        self.discounts = [
            { "article_id": 2, "type": "amount", "value": 25 },
            { "article_id": 4, "type": "percentage", "value": 30 },
        ]

    def test_get_discount(self):
        article_1, article_2 = 1, 2
        self.assertIsNone(ex.get_discount(self.discounts, article_1))
        self.assertEqual(ex.get_discount(self.discounts, article_2), self.discounts[0])


    def test_get_article_price(self):
        article_1, article_2, article_4 = 1, 2, 4
        price_1 = ex.get_article_price(self.articles, self.discounts, article_1)
        price_2 = ex.get_article_price(self.articles, self.discounts, article_2)
        price_4 = ex.get_article_price(self.articles, self.discounts, article_4)
        self.assertEqual(price_1, 100)
        self.assertEqual(price_2, 175)
        self.assertEqual(price_4, 700)


    def test_is_in_price_range(self):
        price_1, price_2, price_3 = 500, 1500, 2500

        self.assertTrue(ex.is_in_price_range(self.delivery_fees[0], price_1))
        self.assertFalse(ex.is_in_price_range(self.delivery_fees[0], price_2))
        self.assertFalse(ex.is_in_price_range(self.delivery_fees[0], price_3))

        self.assertFalse(ex.is_in_price_range(self.delivery_fees[1], price_1))
        self.assertFalse(ex.is_in_price_range(self.delivery_fees[1], price_2))
        self.assertTrue(ex.is_in_price_range(self.delivery_fees[1], price_3))


    def test_compute_fees(self):
        price_1, price_2, price_3 = 500, 1500, 2500
        self.assertEqual(ex.compute_fees(self.delivery_fees, price_1), 800)
        self.assertEqual(ex.compute_fees(self.delivery_fees, price_2), 0)
        self.assertEqual(ex.compute_fees(self.delivery_fees, price_3), 100)


    def test_cart_price(self):
        cart_1 = ex.cart_price(self.articles, [], [], self.carts[0])

        cart_2 = ex.cart_price(self.articles, self.delivery_fees,
                               [], self.carts[0])

        cart_3 = ex.cart_price(self.articles, self.delivery_fees,
                               [], self.carts[1])

        cart_4 = ex.cart_price(self.articles, self.delivery_fees,
                               self.discounts, self.carts[1])

        self.assertEqual(cart_1['total'], 1600)
        self.assertEqual(cart_2['total'], 1600)
        self.assertEqual(cart_3['total'], 3300)
        self.assertEqual(cart_4['total'], 2375)


    def test_compute_output(self):
        data = ex.load_data('data.json')
        articles, carts = data['articles'], data['carts']
        fees, discounts = data['delivery_fees'], data['discounts']
        test_output = ex.compute_output(articles, fees, discounts, carts)
        with open('output.json') as data_file:
            expected_output = json.load(data_file)
            self.assertEqual(expected_output, test_output)
