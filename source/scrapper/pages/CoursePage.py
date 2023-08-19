from selenium.webdriver.remote.webelement import WebElement
from source.scrapper.handlers.PageFactory import PageFactory
from source.classes.Course import Course

class CourseInput:
    def __init__(self, sigle: WebElement, grtheo: WebElement, grlab: WebElement) -> None:
        self.sigle = sigle
        self.grtheo = grtheo
        self.grlab = grlab

    def __repr__(self) -> str:
        return f"{self.sigle.get_text()} {self.grtheo.get_text()} {self.grlab.get_text()}"
        

class CoursePage(PageFactory):
    def __init__(self,driver):
        self.locators = {}
        for i in range(1,11):
            self.locators[f"sigle{i}"] = ('NAME', f"sigle{i}")
            self.locators[f"grtheo{i}"] = ('NAME', f"grtheo{i}")
            self.locators[f"grlab{i}"] = ('NAME', f"grlab{i}")
        
        super().__init__(driver)

        self.courses = []
        for i in range(1,11):
            self.courses.append(CourseInput(getattr(self, f"sigle{i}"), 
                                            getattr(self, f"grtheo{i}"), 
                                            getattr(self, f"grlab{i}")))
        

    def get_courses(self) -> list[Course]:
        courses = []
        for course in self.courses:
            if course.sigle.getAttribute("value") != "":
                courses.append(Course(course.sigle.getAttribute("value"), 
                                      course.grtheo.getAttribute("value"), 
                                      course.grlab.getAttribute("value")))
        return courses
    
    def add_course(self, sigle: str, grtheo: str, grlab: str):
        for course in self.courses:
            if course.sigle.getAttribute("value") == "":
                course.sigle.set_text(sigle)
                course.grtheo.set_text(grtheo)
                course.grlab.set_text(grlab)
                break