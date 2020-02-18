import unittest
import scrape_helpers as sh
from bs4 import BeautifulSoup

dummy_html = """<section class="card-content" data-jobid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail"></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="419414642" data-m_impr_j_jobid="194890933" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.75" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9967" data-m_impr_j_occid="11870" data-m_impr_j_p="1" data-m_impr_j_postingid="bf50682c-f3b0-4b30-bd87-94682b7f38f6" data-m_impr_j_pvc="pandologicpx" data-m_impr_s_t="t" data-m_impr_uuid="66592e1d-3b1b-448a-9646-b9149c2cfd42" href="https://job-openings.monster.com/neurointerventional-radiologist-new-york-ny-us-confidential/bf50682c-f3b0-4b30-bd87-94682b7f38f6" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Neurointerventional Radiologist&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_Confidential&quot;,&quot;eVar31&quot;:&quot;New York_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-13T12:00&quot;,&quot;eVar53&quot;:&quot;2900480001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;regular&quot;}')">Neurointerventional Radiologist</a></h2></header><div class="company"><span class="name">Confidential</span><ul class="list-inline"></ul></div><div class="location"><span class="name">New York, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">3 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>
"""

dummy_html_list = ["""<section class="card-content" data-jobid="fe76d172-235e-4fc7-a6dc-c7c83b8e679f" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail is-loaded"><img alt="LocumTenens.com" src="https://media.newjobs.com/clu/x617/x617517hjsx/branding/158525/Locumtenenscom-logo.jpg"/></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="327032435" data-m_impr_j_jobid="1128297" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.75" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9967" data-m_impr_j_occid="11870" data-m_impr_j_p="24" data-m_impr_j_postingid="fe76d172-235e-4fc7-a6dc-c7c83b8e679f" data-m_impr_j_pvc="track5locum" data-m_impr_s_t="t" data-m_impr_uuid="74a33bc2-833b-4055-af0b-548ba87f8f45" href="https://job-openings.monster.com/radiologist-needed-for-locum-tenens-coverage-in-new-york-manhattan-ny-us-locumtenens-com/fe76d172-235e-4fc7-a6dc-c7c83b8e679f" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Radiologist Needed for Locum Tenens Coverage in New York&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_LocumTenens.com&quot;,&quot;eVar31&quot;:&quot;Manhattan_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-15T12:00&quot;,&quot;eVar53&quot;:&quot;2900470001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;logo&quot;}')">Radiologist Needed for Locum Tenens Coverage in New York</a></h2></header><div class="company"><span class="name">LocumTenens.com</span><ul class="list-inline"></ul></div><div class="location"><span class="name">Manhattan, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">2 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>""",
                   """<section class="card-content" data-jobid="6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" onclick="MKImpressionTrackingMouseDownHijack(this, event)"><div class="flex-row"><div class="mux-company-logo thumbnail"></div><div class="summary"><header class="card-header"><h2 class="title"><a data-bypass="true" data-m_impr_a_placement_id="JSR2CW" data-m_impr_j_cid="3975" data-m_impr_j_coc="" data-m_impr_j_jawsid="333556009" data-m_impr_j_jobid="533623" data-m_impr_j_jpm="1" data-m_impr_j_jpt="2" data-m_impr_j_lat="40.6501" data-m_impr_j_lid="550" data-m_impr_j_long="-73.9496" data-m_impr_j_occid="11870" data-m_impr_j_p="25" data-m_impr_j_postingid="6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" data-m_impr_j_pvc="70ec8331-6e79-4c9f-8681-2bd12c0a0dd1" data-m_impr_s_t="t" data-m_impr_uuid="e80c5c05-f47d-486c-93e8-a67805dc1c41" href="https://job-openings.monster.com/radiologist-body-imaging-brooklyn-ny-us-envision-physician-services-plantation-rsc/6bd5b9bb-f2af-4e9d-819a-0fd929ec8b33" onclick="clickJobTitle('plid=550&amp;pcid=3975&amp;poccid=11870','radiologist',''); clickJobTitleSiteCat('{&quot;events.event48&quot;:&quot;true&quot;,&quot;eVar25&quot;:&quot;Radiologist - Body Imaging&quot;,&quot;eVar66&quot;:&quot;Monster&quot;,&quot;eVar67&quot;:&quot;JSR2CW&quot;,&quot;eVar26&quot;:&quot;_Envision Physician Services - Plantation RSC&quot;,&quot;eVar31&quot;:&quot;Brooklyn_NY_&quot;,&quot;prop24&quot;:&quot;2020-02-11T12:00&quot;,&quot;eVar53&quot;:&quot;2900480001001&quot;,&quot;eVar50&quot;:&quot;PPC&quot;,&quot;eVar74&quot;:&quot;regular&quot;}')">Radiologist - Body Imaging</a></h2></header><div class="company"><span class="name">Envision Physician Services - Plantation RSC</span><ul class="list-inline"></ul></div><div class="location"><span class="name">Brooklyn, NY</span></div></div><div class="meta flex-col"><time datetime="2017-05-26T12:00">6 days ago</time><span class="mux-tooltip applied-only" data-mux="tooltip" title="Applied"><i aria-hidden="true" class="icon icon-applied"></i><span class="sr-only">Applied</span></span><span class="mux-tooltip saved-only" data-mux="tooltip" title="Saved"><i aria-hidden="true" class="icon icon-saved"></i><span class="sr-only">Saved</span></span></div></div></section>"""]


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

    def test_results_parsing_with_multiple_rows(self):
        site = 'www.monster.com'
        query = 'radiologist'
        location = 'New York'

        parsed_class_list = sh.parse_job_list(dummy_html_list, site, query, location)

        print(parsed_class_list)
        print(query)
        self.assertTrue(query in all([x.title for x in parsed_class_list]))
        self.assertTrue(location.lower() in all([x.location for x in parsed_class_list]))
        self.assertTrue(site in all([x.link for x in parsed_class_list]))

if __name__ == '__main__':
    unittest.main()
