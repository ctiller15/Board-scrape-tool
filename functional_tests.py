import unittest
from get_html_script import scrape_site
from bs4 import BeautifulSoup

class TestScrapeMethods(unittest.TestCase):

    def test_successfully_scrapes_site(self):
        # Phil comes by, he wants to use this web scraper tool.
        # He plans to see if it can find data on mechanics jobs, and he wants to move to tampa, so he checks monster.
        query = 'mechanic'
        location = 'Tampa'
        site = 'https://www.monster.com'
        #url = 'https://www.monster.com/jobs/search/?q=mechanic&where=Tampa'
        results = scrape_site(site, query, location)

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
        site = 'https://www.monster.com'

        # Mary tries to verify some of the same stuff.
        results = scrape_site(site, query, location)

        # Mary sees that it did in fact search the site she wanted.
        self.assertTrue(site in results.url)

        # Mary sees that it definitely searched for the type of job she wanted.
        self.assertTrue(query in results.url)

        # She also sees that it certainly searched the location he wanted.
        self.assertTrue(location in results.url)

        # Mary sees that the site did, in fact, get data from the monster job site.
        self.assertTrue(results.url.contains(site))
        # Mary, not being one of those computer-y types, is glad that his result does not contain any html inside of it.

        self.assertFalse(bool(BeautifulSoup(results.content, "html.parser").find()))

        # Mary sees that she did get mechanic jobs in her results.
        self.assertTrue(results.listItems.names.contains(query))

        # Mary also sees that she got results in New York.
        self.assertTrue(results.listItems.locations.any.contains(location))

        # Mary sees that the scraper can actually grab data from a site!
        self.assertNotEmpty(results.response)

        # Amazed at how far technology has come, a satisfied Mary goes to bed.


if __name__ == '__main__':
    unittest.main()

