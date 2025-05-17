import io
import unittest
from unittest import mock

try:
    from webapp.app import app
    flask_available = True
except ModuleNotFoundError:
    # Flask is not installed; skip tests
    app = None
    flask_available = False

@unittest.skipUnless(flask_available, "Flask not installed")
class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'BayesPy Data Explorer', resp.data)

    @mock.patch('webapp.app.compute_priors', return_value=[0.5, 0.5])
    def test_dirichlet_api(self, mock_compute):
        data = '1,2\n3,4\n'
        resp = self.client.post('/api/dirichlet',
                                data={'file': (io.BytesIO(data.encode('utf-8')), 'test.csv')},
                                content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {'priors': [0.5, 0.5]})
        mock_compute.assert_called()

    def test_sample_served(self):
        resp = self.client.get('/static/samples/sample1.csv')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.data), 0)

if __name__ == '__main__':
    unittest.main()
