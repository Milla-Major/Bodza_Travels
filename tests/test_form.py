import os, pytest
from bs4 import BeautifulSoup


HTML_DIR = "templates"

@pytest.fixture
def support_html():
    with open(os.path.join(HTML_DIR, "support.html"), encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

@pytest.fixture
def submitted_html():
    with open(os.path.join(HTML_DIR, "support_submitted.html"), encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_support_form_structure(support_html):
    form = support_html.select_one("form.support-form")
    assert form is not None
    assert form["action"] == "/submit-support"
    assert form["method"].lower() == "post"
    assert form.find("input", {"name": "name"}) is not None
    assert form.find("input", {"name": "email"}) is not None
    assert form.find("textarea", {"name": "message"}) is not None
    assert form.find("button", {"type": "submit"}) is not None

def test_support_submitted_content(submitted_html):
    title = submitted_html.find("h1", class_="title")
    subtitle = submitted_html.find("p", class_="subtitle")
    back_link = submitted_html.find("a", class_="form-back")
    assert title is not None
    assert "Thank you" in title.text
    assert subtitle is not None
    assert "Your message has been received" in subtitle.text
    assert back_link is not None
    assert back_link["href"] == "/"
