class Locators:
    #XPath Locators
    SUGGESTION_CLASS_EXAMPLE_INPUT = "//legend[text()='Suggession Class Example']/..//input[@id='autocomplete']"
    SUGGESTION_COUNTRY = "//li[@class='ui-menu-item']//div[text()='Mexico']"
    DROPDOWN = "//select"  
    DROPDOWN_OPTION = "//select/option[position()={}]"  
    OPEN_WINDOW_BUTTON = "//button[@id='openwindow']"

class CSS_Locators:
    #CSS Locators
    OPEN_TAB_BUTTON = "a#opentab[class^='btn-']"