import ujson
import finder
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        finder.app.config['TESTING'] = True
        self.app = finder.app.test_client()

    def echo(self, data):
        response = self.app.post('/echo', data=ujson.dumps(data),
                                 content_type='application/json')
        return ujson.loads(response.data)

    def test_echo(self):
        data = {"hello": "world"}
        assert data == self.echo(data)
