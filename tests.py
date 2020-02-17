import unittest
import scrape_helpers as sh
from bs4 import BeautifulSoup

dummy_html = """<section class="card-content" data-jobid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail"></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="419414642" data-m_impr_j_jobid="194890933" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.75" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9967" data-m_impr_j_occid="11870" data-m_impr_j_p="1" data-m_impr_j_postingid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" data-m_impr_j_pvc="pandologicpx" data-m_impr_s_t="t" data-m_impr_uuid="66592e1d-3b1b-448a-9646-b9149c2cfd42" href="https://job-openings.monster.com/neurointerventional-radiologist-new-york-ny-us-confidential/bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Neurointerventional Radiologist&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_Confidential&quot;,&quot;eVar31&quot;:&quot;New York_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-13T12:00&quot;,&quot;eVar53&quot;:&quot;2900480001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;regular&quot;}')">Neurointerventional Radiologist</a></h2></header><div class="company"><span class="name">Confidential</span><ul class="list-inline"></ul></div><div class="location"><span class="name">New York, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">3 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>
"""

class TestUrlGeneration(unittest.TestCase):
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
        parsed_class = sh.parse_relevant_job_data(dummy_html, site, query, location)

        print(parsed_class.title)
        print(query)
        self.assertTrue(query in parsed_class.title)
        self.assertTrue(location.lower() in parsed_class.location)
        self.assertTrue(site in parsed_class.link)

if __name__ == '__main__':
    unittest.main()
