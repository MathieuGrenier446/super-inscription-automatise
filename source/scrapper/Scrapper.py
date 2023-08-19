import itertools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from source.classes import Course, Credentials, InvalidClassException
from source.scrapper.handlers.PopUpHandler import PopUpHandler
from source.scrapper.pages.LoginPage import LoginPage
from source.scrapper.pages.CoursePage import CoursePage
from source.scrapper.pages.MainPage import MainPage


class Scrapper:

    def __init__(self):
        self.pop_up_handler = PopUpHandler()

    def main(self, courses: list[Course], credentials: Credentials):
        """
        Main function for the Scrapper class.
        """
        print("Starting scrapper...")

        self.open_website("https://dossieretudiant.polymtl.ca/WebEtudiant7/")
        
        self.login(credentials.username, credentials.password, credentials.date_of_birth)

        self.navigate_to_courses()
        
        existing_courses = self.get_existing_courses()

        courses_to_modify = [course for course in courses if course in existing_courses]

        print(courses_to_modify)

        self.add_course("LOG1000", "1", "1")
        # self.modify_courses(courses_to_modify)

        # courses_left = [course for course in courses if course not in existing_courses]

        # self.add_courses(courses_left)

        # # Close the browser
        # self.driver.close()

    def open_website(self, url: str):
        print("Opening website...")
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def navigate_to_courses(self):
        print("Navigating to courses...")
        main_page = MainPage(self.driver)
        main_page.navigate_to_courses()

    def login(self, username: str, password: str, date_of_birth: str):
        print("Logging in...")

        login_page = LoginPage(self.driver)
        login_page.login(username, password, date_of_birth)
     

    def get_existing_courses(self) -> list[Course]:
        print("Getting courses...")
        course_page = CoursePage(self.driver)

        return course_page.get_courses()
    
    def add_courses(self, courses: list[Course]):
        print("Adding all courses...")
        for course in courses:
            self.add_course(course.sigle, course.grtheo, course.grlab)

    def modify_courses(self, courses: list[Course]):
        print("Modifying all courses...")
        for course in courses:
            self.modify_course(course.sigle, course.grtheo, course.grlab)

    def modify_course(self, course_sigle: str, new_grtheo: int,  new_grlab: int):
        
        print("Modifying course...")

        # Find the input fields for the course
        rows = self.driver.find_elements_by_css_selector(".tableListeCoursActuels")
        target_row = None

        for row in rows:
            sigle_field = None
            for input_field in row.find_elements_by_css_selector("input[name^='sigle']"):
                if input_field.get_attribute("value") == course_sigle:
                    sigle_field = input_field
                    break
            if sigle_field is not None:
                target_row = row
                break

        if target_row is None:
            print("No course found with the provided sigle.")
            return

        grtheo_field = target_row.find_element_by_name("input[name^='grtheo']")
        grlab_field = target_row.find_element_by_name("input[name^='grlab']")

        # Clear the existing values
        grtheo_field.clear()
        grlab_field.clear()

        # Input the new course details
        grtheo_field.send_keys(new_grtheo)
        self.pop_up_handler.resolve_all_alerts()
        grlab_field.send_keys(new_grlab)
        self.handle_pop_up()

    def add_course(self, course_sigle: str, course_grtheo: int, course_grlab: int):
        print("Adding course...")

        course_page = CoursePage(self.driver)

        course_page.add_course(course_sigle, course_grtheo, course_grlab)

        # # Find the input fields for the new course
        # rows = self.driver.find_elements_by_css_selector(".tableListeCoursActuels")
        # next_row = None

        # for row in rows:
        #     sigle_field = None
        #     for input_field in row.find_elements_by_css_selector("input[name^='sigle']"):
        #         if input_field.get_attribute("value") == "":
        #             sigle_field = input_field
        #             break
        #     if sigle_field is not None:
        #         next_row = row
        #         break

        # if next_row is None:
        #     print("No available row found for adding a new course.")
        #     return

        # grtheo_field = next_row.find_element_by_name("input[name^='grtheo']")
        # grlab_field = next_row.find_element_by_name("input[name^='grlab']")

        # # Input the course details
        # sigle_field.send_keys(course_sigle)
        # self.handle_pop_up()
        # grtheo_field.send_keys(course_grtheo)
        # self.handle_pop_up()
        # grlab_field.send_keys(course_grlab)
        # self.handle_pop_up()


    def cancel(self):
        print("Cancelling...")

    def handle_pop_up(self):
        print("Handling alerts...")

        try:
            # Wait for the alert to be present
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.alert_is_present())

            # Switch to the alert
            alert = self.driver.switch_to.alert

            # Get the alert text
            alert_text = alert.text
            print(f"Alert text: {alert_text}")

            # Accept the alert
            alert.accept()

            # Switch back to the default content
            self.driver.switch_to.default_content()

        except EC.TimeoutException:
            print("No alert found")

        # Continue with other actions on the webpage


    