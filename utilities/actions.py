import csv
from datetime import datetime  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from locators.locators import Locators
from selenium.common.exceptions import TimeoutException  # Import this for handling timeouts


class Actions:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        """
        Opens the specified URL in the browser and asserts the page loads successfully.
        """
        self.driver.get(url)
        assert self.driver.current_url == url, f"URL did not load correctly. Expected: {url}, Got: {self.driver.current_url}"
        print(f"[PASS] Successfully opened URL: {url}")

    def enter_text_for_suggestions(self, locator, text):
        """
        Enters text into an input field identified by the locator and asserts the input value.
        """
        element = self.driver.find_element(By.XPATH, locator)
        element.clear()
        element.send_keys(text)
        assert element.get_attribute("value") == text, f"Text input failed. Expected: {text}, Got: {element.get_attribute('value')}"
        print(f"[PASS] Successfully entered text '{text}' in field: {locator}")

    def select_from_suggestions(self, locator_template, country):
        """
        Selects an option from the suggestions dropdown dynamically and asserts the selection.
        """
        # Format the dynamic locator with the provided country
        dynamic_locator = locator_template.format(country)
        
        # Wait for the element to be visible
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, dynamic_locator))
        )
        
        # Click on the dynamically located suggestion
        self.driver.find_element(By.XPATH, dynamic_locator).click()
        
        # Validate that the correct country was selected
        dropdown_value = self.driver.find_element(By.XPATH, Locators.SUGGESTION_CLASS_EXAMPLE_INPUT).get_attribute("value")
        assert dropdown_value == country, f"Dropdown selection failed. Expected: {country}, Got: {dropdown_value}"
        
        print(f"[PASS] Successfully selected '{country}' from suggestions.")
        
        # Take a screenshot after selecting the suggestion
        self.take_screenshot(f"dropdown_selected_{country}")


    def read_csv_data(self, file_path):
        """
        Reads hardcoded data from a CSV file and returns a dictionary.
        """
        absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file_path)
        data = {}
        with open(absolute_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row['key']] = row['value']
        print(f"[PASS] Successfully read data from CSV file: {file_path}")
        return data

    def verify_element_visible(self, locator):
        """
        Verifies that an element is visible on the page.
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locator))
        )
        assert element.is_displayed(), f"Element not visible: {locator}"
        print(f"[PASS] Element is visible: {locator}")

    def assert_text_in_element(self, locator, expected_text):
        """
        Asserts that the text of an element matches the expected text.
        """
        element = self.driver.find_element(By.XPATH, locator)
        actual_text = element.text
        assert actual_text == expected_text, f"Text assertion failed. Expected: {expected_text}, Got: {actual_text}"
        print(f"[PASS] Text in element '{locator}' matches expected: {expected_text}")

    def select_dropdown_option(self, dropdown_locator, option_position):
        """
        Selects an option from the dropdown based on position.
        """
        option_locator = dropdown_locator.format(option_position)
        dropdown_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, option_locator))
        )
        dropdown_option.click()
        print(f"[PASS] Successfully selected option at position {option_position}")
        self.take_screenshot("dropdown_options")

    
    def open_window_and_verify_text(self, openwindow_button_locator, heading_xpath, paragraph_xpath):
        """
        Clicks the button to open a new window, switches to it, verifies the expected text, 
        and closes the new window. If the expected text is not found, the test fails.
        
        Args:
            openwindow_button_locator (str): XPath for the button that opens the new window.
            heading_xpath (str): XPath to locate the heading text (e.g., "30 day Money Back Guarantee").
            paragraph_xpath (str): XPath to locate the paragraph text to validate.
        """
        # Get the current number of open windows
        initial_window_handles = self.driver.window_handles
        initial_window_count = len(initial_window_handles)

        # Click the button to open the window
        openwindow_button = self.driver.find_element(By.XPATH, openwindow_button_locator)
        openwindow_button.click()

        # Wait for a new window to appear
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > initial_window_count
        )

        # Get the updated list of window handles
        updated_window_handles = self.driver.window_handles

        # Assert that a new window was opened
        assert len(updated_window_handles) > initial_window_count, "No new window was opened."
        print(f"[PASS] New window opened successfully. Total windows: {len(updated_window_handles)}")

        # Get the handle of the new window
        new_window_handle = [handle for handle in updated_window_handles if handle not in initial_window_handles][0]

        # Switch to the new window
        self.driver.switch_to.window(new_window_handle)

        # Verify the heading text
        try:
            heading_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, heading_xpath))
            )
            assert heading_element.is_displayed(), "[FAIL] Heading text is not visible in the new window."
            print(f"[PASS] Heading text '{heading_element.text}' is displayed as expected.")
        except Exception as e:
            raise Exception(f"[FAIL] Heading text verification failed: {str(e)}")

        # Verify the paragraph text
        try:
            paragraph_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, paragraph_xpath))
            )
            assert paragraph_element.is_displayed(), "[FAIL] Paragraph text is not visible in the new window."
            print(f"[PASS] Paragraph text '{paragraph_element.text}' is displayed as expected.")
        except Exception as e:
            raise Exception(f"[FAIL] Paragraph text verification failed: {str(e)}")

        # Close the new window and switch back to the original
        self.driver.close()
        self.driver.switch_to.window(initial_window_handles[0])
        print(f"[INFO] Closed the new window and switched back to the main window.")

    def handle_suggestion_class(self, input_locator, input_text, suggestion_locator_template, suggestion_value):
        """
        Handles entering text in a suggestion input field and selecting a suggestion.

        Args:
            input_locator (str): XPath to locate the suggestion input field.
            input_text (str): Text to enter in the input field.
            suggestion_locator_template (str): Template XPath to locate the suggestion dropdown.
            suggestion_value (str): The suggestion to select.

        Returns:
            str: The selected suggestion value.

        Raises:
            Exception: If suggestion selection fails.
        """
        try:
            # Enter text in the suggestion input field
            self.enter_text_for_suggestions(input_locator, input_text)

            # Select the suggestion
            self.select_from_suggestions(suggestion_locator_template, suggestion_value)

            print(f"[PASS] Successfully handled suggestion class with input: {input_text} and selected: {suggestion_value}")
        except Exception as e:
            raise Exception(f"[FAIL] Failed to handle suggestion class: {e}")

    def handle_dropdown_example(self, dropdown_locator, option_1, option_2):
        """
        Handles selecting multiple options from a dropdown.

        Args:
            dropdown_locator (str): XPath template for dropdown options.
            option_1 (str): First option to select.
            option_2 (str): Second option to select.

        Raises:
            Exception: If dropdown selection fails.
        """
        try:
            # Select the first dropdown option
            self.select_dropdown_option(dropdown_locator, option_1)

            # Select the second dropdown option
            self.select_dropdown_option(dropdown_locator, option_2)

            print(f"[PASS] Successfully selected dropdown options: {option_1}, {option_2}")
        except Exception as e:
            raise Exception(f"[FAIL] Failed to handle dropdown example: {e}")


    def click_open_tab(self, opentab_locator):
        """
        Clicks the 'Open Tab' button and verifies that a new tab is opened.
        """
        # Store the current window handle
        original_window = self.driver.current_window_handle
        initial_tabs = self.driver.window_handles

        # Click the 'Open Tab' button
        open_tab_button = self.driver.find_element(By.CSS_SELECTOR, opentab_locator)
        open_tab_button.click()

        # Wait for the new tab to open
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > len(initial_tabs)
        )
        print("[PASS] New tab opened successfully.")

        # Return the original window handle for later use
        return original_window

    def handle_alert(self, alert_type="alert", expected_text=None):
        """
        Handles alerts and confirm dialogs.
        :param alert_type: 'alert' or 'confirm'
        :param expected_text: Text to validate in the alert/confirm dialog
        :return: The text of the alert
        """
        alert = self.driver.switch_to.alert
        alert_text = alert.text

        # Print the alert text
        print(f"{alert_type.capitalize()} Text: {alert_text}")

        # Validate the alert/confirm text if expected_text is provided
        if expected_text:
            assert alert_text == expected_text, f"Expected '{expected_text}', but got '{alert_text}'"

        alert.accept()  # Accept the alert
        return alert_text

    def validate_alert_text(self, expected_text):
        """
        Handles alerts and confirms that the alert text matches the expected text.

        Args:
            expected_text (str): The text expected to appear in the alert.

        Raises:
            Exception: If the alert text does not match the expected text.
        """
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print(f"[INFO] Alert Text: {alert_text}")

            # Validate the alert text
            if expected_text:
                if alert_text != expected_text:
                    raise Exception(f" (Expected: '{expected_text}', Got: '{alert_text}')")
                print("[PASS] Alert text validation successful.")

            # Accept the alert
            alert.accept()
            print("[INFO] Alert accepted.")
        except Exception as e:
            print(f"[FAIL] Alert validation failed. Error: {e}")
            raise

    def handle_alert_interaction(self, input_locator, input_text, alert_button_locator, confirm_button_locator, expected_text=None):
        """
        Handles alert interactions, including entering text, triggering alerts, and validating confirm dialog text.

        Args:
            input_locator (str): Locator for the input field to send text.
            input_text (str): Text to enter into the input field.
            alert_button_locator (str): Locator for the alert button.
            confirm_button_locator (str): Locator for the confirm button.
            expected_text (str, optional): Expected text in the confirm alert. Defaults to None.

        Raises:
            Exception: If the expected text validation fails.
        """
        try:
            # Step 1: Enter the text into the input field
            self.enter_text(input_locator, input_text)

            # Step 2: Trigger the Alert
            self.click_element(alert_button_locator)
            alert = self.driver.switch_to.alert
            print(f"[INFO] Alert Text: {alert.text}")
            alert.accept()  # Dismiss the alert

            # Step 3: Trigger the Confirm dialog
            self.enter_text(input_locator, input_text)
            self.click_element(confirm_button_locator)
            confirm = self.driver.switch_to.alert
            confirm_text = confirm.text
            print(f"[INFO] Confirm Dialog Text: {confirm_text}")

            # Step 4: Validate the confirm dialog text, if expected text is provided
            if expected_text:
                assert confirm_text == expected_text, f"[FAIL] Expected '{expected_text}', but got '{confirm_text}'"
                print("[PASS] Confirm dialog text matches expected.")

            confirm.accept()  # Accept the confirm dialog

        except Exception as e:
            raise Exception(f"[FAIL] Alert interaction failed: {e}")


    def validate_window_content(self, open_button_locator, heading_locator, paragraph_locator, screenshot_name="new_window"):
        """
        Validates the content of a new window.

        Args:
            open_button_locator (str): Locator for the button to open the new window.
            heading_locator (str): Locator for the heading text in the new window.
            paragraph_locator (str): Locator for the paragraph text in the new window.
            screenshot_name (str): Name for the screenshot file.

        Raises:
            Exception: If the validation fails at any step.
        """
        original_window = self.driver.current_window_handle
        try:
            # Click button to open the new window
            self.click_element(open_button_locator)

            # Wait for the new window to appear
            WebDriverWait(self.driver, 10).until(lambda driver: len(driver.window_handles) > 1)
            new_window_handle = [handle for handle in self.driver.window_handles if handle != original_window][0]

            # Switch to the new window
            self.driver.switch_to.window(new_window_handle)

            # Validate heading text
            heading_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, heading_locator))
            )
            assert heading_element.is_displayed(), "[FAIL] Heading text not displayed."
            print(f"[PASS] Heading text: {heading_element.text}")

            # Validate paragraph text
            paragraph_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, paragraph_locator))
            )
            assert paragraph_element.is_displayed(), "[FAIL] Paragraph text not displayed."
            print(f"[PASS] Paragraph text: {paragraph_element.text}")

            # Take a screenshot
            self.take_screenshot(screenshot_name)

        except Exception as e:
            raise Exception(f"[FAIL] Validation failed for new window content: {e}")

        finally:
            # Close the new window and switch back to the original
            self.driver.close()
            self.driver.switch_to.window(original_window)
            print("[INFO] Cleaned up new window and returned to the original window.")


    def cleanup_windows_except(self, original_window):
        """
        Closes all windows except the original one and switches back to the original window.
        """
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(original_window)
        print("[PASS] Cleaned up additional windows and switched to the original window.")

    def click_element(self, locator):
        """
        Clicks an element located by a CSS selector or XPath.
        """
        element = self.driver.find_element(By.XPATH, locator)
        element.click()
        print(f"[PASS] Clicked element with locator: {locator}")

    def click_element_by_css(self, locator):
        """
        Clicks an element located by a CSS selector.
        """
        try:
            print(f"[DEBUG] Waiting for element to be clickable: {locator}")
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
            )
            element.click()
            print(f"[PASS] Clicked element with CSS selector: {locator}")
        except Exception as e:
            print(f"[FAIL] Could not click element with CSS selector: {locator}. Error: {e}")
            raise

    def enter_text(self, locator, text):
        """
        Enters text into an input field located by a CSS selector or XPath.
        """
        element = self.driver.find_element(By.XPATH, locator)
        element.clear()
        element.send_keys(text)
        print(f"[PASS] Entered text '{text}' into element with locator: {locator}")

    def validate_tab_content(self, open_tab_button_locator, content_locator, screenshot_name="new_tab"):
        """
        Validates the content of a new tab.

        Args:
            open_tab_button_locator (str): Locator for the button to open the new tab.
            content_locator (str): Locator for the content element in the new tab.
            screenshot_name (str): Name for the screenshot file.

        Raises:
            Exception: If the validation fails at any step.
        """
        original_window = self.driver.current_window_handle
        try:
            # Click button to open a new tab
            self.click_element(open_tab_button_locator)

            # Wait for the new tab to appear
            WebDriverWait(self.driver, 10).until(lambda driver: len(driver.window_handles) > 1)
            new_tab_handle = [handle for handle in self.driver.window_handles if handle != original_window][0]

            # Switch to the new tab
            self.driver.switch_to.window(new_tab_handle)

            # Validate the content element
            content_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, content_locator))
            )
            assert content_element.is_displayed(), "[FAIL] Content element not displayed."
            print(f"[PASS] Content element found: {content_element.text}")

            # Take a screenshot
            self.take_screenshot(screenshot_name)

        except Exception as e:
            raise Exception(f"[FAIL] Validation failed for new tab content: {e}")

        finally:
            # Close the new tab and switch back to the original
            self.driver.close()
            self.driver.switch_to.window(original_window)
            print("[INFO] Cleaned up new tab and returned to the original window.")



    def click_open_tab(self, tab_button_locator):
        original_window = self.driver.current_window_handle

        # Click the Open Tab button
        print(f"[INFO] Clicking Open Tab button with locator: {tab_button_locator}")
        self.click_element(tab_button_locator)

        # Wait for the new tab to open
        print("[INFO] Waiting for new tab to open...")
        self.wait_for_new_tab()

        # Print window handles
        print(f"[INFO] Window handles after clicking tab: {self.driver.window_handles}")

        # Switch to the new tab
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                print(f"[PASS] Switched to new tab with handle: {handle}")
                break

        return original_window

    def take_screenshot(self, name):
        """Take a screenshot with a unique name."""
        # Create the directory if it doesn't exist
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # Generate a timestamped filename for the screenshot
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Ensure correct usage of datetime
        screenshot_path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")

        # Save the screenshot
        self.driver.save_screenshot(screenshot_path)
        print(f"[INFO] Screenshot saved at: {screenshot_path}")
        return screenshot_path

    def scroll_and_screenshot(self, element_locator, screenshot_name):
        """
        Scrolls to the specified element and takes a screenshot.
        
        :param element_locator: The locator (XPATH or CSS) for the element to scroll to.
        :param screenshot_name: The name of the screenshot file (without extension).
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_locator))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"[PASS] Scrolled to the element located by: {element_locator}")

        # Save the screenshot
        screenshot_path = os.path.join("screenshots", f"{screenshot_name}.png")
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(screenshot_path)
        print(f"[PASS] Screenshot saved at: {screenshot_path}")

    def handle_new_tab(self, button_locator, original_window, screenshot_name):
        """
        Handles actions in the new tab, verifies button presence, and switches back.
        :param button_locator: Locator for the button in the new tab.
        :param original_window: Handle of the original window.
        :param screenshot_name: Name for the screenshot.
        """
        try:
            # Wait for the new tab to open
            print("[INFO] Waiting for new tab to load...")
            WebDriverWait(self.driver, 10).until(lambda driver: len(driver.window_handles) > 1)

            # Switch to the new tab
            new_tab = [handle for handle in self.driver.window_handles if handle != original_window][0]
            self.driver.switch_to.window(new_tab)
            print("[PASS] Switched to the new tab.")

            # Wait for the element in the new tab to load
            print("[INFO] Waiting for element in the new tab...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, button_locator))
            )
            print("[PASS] Element found in the new tab.")

            # Scroll to the element and take a screenshot
            element = self.driver.find_element(By.XPATH, button_locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.take_screenshot(screenshot_name)
            print(f"[PASS] Screenshot saved as {screenshot_name}")

        except TimeoutException:
            raise Exception(f"[FAIL] Element with locator '{button_locator}' not found within the timeout period.")
        except Exception as e:
            raise Exception(f"Unexpected error while handling the new tab: {str(e)}")
        finally:
            # Close the new tab and switch back to the original
            print("[INFO] Closing the new tab...")
            self.driver.close()
            print("[INFO] Switching back to the original tab...")
            if original_window in self.driver.window_handles:
                self.driver.switch_to.window(original_window)
                print("[PASS] Switched back to the original tab.")
            else:
                print("[FAIL] Original tab is no longer available.")


    def click_open_tab(self, open_tab_locator):
        """
        Clicks the 'Open Tab' button and returns the original window handle.
        """
        original_window = self.driver.current_window_handle
        self.click_element(open_tab_locator)
        print("[PASS] Clicked the 'Open Tab' button.")
        return original_window

    def cleanup_all_tabs_except(self, original_tab):
        """
        Closes all tabs except the specified original tab.
        :param original_tab: The handle of the original tab to keep open.
        """
        if not self.driver:
            print("[WARN] WebDriver session is invalid or already closed. Skipping cleanup.")
            return
        try:
            for handle in self.driver.window_handles:
                if handle != original_tab:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                    print(f"[INFO] Closed tab with handle: {handle}")
            self.driver.switch_to.window(original_tab)
            print("[PASS] Cleaned up additional tabs and switched to the original tab.")
        except Exception as e:
            print(f"[ERROR] Failed during cleanup: {e}")

    def get_courses_with_price(self, price):
        """
        Finds and prints the count and names of courses with the given price.
        
        :param price: The price to filter courses by (e.g., 25)
        """
        price_selector = f"#product tbody tr td:nth-child(3)"
        course_name_selector_template = "#product tbody tr:nth-child({}) td:nth-child(2)"

        # Find all price cells matching the criteria
        price_cells = self.driver.find_elements(By.CSS_SELECTOR, price_selector)
        matching_courses = []

        for i, price_cell in enumerate(price_cells, start=1):
            if price_cell.text == str(price):
                # Use the index to locate the course name cell
                course_name_cell = self.driver.find_element(By.CSS_SELECTOR, course_name_selector_template.format(i))
                matching_courses.append(course_name_cell.text)

        print(f"[INFO] Number of courses with price ${price}: {len(matching_courses)}")
        for course in matching_courses:
            print(f"[INFO] Course Name: {course}")

    def get_engineers_names(self, engineers_xpath):
        """
        Finds and returns the names of all engineers in the Web Table Fixed Header.

        :return: List of names of engineers
        """
        engineer_names = []
        try:
            # Using XPath
            engineer_elements = self.driver.find_elements(By.XPATH, engineers_xpath)

            for element in engineer_elements:
                engineer_names.append(element.text)
            
            print(f"[INFO] Engineers found using XPath: {', '.join(engineer_names)}")
        except Exception as e:
            print(f"[FAIL] Failed to get engineers' names. Error: {e}")
            raise

        return engineer_names


    def get_highlighted_text(self, iframe_locator, highlighted_text_locator, expected_text):
        """
        Switches to the iFrame and retrieves the highlighted text, validating it against the expected string.

        Args:
            iframe_locator (str): XPath to locate the iFrame.
            highlighted_text_locator (str): XPath to locate the highlighted text in blue.
            expected_text (str): The exact text expected to be highlighted.

        Returns:
            str: The highlighted text.

        Raises:
            Exception: If the highlighted text does not match the expected string or an error occurs.
        """
        try:
            # Switch to the iFrame
            iframe = self.driver.find_element(By.XPATH, iframe_locator)
            self.driver.switch_to.frame(iframe)

            # Get the highlighted text element
            highlighted_element = self.driver.find_element(By.XPATH, highlighted_text_locator)

            # Scroll to the highlighted element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", highlighted_element)
            print(f"[INFO] Scrolled to the highlighted element.")

            # Extract the text of the highlighted element
            highlighted_text = highlighted_element.text

            # Validate the highlighted text matches the expected string
            assert highlighted_text == expected_text, f"[FAIL] Highlighted text does not match. Expected: '{expected_text}', Got: '{highlighted_text}'"
            print(f"[PASS] Highlighted text matches the expected string: '{highlighted_text}'")

            # Take a screenshot after scrolling
            self.take_screenshot("Highlighted_text")

            # Switch back to the main content
            self.driver.switch_to.default_content()

            return highlighted_text

        except Exception as e:
            print(f"[FAIL] Failed to get highlighted text. Error: {e}")
            raise


    def validate_engineers_found(self, engineers):
        """
        Validates that engineers are found in the table.

        Args:
            engineers (list): List of engineer names.

        Raises:
            Exception: If no engineers are found.
        """
        if not engineers:
            raise Exception("[FAIL] No engineers found in the table.")
        print("[PASS] Engineers found in the table:")
        for name in engineers:
            print(f"- {name}")
