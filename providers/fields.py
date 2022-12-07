from abc import abstractmethod
from importlib import import_module
from string import Template


class BaseField:
    @abstractmethod
    def render(self, *args, **kwargs):
        pass


class Pattern(BaseField):
    def __init__(self, pattern=None, fields=None, **kwargs):
        self.pattern = Template(pattern)
        self.fields = {key: make_field(**data) for key, data in fields.items()}

    def render(self, user=None, time=None):
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
    def __init__(self, format):
        self.format = format

    def render(self, time, **kwargs):
        return time.strftime(self.format)


class UserField(BaseField):
    def __init__(self, attribute=None):
        self.attribute = attribute

    def render(self, user, **kwargs):
        return getattr(user, self.attribute, "ATTR NOT FOUND")


class Field:
    def __init__(self, func=None, data=None, **kwargs):
        self.data = data
        self.kwargs = kwargs

        if callable(func):
            self.func = func
        elif type(func) is str:
            if "." in func:
                module, function = func.rsplit(".", 1)
                mod = import_module(module)
            else:
                mod = import_module("..generators", ".")
                function = func

            self.func = getattr(mod, function)

    def render(self):
        if self.data:
            return self.data

        return self.func(**self.kwargs)


def make_field(**data):
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
