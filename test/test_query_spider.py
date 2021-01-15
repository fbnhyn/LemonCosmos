import unittest

import scrapy
import scrapy.http
from lmpd.lemon.lemon.models import Query


class TestQuerySpider(unittest.TestCase):
    
    def test_add_price_range_to_url(self):
        response = scrapy.http.Response(url="/maker/model?cy=D")
        query = Query(response, 400)
        refined_url = query.refine_query()
        self.assertTrue("priceto" in refined_url)
        self.assertTrue("pricefrom" in refined_url)

    def test_refine_lower_query(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&pricefrom=200&priceto=1000")
        query = Query(response, 400)
        refined_url = query.refine_query()
        self.assertTrue("priceto=600" in refined_url)
        self.assertTrue("?cy=D" in refined_url)

    def test_has_offer_param(self):
        response = scrapy.http.Response(url="/maker/model?offer=u&cy=D&pricefrom=200&priceto=1000")
        query = Query(response, 150)
        refined_url = query.refine_query()
        self.assertTrue("offer" in refined_url)

    def test_refine_upper_query(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&pricefrom=200&priceto=1000")
        query = Query(response, 100)
        refined_url = query.refine_query()
        self.assertTrue("priceto=999999999" in refined_url)
        self.assertTrue(f"pricefrom={query.price_to + 1}" in refined_url)

    def test_refine_upper_query_false_all_in_one_query(self):
        response = scrapy.http.Response(url="/maker/model?cy=D")
        query = Query(response, 100)
        self.assertFalse(query.has_upper_query)

    def test_init_price_to_has_value(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&priceto=500")
        query = Query(response, 200)
        self.assertEqual(query.price_to, 500)

    def test_init_price_to_is_none(self):
        response = scrapy.http.Response(url="/maker/model?cy=D")
        query = Query(response, 200)
        self.assertEqual(query.price_to, None)

    def test_init_price_from_has_value(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&pricefrom=1000")
        query = Query(response, 200)
        self.assertEqual(query.price_from, 1000)

    def test_has_upper_query_true(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&pricefrom=1000&priceto=5000")
        query = Query(response, 100)
        self.assertTrue(query.has_upper_query)

    def test_has_upper_query_false(self):
        response = scrapy.http.Response(url="/maker/model?cy=D&pricefrom=1000&priceto=999999999")
        query = Query(response, 100)
        self.assertFalse(query.has_upper_query)

if __name__ == '__main__':
    unittest.main()
