from source.scrapper.handlers.PageFactory import PageFactory

class LoginPage(PageFactory):
    def __init__(self,driver):
        self.locators = {
            "user": ('NAME', 'code'),
            "pwd": ('NAME', 'nip'),
            "dob": ('NAME', 'naissance'),
            "btnLogin": ('XPATH', '/html/body/div[2]/div[2]/form/div[4]/input')
        }
        super().__init__(driver)

    def login(self, username: str, password: str, date_of_birth: str):
        self.user.set_text(username)
        self.pwd.set_text(password)
        self.dob.set_text(date_of_birth)
        self.btnLogin.click_button()