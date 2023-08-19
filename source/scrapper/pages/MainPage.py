from source.scrapper.handlers.PageFactory import PageFactory

class MainPage(PageFactory):
    def __init__(self,driver):
        self.locators = {
            "btnModifChoixCours": ('NAME', 'btnModif'),
        }
        super().__init__(driver)

    def navigate_to_courses(self):
        self.btnModifChoixCours.click_button()
