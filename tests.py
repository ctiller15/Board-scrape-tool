import unittest
import scrape_helpers as sh
from bs4 import BeautifulSoup
from models import models
from models.database_models import JobDataDbModel
from models import domain_db_mappings as dbm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import html_generator as html_gen

Base = declarative_base()

dummy_html = """<section class="card-content" data-jobid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail"></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="419414642" data-m_impr_j_jobid="194890933" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.75" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9967" data-m_impr_j_occid="11870" data-m_impr_j_p="1" data-m_impr_j_postingid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" data-m_impr_j_pvc="pandologicpx" data-m_impr_s_t="t" data-m_impr_uuid="66592e1d-3b1b-448a-9646-b9149c2cfd42" href="https://job-openings.monster.com/neurointerventional-radiologist-new-york-ny-us-confidential/bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Neurointerventional Radiologist&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_Confidential&quot;,&quot;eVar31&quot;:&quot;New York_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-13T12:00&quot;,&quot;eVar53&quot;:&quot;2900480001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;regular&quot;}')">Neurointerventional Radiologist</a></h2></header><div class="company"><span class="name">Confidential</span><ul class="list-inline"></ul></div><div class="location"><span class="name">New York, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">3 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>
"""

dummy_html_list = ["""<section class="card-content" data-jobid="fe76d172-235e-4fc7-a6dc-c7c83b8e679f" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail is-loaded"><img alt="LocumTenens.com" src="https://media.newjobs.com/clu/x617/x617517hjsx/branding/158525/Locumtenenscom-logo.jpg"/></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="327032435" data-m_impr_j_jobid="1128297" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.75" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9967" data-m_impr_j_occid="11870" data-m_impr_j_p="24" data-m_impr_j_postingid="fe76d172-235e-4fc7-a6dc-c7c83b8e679f" data-m_impr_j_pvc="track5locum" data-m_impr_s_t="t" data-m_impr_uuid="74a33bc2-833b-4055-af0b-548ba87f8f45" href="https://job-openings.monster.com/radiologist-needed-for-locum-tenens-coverage-in-new-york-manhattan-ny-us-locumtenens-com/fe76d172-235e-4fc7-a6dc-c7c83b8e679f" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Radiologist Needed for Locum Tenens Coverage in New York&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_LocumTenens.com&quot;,&quot;eVar31&quot;:&quot;Manhattan_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-15T12:00&quot;,&quot;eVar53&quot;:&quot;2900470001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;logo&quot;}')">Radiologist Needed for Locum Tenens Coverage in New York</a></h2></header><div class="company"><span class="name">LocumTenens.com</span><ul class="list-inline"></ul></div><div class="location"><span class="name">Manhattan, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">2 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>""",
                   """<section class="card-content" data-jobid="6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail"></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="333556009" data-m_impr_j_jobid="533623" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.6501" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9496" data-m_impr_j_occid="11870" data-m_impr_j_p="25" data-m_impr_j_postingid="6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" data-m_impr_j_pvc="70ec8331-6e79-4c9f-8681-2bd12c0a0dd1" data-m_impr_s_t="t" data-m_impr_uuid="e80c5c05-f47d-486c-93e8-a67805dc1c41" href="https://job-openings.monster.com/radiologist-body-imaging-brooklyn-ny-us-envision-physician-services-plantation-rsc/6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Radiologist - Body Imaging&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_Envision Physician Services - Plantation RSC&quot;,&quot;eVar31&quot;:&quot;Brooklyn_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-11T12:00&quot;,&quot;eVar53&quot;:&quot;2900480001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;regular&quot;}')">Radiologist - Body Imaging</a></h2></header><div class="company"><span class="name">Envision Physician Services - Plantation RSC</span><ul class="list-inline"></ul></div><div class="location"><span class="name">Brooklyn, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">6 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>"""]

dummy_html_blob = """<body><div id="ResultsContainer"><section class="card-content">Item1</section><section class="card-content">Item2</section>"""

empty_dummy_html_list = """<section class="card-content"></section>"""

mixed_dummy_html_list = ["""<section class="card-content"></section>""",""" <section class="card-content"><h2 class="title">JobTitle</h2><div class="location">CoolLocation</div><a href="https://job-openings.monster.com/radiologist-body-imaging-brooklyn-ny-us-envision-physician-services-plantation-rsc/6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33"></a></section>"""]

