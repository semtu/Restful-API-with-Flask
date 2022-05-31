import unittest
import requests

class APITest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/api"
    PING_URL = "{}/ping".format(API_URL)
    POST_URL = "{}/posts".format(API_URL)

    # Check that Ping returns 200 status code
    def test_1_ping_200(self):
        self.assertEqual(requests.get(APITest.PING_URL).status_code, 200)

    # Check that posts return 200 if tags are present or absent and direction parameters are valid
    def test_2_tags_sortby(self):
        self.assertEqual(requests.get("{}".format(APITest.POST_URL)).status_code, 200)
        self.assertEqual(
            requests.get("{}?tags=tech".format(APITest.POST_URL)).status_code, 200
        )
        self.assertEqual(
            requests.get("{}?direction=dsc".format(APITest.POST_URL)).status_code, 200
        )

    # Check that posts returns 400 if direction parameter is invalid
    def test_3_tags_sortby(self):
        self.assertEqual(
            requests.get("{}?direction=mean".format(APITest.POST_URL)).status_code, 400
        )

    # Check that content type is Json
    def test_4_content_type(self):
        self.assertEqual(
            requests.get(
                "{}?tags=business,tech&direction=dsc".format(APITest.POST_URL)
            ).headers["content-type"],
            "application/json",
        )
