import pytest,json, os

@pytest.fixture(scope="module")
def category_map():
    """Load the category map JSON once for all tests."""
    with open("category_map.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("category, expected", [
    ("tourism.sights.memorial", "memorial"),
    ("tourism.sights.place_of_worship.church", "church"),
    ("tourism.sights.tower", "tower"),
    ("building.historic", "historic building"),
    ("building.place_of_worship", "place of worship"),
    ("religion.place_of_worship.christianity", "church"),
    ("entertainment.museum", "museum"),
    ("education.library", "library"),
    ("highway.secondary", "road"),
    ("wheelchair.limited", "limited wheelchair access"),
    ("unknown.category.type", "type"), #this is for fallback
])
def test_category_mapping(category_map, category, expected):
    result = category_map.get(category, category.split(".")[-1])
    assert result == expected
