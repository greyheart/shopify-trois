from ... import ShopifyTroisTestCase

from shopify_trois import Shop, Credentials, ShopifyException
from shopify_trois.engines.http.json import Json as Shopify
from shopify_trois.engines.http.request import Request

class JsonEngineTestCase(ShopifyTroisTestCase):

    def test_class(self):
        expected = "json"
        self.assertEqual(Shopify.extension, expected)

        expected = "application/json; charset=utf-8"
        self.assertEqual(Shopify.mime, expected)

    def test_prepare_request(self):
        shop = Shop(name = 'test')
        credentials = Credentials()
        shopify = Shopify(shop = shop, credentials = credentials)

        request = Request()
        shopify._prepare_request(request)
        expected = {
            "X-Shopify-Access-Token": None,
            "Content-Type": "application/json; charset=utf-8"
        }
        self.assertEquals(request.headers(), expected)

        request = Request()
        shopify._prepare_request(request, use_access_token = False)
        expected = {
            "Content-Type": "application/json; charset=utf-8"
        }
        self.assertEquals(request.headers(), expected)

    def test_url_for_request(self):
        shop = Shop(name = 'test')
        credentials = Credentials()
        shopify = Shopify(shop = shop, credentials = credentials)

        request = Request()
        request.resource = "test"
        url = shopify.url_for_request(request)
        # Note: the base request class does not have an extension.
        expected = "https://test.myshopify.com/admin/test.json"
        self.assertEquals(url, expected)

        request.resource = "test/mmmm food"
        url = shopify.url_for_request(request)
        # Note: The url generated by url_for_request are not escaped. The
        # actual request.{method} will escape the url for us.
        expected = "https://test.myshopify.com/admin/test/mmmm food.json"
        self.assertEquals(url, expected)
