# from parent directory, run:
#  > python3 -m unittest a1q6.piwigo_metamorphic_test_suite

import requests
import unittest

API_URL = "https://gallery.patricklam.ca/ws.php"

class PiwigoMetamorphicTestSuite (unittest.TestCase):
    def test_tags_and_subset_of_or(self):
        and_payload = [('format', 'json'), ('method', 'pwg.tags.getImages'), ('tag_name[]', 'fauna'), ('tag_name[]', 'bird'), ('tag_mode_and', 'true')]
        and_response = requests.get(API_URL, params=and_payload)
        and_result = and_response.json()['result']
        self.assertEqual(and_result['paging']['count'], and_result['paging']['total_count'])
        and_hits = list(map(lambda x: x['id'], and_result['images']))

        or_payload = [('format', 'json'), ('method', 'pwg.tags.getImages'), ('tag_name[]', 'fauna'), ('tag_name[]', 'bird'), ('tag_mode_and', 'false')]
        or_response = requests.get(API_URL, params=or_payload)
        or_result = or_response.json()['result']
        self.assertEqual(or_result['paging']['count'], or_result['paging']['total_count'])
        or_hits = list(map(lambda x: x['id'], or_result['images']))

        self.assertTrue(set(and_hits).issubset(or_hits))

    def test_tags_total_images_in_tags_get_list_at_most_sum_of_tags_getimages(self):
        pass

    def test_students_choice_metamorphic(self):
        pass
        
        

