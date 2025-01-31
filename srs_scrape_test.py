import pytest
from bs4 import BeautifulSoup
import requests
from srs_scrape import get_srs


def mock_response():
    # Simulating a mock instead of calling the url while testing

    html = """
    <html>
        <body>
            <table>
                <tr><td>BoatType1</td><td>SRS1</td><td>SRS2</td><td>SRS3</td><td>SRS4</td></tr>
                <tr><td>BoatType1</td><td>SRS1</td><td>SRS2</td><td>SRS3</td><td>SRS4</td></tr>
            </table>
        </body>
    </html>
    """
    
    class MockResponse:
        @property
        def content(self):
            return html.encode("utf-8")
        
    return MockResponse()

@pytest.fixture
def mock_request_get(mocker):
    mocker.patch("requests.get", side_effect=mock_response)

def test_get_srs(mock_request_get):
    #Calling get_srs() and compare with excpected_lst to see if they are the same
    boat_list = get_srs()

    excpected_list = ['1006', '0.949', '0.926', '0.942', '0.922']
    
    assert boat_list[:5] == excpected_list