from source.scrapper.handlers.PopUpHandler import resolve_all_alerts

class ElementGuard:
    def __init__(self, element):
        self._element = element

    def __getattr__(self, item):
        attr = getattr(self._element, item)

        if callable(attr):
            def wrapper(*args, **kwargs):
                # Add any needed behaviour modification here
                resolve_all_alerts()
                return attr(*args, **kwargs)
            return wrapper

        return attr

def guard(element):
    return ElementGuard(element)