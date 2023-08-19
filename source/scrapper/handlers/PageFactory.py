from selenium import webdriver
from seleniumpagefactory.Pagefactory import PageFactory as BasePageFactory
from selenium.webdriver.remote.webelement import WebElement
from source.scrapper.handlers.ElementGuard import ElementGuard


class PageFactory(BasePageFactory):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        for attr_name, attr_value in self.__dict__.items():

            if isinstance(attr_value, WebElement):
                guarded_element = ElementGuard(attr_value)
                setattr(self, attr_name, guarded_element)