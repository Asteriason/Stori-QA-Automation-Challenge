import pytest
import os
from datetime import datetime
from pytest_html import extras


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure or specific test parts
    and embed them into the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    pytest_html = item.config.pluginmanager.getplugin('html')

    if report.when == 'call':  # For the actual test execution
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)

            # Take and save the screenshot
            test_name = item.name
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"[INFO] Screenshot captured for test '{test_name}' at {screenshot_path}")

            # Embed screenshot into the HTML report
            extra.append(extras.image(screenshot_path))
        report.extra = extra
