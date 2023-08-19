
from source.classes import Credentials
from source.scrapper.Scrapper import Scrapper

if __name__ == "__main__":
    scrapper = Scrapper()
    credentials = Credentials("", "", "")
    scrapper.main([], credentials)
