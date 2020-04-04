import unittest
from bs4 import BeautifulSoup
from src import get_html_script as ghs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import domain_db_mappings as dbm
from models.database_models import JobDataDbModel
import models.database_methods as db_ops
from src.email_generator import TextEmailContent, HtmlEmailContent, generate_full_email_content
from src.email_sender import send_email_to_user
from datetime import date

Base = declarative_base()

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

        query = 'developer'
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

class EndToEndHtmlScrapeSaveToDbTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, tables=[JobDataDbModel.__table__])

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_scrapes_and_saves_job_data(self):
        job_sites = ['monster.com']
        location = 'utah'
        query = 'hairdresser'

        before_data = self.session.query(JobDataDbModel).all()

        self.assertFalse(before_data)

        ghs.scrape_sites_and_save_jobs(job_sites, query, location, self.session)

        after_data = self.session.query(JobDataDbModel).all()

        self.assertTrue(after_data)

class StoresDataAndSendsEmailTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, tables=[JobDataDbModel.__table__])

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_emails_saved_job_data(self):
        # Larry is lazy. He doesn't want to have to keep checking everything himself, so
        # He wants the app to email him only results that haven't already been emailed to him yet.

        query = 'hairdresser'
        location = 'utah'
        site = 'monster.com'

        class_data = ghs.scrape_full_page(site, query, location)

        # His data is saved to the database. It is the exact same data that he had before.
        mapped_data = dbm.map_job_data_models_to_db_models(class_data)

        for data_point in mapped_data:
            self.session.add(data_point)

        self.session.commit()

        saved_data = self.session.query(JobDataDbModel).all()

        self.assertEqual(len(class_data), len(saved_data))

        # His data is safely persisted in a database. Now he expects it to email itself to him.

        relevant_job_data = generate_full_email_content(saved_data)

        # The email has all of the expected data. It gets emailed to him.
        response = send_email_to_user(relevant_job_data)

        # Larry has received the email after a short amount of time has passed.
        self.assertDictEqual(response, {})

        db_ops.mark_job_data_as_sent(self.session, saved_data)
        # All of the items that were sent are now marked as having been sent.
        # Because of this, none of them should show if we filter out sent items in the DB.
        updated_data = self.session.query(JobDataDbModel).filter(JobDataDbModel.has_been_emailed == False).all()
        self.assertTrue(len(updated_data) == 0)

        # Satisfied that it works as expected, Larry goes to bed.


if __name__ == '__main__':
    unittest.main()

