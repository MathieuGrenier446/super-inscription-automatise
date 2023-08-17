import json
from source.classes import Course, Credentials

def read_settings(settings_file_path: str) -> list[Course]:
    """
    Reads the settings from the settings.json file and returns a list of Course objects.
    """
    # Open the settings.json file and load the data
    with open(settings_file_path) as json_file:
        data = json.load(json_file)

    # Create a list of Course objects
    courses = []
    for course in data.get("courses"):
        courses.append(Course(course["sigle"], course["lab_groups"], course["theo_groups"]))

    raw_credentials = data.get("credentials")
    credentials = Credentials(raw_credentials["username"], raw_credentials["password"], raw_credentials["date_of_birth"])
    return courses