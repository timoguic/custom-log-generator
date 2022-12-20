from .fields import Pattern
from .timestamp import TimeProvider
from .user import UserProvider


class LogProvider:
    """Main class controlling log generation and field/attributes mapping"""

    def __init__(self, conf):
        """Creates providers as necessary, loads the pattern and calculate log count"""
        self.config = conf
        self.user_provider = UserProvider(**conf["users"])
        self.time_provider = TimeProvider(**conf["timestamps"])

        self.pattern = Pattern(conf["pattern"], conf["fields"])

        self.nb_lines = 0
        self.count = conf.get("log_entries")
        if self.count is None:
            size = conf["log_size"]
            self.count = size // len(self.pattern.pattern.template) + 1

    @property
    def done(self):
        """Returns True when the required log size has been reached"""
        return self.nb_lines >= self.count

    def generate(self):
        """Generate a single log line"""
        current_user = self.user_provider.random_user
        current_time = self.time_provider.timestamp
        out = self.pattern.render(user=current_user, time=current_time)
        self.nb_lines += 1
        return out
