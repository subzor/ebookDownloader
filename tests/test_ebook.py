
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend"))
from ebook import Ebook

details = {
    "ebook_name" : "Kamasutra of eMail Marketing Deliverability",
    "name" : "Daniel Test",
    "email" : "danieltest@cezar-trans.com",
    "company" : "Recruitment task",
    "website" : "www.google.pl",
    "country" : "Poland",
    "country_code" : "+48",
    "phone" : "555666777"
}

def test_should_pass_when_ebookExist():
    
    test = Ebook(account=details)
    test.get_url()

    is_file = os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(__file__)),"download" ,details["ebook_name"] + ".pdf"))

    assert is_file == True




