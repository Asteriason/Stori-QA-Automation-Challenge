import pytest
from utilities.environment import setup_browser, teardown_browser
from utilities.actions import Actions
from locators.locators import Locators, CssLocators

@pytest.fixture(scope="session")
def driver():
    """
    Setup browser for the test session and navigate to the base URL.
    """
    driver = setup_browser()
    actions = Actions(driver)
    # Load the webpage only once for all test cases
    data = actions.read_csv_data("data/test_data.csv")
    actions.open_url(data["url"])
    yield driver
    teardown_browser(driver)

@pytest.fixture(scope="function")
def actions(driver):
    """
    Provide a fresh instance of the Actions class for each test case.
    """
    return Actions(driver)

@pytest.fixture(scope="function")
def data(actions):
    """
    Load test data from the CSV file for each test case.
    """
    return actions.read_csv_data("data/test_data.csv")

def test_case_suggestion_class(actions, data):
    """
    Test Case: Suggestion Class Example
    """
    print("Executing Test Case: Suggestion Class Example")

    # Use the encapsulated method to handle the suggestion class
    actions.handle_suggestion_class(
        Locators.SUGGESTION_CLASS_EXAMPLE_INPUT,
        data["input_text"],
        Locators.SUGGESTION_COUNTRY_TEMPLATE,
        data["country"]
    )

def test_case_dropdown_example(actions, data):
    """
    Test Case: Dropdown Example
    """
    print("Executing Test Case 2: Dropdown Example")

    # Use the encapsulated method to handle the dropdown selection
    actions.handle_dropdown_example(
        Locators.DROPDOWN_OPTION,
        data["dropdown_option_1"],
        data["dropdown_option_2"]
    )

def test_case_new_window(actions, data):
    """
    Test Case 3: Button Example - Verifies the new window and its content.
    """
    print("Executing Test Case: New Window Content Verification")
    actions.validate_window_content(
        Locators.OPEN_WINDOW_BUTTON,
        data["heading_xpath"],
        data["paragraph_xpath"],
        screenshot_name="new_window_verification"
    )

def test_case_switch_tab(actions):
    """
    Test Case 4: Switch Tab Example
    """
    print("Executing Test Case: Switch Tab Example")
    actions.validate_tab_content(
        Locators.OPEN_TAB_BUTTON,
        Locators.VIEW_ALL_COURSES_BUTTON,
        screenshot_name="switch_tab_verification"
    )


def test_case_alert_input(actions, data):
    """
    Test Case: Alert Input
    """
    print("Executing Test Case: Alert Input")
    actions.handle_alert_interaction(
        Locators.ALERT_INPUT,
        data["alert_input_text"],
        Locators.ALERT_BUTTON,
        Locators.CONFIRM_BUTTON,
        data["expected_text"]
    )


def test_case_web_table(actions, data):
    """
    Test Case: Web Table Example
    Objective: Print the number of courses priced at $25 and their names.
    """
    print("Executing Test Case: Web Table Example")

    # Get courses priced at $25
    actions.get_courses_with_price(data["course_price"])

def test_case_web_table_engineers(actions):
    """
    Test Case: Web Table Fixed Header
    Objective: Print the names of all engineers in the table.
    """
    print("Executing Test Case: Web Table Fixed Header")

    # Get the names of all engineers
    engineers = actions.get_engineers_names(Locators.ENGINEERS_NAMES)

    # Assert the number of engineers is as expected (optional)
    actions.validate_engineers_found(engineers)

def test_case_iframe_highlighted_text(actions):
    """
    Test Case: iFrame Example
    Objective: Print the highlighted text inside the iFrame.
    """
    print("Executing Test Case: iFrame Example")

    # Use the encapsulated method to retrieve the highlighted text
    highlighted_text = actions.handle_iframe_highlighted_text(
        Locators.IFRAME_LOCATOR,
        Locators.HIGHLIGHTED_TEXT_LOCATOR
    )
    # Log the result
    print(f"[PASS] Highlighted Text: {highlighted_text}")

