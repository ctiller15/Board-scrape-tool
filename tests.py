import unittest
from scrape_helpers import generate_request_url
class TestUrlGeneration(unittest.TestCase):

    def test_url_generation(self):
       site = 'http://www.monster.com'
       query = 'mechanic'
       location = 'tampa'

       generated_url = generate_request_url(site, query, location)
       
       self.assertEqual(generated_url, 'https://www.monster.com/jobs/search/?q=mechanic&where=Tampa'.lower())

if __name__ == '__main__':
    unittest.main()
