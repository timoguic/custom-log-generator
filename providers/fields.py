from abc import abstractmethod
from importlib import import_module
from string import Template


class BaseField:
    """Abstract base class - all fields must defined the render() method"""

    @abstractmethod
    def render(self, *args, **kwargs):
        pass


class Pattern(BaseField):
    """Creates and renders a pattern using $-vars"""

    def __init__(self, pattern=None, fields=None, **kwargs):
        self.pattern = Template(pattern)
        # A pattern contains fields
        self.fields = {key: make_field(**data) for key, data in fields.items()}

    def render(self, user=None, time=None):
        """Renders the pattern"""
        mapping = {}
        for name, field in self.fields.items():
            if type(field) == UserField:
                mapping[name] = field.render(user=user)
            elif type(field) == TimeField:
                mapping[name] = field.render(time=time)
            else:
                mapping[name] = field.render()

        return self.pattern.substitute(mapping)

    def __str__(self):
        return f"<Pattern: '{self.pattern.template}'>"


class TimeField(BaseField):
    """Timestamp field - renders with the given format"""

    def __init__(self, format):
        self.format = format

    def render(self, time, **kwargs):
        return time.strftime(self.format)


class UserField(BaseField):
    """User field - renders the given attribute"""

    def __init__(self, attribute=None):
        self.attribute = attribute

    def render(self, user, **kwargs):
        return getattr(user, self.attribute, "ATTR NOT FOUND")


class Field:
    """Generic field. It can either:
    - dynamically imports and gets function to generate the field value
    - render static data
    """

    def __init__(self, func=None, data=None, **kwargs):
        self.data = data
        self.kwargs = kwargs

        if callable(func):
            # Plain function that can be called
            self.func = func
        elif type(func) is str:
            # Dotted path
            if "." in func:
                module, function = func.rsplit(".", 1)
                mod = import_module(module)
            else:
                # if no specific path, look for it in the generators package
                mod = import_module("..generators", ".")
                function = func

            self.func = getattr(mod, function)

    def render(self):
        if self.data:
            # Static data
            return self.data

        return self.func(**self.kwargs)


def make_field(**data):
    """Factory method to create the relevant field instance based on the provider"""
    provider = data.get("provider")
    if provider == "user":
        return UserField(data["attribute"])
    elif provider == "timestamp":
        return TimeField(data["format"])
    elif provider == "template":
        return Pattern(data["pattern"], data["fields"])
    elif provider == "static":
        return Field(data=data["data"])
    elif provider is not None:
        raise RuntimeError(f"Unknown provider {provider}!")

    return Field(**data)
