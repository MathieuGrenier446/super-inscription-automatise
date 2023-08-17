from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from source.classes import Course, Credentials, InvalidClassException

class Scrapper:

    def main(self, courses: list[Course], credentials: Credentials):
        """
        Main function for the Scrapper class.
        """
        print("Starting scrapper...")

        self.open_website("https://dossieretudiant.polymtl.ca/WebEtudiant7/")
        
        self.login(credentials.username, credentials.password, credentials.date_of_birth)

        self.navigate_to_courses()

        existing_courses = self.get_existing_courses()

        self.modify_courses(existing_courses)

        courses_left = [course for course in courses if course not in existing_courses]

        self.add_courses(courses_left)

        # Close the browser
        self.driver.close()

    def open_website(self, url: str):
        print("Opening website...")
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def navigate_to_courses(self):
        print("Navigating to courses...")
        # Find the button for getting courses
        get_courses_button = self.driver.find_element_by_name("btnModif")

        # Click the button
        get_courses_button.click()

    def login(self, username: str, password: str, date_of_birth: str):
        print("Logging in...")
        # Find the input fields
        username_field = self.driver.find_element_by_name("code")
        password_field = self.driver.find_element_by_name("nip")
        dob_field = self.driver.find_element_by_name("naissance")

        # Input the user credentials and date of birth
        username_field.send_keys(username)
        password_field.send_keys(password)
        dob_field.send_keys(date_of_birth)

        # Submit the form
        password_field.send_keys(Keys.RETURN)

    def get_existing_courses(self) -> list[Course]:
        print("Getting courses...")
        course_elements = self.driver.find_elements_by_xpath('//input[starts-with(@name, "sigle")]')
        group_elements_theo = self.driver.find_elements_by_xpath('//input[starts-with(@name, "grtheo")]')
        group_elements_lab = self.driver.find_elements_by_xpath('//input[starts-with(@name, "grlab")]')

        # Initialize list to hold course info
        courses = []

        # Assume each course has associated group data and lengths of lists are same
        for i in range(len(course_elements)):
            # Check course code not empty
            course_code = course_elements[i].get_attribute('value')
            if course_code:
                # Check group code not empty
                group_code_theo = group_elements_theo[i].get_attribute('value')
                group_code_lab = group_elements_lab[i].get_attribute('value')
                if group_code_theo and group_code_lab:
                    # Add course to list
                    courses.append(Course(course_code, group_code_theo, group_code_lab))

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
        self.handle_pop_up()
        grlab_field.send_keys(new_grlab)
        self.handle_pop_up()

    def add_course(self, course_sigle: str, course_grtheo: int, course_grlab: int):
        print("Adding course...")

        # Find the input fields for the new course
        rows = self.driver.find_elements_by_css_selector(".tableListeCoursActuels")
        next_row = None

        for row in rows:
            sigle_field = None
            for input_field in row.find_elements_by_css_selector("input[name^='sigle']"):
                if input_field.get_attribute("value") == "":
                    sigle_field = input_field
                    break
            if sigle_field is not None:
                next_row = row
                break

        if next_row is None:
            print("No available row found for adding a new course.")
            return

        grtheo_field = next_row.find_element_by_name("input[name^='grtheo']")
        grlab_field = next_row.find_element_by_name("input[name^='grlab']")

        # Input the course details
        sigle_field.send_keys(course_sigle)
        self.handle_pop_up()
        grtheo_field.send_keys(course_grtheo)
        self.handle_pop_up()
        grlab_field.send_keys(course_grlab)
        self.handle_pop_up()


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

            raise InvalidClassException(alert_text)

        except EC.TimeoutException:
            print("No alert found")

        # Continue with other actions on the webpage


    