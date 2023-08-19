from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

class PopUpHandler:

    def _is_alert_present(self, driver, timeout):
        '''Check if an alert is present'''
        try:
            alert = WebDriverWait(driver, timeout).until(expected_conditions.alert_is_present())
            if alert:
                return True
            else:
                raise TimeoutException
        except TimeoutException:
            # log the exception;
            return False

    def _resolve_alert(self, driver, accept):
        '''Accept or dismiss an alert'''
        if accept:
            driver.switch_to.alert.accept()
        else:
            driver.switch_to.alert.dismiss()

def resolve_all_alerts(self):
    '''Resolve all alerts'''
    handler = PopUpHandler()
    timeout = 5
    accept = True
    while handler.is_alert_present(self.driver, timeout):
        handler.resolve_alert(self.driver, accept)