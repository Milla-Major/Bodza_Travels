import os, pytest
from bs4 import BeautifulSoup

HTML_DIR = "templates"
CSS_PATH = "static/css/style.css"

@pytest.fixture
def index_html():
    with open(os.path.join(HTML_DIR, "index.html"), encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

@pytest.fixture
def style_css():
    with open(CSS_PATH, encoding="utf-8") as f:
        return f.read()

def test_title(index_html):
    assert index_html.title is not None
    assert "Bodza Travels" in index_html.title.text

def test_navbar_links(index_html):
    links = [a["href"] for a in index_html.select(".nav-item")]
    for link in ["/", "/about", "/recent_places"]:
        assert link in links

def test_support_button(index_html):
    support = index_html.select_one(".nav-support")
    assert support is not None
    assert support["href"] == "/support"

def test_form_elements(index_html):
    form = index_html.find("form", {"id": "cityForm"})
    assert form is not None
    assert form.find("input", {"id": "cityInput"}) is not None
    assert form.find("button", {"type": "submit"}) is not None

def test_autocomplete_box(index_html):
    ac_box = index_html.find("div", {"id": "autocomplete-list"})
    assert ac_box is not None

def test_img_alt_text(index_html):
    for img in index_html.find_all("img"):
        assert img.has_attr("alt")

def test_footer_content(index_html):
    footer = index_html.select_one(".footer")
    assert footer is not None
    assert "Milla Major" in footer.text

def test_main_css_classes(style_css):
    for cls in [".navbar", ".footer", ".main-content", ".nav-item"]:
        assert cls in style_css

def test_media_queries(style_css):
    assert "@media" in style_css

def test_key_colors_fonts(style_css):
    assert "#00dd58" in style_css
    assert "font-family: 'Segoe UI'" in style_css

def test_autocomplete_style(style_css):
    assert ".autocomplete-items" in style_css
    assert "box-shadow" in style_css

def test_button_hover(style_css):
    assert ".search-box button:hover" in style_css
    assert "background-color" in style_css
