import unittest
from bs4 import BeautifulSoup
import get_html_script as ghs

class TestScrapeMethods(unittest.TestCase):

    def test_successfully_scrapes_site(self):
        # Phil comes by, he wants to use this web scraper tool.
        # He plans to see if it can find data on mechanics jobs,
        # and he wants to move to tampa, so he checks monster.
        query = 'mechanic'
        location = 'Tampa'
        site = 'https://www.monster.com'
        #url = 'https://www.monster.com/jobs/search/?q=mechanic&where=Tampa'
        results = ghs.scrape_site(site, query, location)

        # Phil sees that he was able to get a successful response
        self.assertEqual(results.status_code, 200)

        # Phil sees that it did in fact search the site he wanted.
        self.assertTrue(site in results.url)

        # Phil sees that it definitely searched for the type of job he wanted.results
        self.assertTrue(query in results.url)

        # He also sees that it certainly searched the location he wanted.
        self.assertTrue(location in results.url)

    def test_successfully_parses_data(self):
        # Mary is a bit more discerning than Phil.
        # She wants to make sure her data makes sense.

        query = 'radiologist'
        location = 'New York'
        site = 'monster.com'
        location_names = ['New York', 'NY']

        results = ghs.scrape_full_page(site, query, location)

        # Results are not empty. Mary managed to scrape data from a site!
        self.assertTrue(results)

        # Mary does not see any html.
        results_names = [result.title for result in results]
        results_locations = [result.location for result in results]
        results_sites = [result.link for result in results]

        self.assertFalse(any(
            [
                bool(BeautifulSoup(results_name, "html.parser").find())
                for results_name in results_names
            ]
        ))

        self.assertFalse(any(
            bool(BeautifulSoup(results_location, "html.parser").find())
            for results_location in results_locations
        ))

        # Mary sees that she did get radiologist jobs in her results.
        self.assertTrue(any([(query in results_name) for results_name in results_names]))

        # Mary also sees that she got results in New York.
        self.assertTrue(any(
            [
                [loc in results_location for loc in location_names]
                for results_location in results_locations
            ]
        ))

        # Mary lastly sees that all of the job links are, in fact from monster.
        self.assertTrue(all([site in result_site for result_site in results_sites]))

        # Amazed at how far technology has come, a satisfied Mary goes to bed.


if __name__ == '__main__':
    unittest.main()

