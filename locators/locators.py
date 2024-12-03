class Locators:
    #XPath Locators
    SUGGESTION_CLASS_EXAMPLE_INPUT = "//legend[text()='Suggession Class Example']/..//input[@id='autocomplete']"
    SUGGESTION_COUNTRY_TEMPLATE = "//li[@class='ui-menu-item']//div[text()='{}']"
    DROPDOWN = "//select"  
    DROPDOWN_OPTION = "//select/option[position()={}]"  
    OPEN_WINDOW_BUTTON = "//button[@id='openwindow']"
    VIEW_ALL_COURSES_BUTTON = "//a[contains(text(), 'View all Courses')]"
    ALERT_INPUT = "//legend[text()='Switch To Alert Example']/..//input[@id='name']"
    ALERT_BUTTON = "//legend[text()='Switch To Alert Example']/..//input[@id='alertbtn']"
    CONFIRM_BUTTON = "//legend[text()='Switch To Alert Example']/..//input[@id='confirmbtn']"
    OPEN_TAB_BUTTON = "//a[@id='opentab']"
    ENGINEERS_NAMES = "//table[@id='product']//tr[td[2][text()='Engineer']]/td[1]"
    IFRAME_LOCATOR = "//iframe[@id='courses-iframe']"
    LIST_ITEMS_LOCATOR = "//div[@class='row clearfix']//ul[@class='list-style-two']/li"
    HIGHLIGHTED_TEXT_LOCATOR = "//div[@class='row clearfix']//li[contains(text(), 'mentorship program')]"
    ITEM_LOCATOR = "//div[@class='row clearfix']//ul[@class='list-style-two']/li[position() = 8]"

class CssLocators:
    #CSS Locators
    OPEN_TAB_BUTTON = "a#opentab"
    ALERT_INPUT = "input#name.inputs"
    ALERT_BUTTON = "input#alertbtn.btn-style"
    CONFIRM_BUTTON = "input#confirmbtn.btn-style"