class TestSiteScraper(unittest.TestCase):
    def test_url_generation(self):
       site = 'monster.com'
       query = 'mechanic'
       location = 'tampa'

       generated_url = sh.generate_request_url(site, query, location)

       self.assertEqual(generated_url, 'https://www.monster.com/jobs/search/?q=mechanic&where=Tampa'.lower())

    def test_results_parsing(self):

        site = 'monster.com'
        query = 'radiologist'
        location = 'New York'

        # Check that it parses the existing results correctly.
        parsed_class = sh.parse_relevant_job_data(dummy_html)

        self.assertTrue(query in parsed_class.title)
        self.assertTrue(location.lower() in parsed_class.location)
        self.assertTrue(site in parsed_class.link)

    def test_results_parsing_with_multiple_rows(self):
        site = 'www.monster.com'
        query = 'radiologist'
        location = 'New York'

        parsed_class_list = sh.parse_job_list(dummy_html_list)

        self.assertTrue(all([x.title != None for x in parsed_class_list]))
        self.assertTrue(all([x.location != None for x in parsed_class_list]))
        self.assertTrue(all([x.link != None for x in parsed_class_list]))
        self.assertEqual(len(parsed_class_list), len(dummy_html_list))

    def test_empty_result_parsing_returns_empty(self):
        site = 'monster.com'
        query = 'radiologist'
        location = 'New York'

        parsed_class = sh.parse_relevant_job_data(empty_dummy_html_list)

        self.assertIsNone(parsed_class)

    def test_parsing_multiple_rows_with_empty_rows_returns_cleared_data(self):
        site = 'monster.com'
        query = 'radiologist',
        location = 'New York'

        parsed_list = sh.parse_job_list(mixed_dummy_html_list)

        self.assertTrue(len(mixed_dummy_html_list) > len(parsed_list))

    def test_parsing_monster_query_results_into_multiple_rows(self):

        data_parsed_to_list = sh.parse_html_to_lists(dummy_html_blob)

        self.assertTrue(isinstance(data_parsed_to_list, list))
        self.assertTrue(len(data_parsed_to_list) > 1)

class TestDbInteractions(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, tables=[JobDataDbModel.__table__])

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_results_mapping_to_data_model(self):
        original_result = models.JobDataModel("test_title", "test_location", "test_url")

        final_mapping = dbm.map_job_data_model_to_db(original_result)

        self.assertEqual(final_mapping.title, "test_title")
        self.assertEqual(final_mapping.location, "test_location")
        self.assertEqual(final_mapping.link, "test_url")
        self.assertEqual(final_mapping.has_been_emailed, False)

    def test_multiple_results_mapping_to_data_model(self):
        original_results = [models.JobDataModel("test_title_01", "test_location_01", "test_url_01"),
                            models.JobDataModel("test_title_02", "test_location_02", "test_url_02")]

        final_results = dbm.map_job_data_models_to_db_models(original_results)

        self.assertEqual(len(final_results), len(original_results))

        for i in range(len(original_results)):
            self.assertNotEqual(type(original_results[i]), type(final_results[i]))
            self.assertEqual(original_results[i].title, final_results[i].title)
            self.assertEqual(original_results[i].location, final_results[i].location)
            self.assertEqual(original_results[i].link, final_results[i].link)

    def test_results_save_to_database(self):
        model = JobDataDbModel(title="test_job", location="test_location", link="test_link", has_been_emailed=False)

        self.session.add(model)
        self.session.commit()

        saved_data = self.session.query(JobDataDbModel).all()

        self.assertEqual(len(saved_data), 1)

        returned_row = saved_data[0]

        self.assertEqual(model.id, 1)
        self.assertTrue(model.__dict__ == returned_row.__dict__)

    def test_multiple_results_save_to_database(self):
        models = [JobDataDbModel(title='test_job_01', location='test_location_01', link='test_link_01', has_been_emailed=False),
                  JobDataDbModel(title='test_job_02', location='test_location_02', link='test_link_02', has_been_emailed=False)]

        for model in models:
            self.session.add(model)

        self.session.commit()

        saved_data = self.session.query(JobDataDbModel).all()

        self.assertEqual(len(saved_data), len(models))

        for i in range(len(saved_data)):
            self.assertEqual(models[i].id, i + 1)
            self.assertTrue(models[i].__dict__ == saved_data[i].__dict__)

class TestHtmlGeneration(unittest.TestCase):

    def test_html_generated_for_single_class(self):
        original_model = models.JobDataModel("title", "location", "url")

        generated_row = html_gen.generate_row_from_job_data(original_model)

        soup = BeautifulSoup(generated_row, 'html.parser')

        title_elem = soup.find('h3')
        location_elem = soup.find('p')
        url_elem = soup.find('a')

        self.assertEqual(original_model.title, title_elem.text)
        self.assertTrue(original_model.location in location_elem.text)
        self.assertEqual(original_model.link, url_elem['href'])

    def test_html_generated_for_multiple_classes(self):
        original_models = [models.JobDataModel("title_01", "location_01", "url_01"),
                           models.JobDataModel("title_02", "location_02", "url_02")]

        generated_rows = html_gen.generate_rows_from_job_data_list(original_models)

        for i in range(len(original_models)):

            soup = BeautifulSoup(generated_rows[i], 'html.parser')

            html_row = soup.find('tr')

            title_elem = html_row.find('h3')
            location_elem = html_row.find('p')
            url_elem = html_row.find('a')

            self.assertEqual(original_models[i].title, title_elem.text)
            self.assertTrue(original_models[i].location in location_elem.text)
            self.assertEqual(original_models[i].link, url_elem['href'])


if __name__ == '__main__':
    unittest.main()
