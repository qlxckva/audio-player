from abc import ABC, abstractmethod
from datetime import datetime
import os

from config import AUDIO_EXT, TIME_FORMAT


class Entity(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def get_info(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._name == other._name

    def __lt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._name.lower() < other._name.lower()

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return f"{type(self).__name__}({self._name!r})"

    def __str__(self):
        return self._name


class Track(Entity):
    def __init__(self, path):
        super().__init__(os.path.splitext(os.path.basename(path))[0])
        self._path = path
        self._play_count = 0

    @property
    def title(self):
        return self._name

    @title.setter
    def title(self, value):
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def play_count(self):
        return self._play_count

    @play_count.setter
    def play_count(self, value):
        self._play_count = max(0, value)

    @staticmethod
    def is_audio(path):
        return path.lower().endswith(AUDIO_EXT)

    def get_info(self):
        return f"{self.title} | {self.path} | plays: {self.play_count}"

    def __eq__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        return self.path == other.path

    def __lt__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        return self.title.lower() < other.title.lower()

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return f"Track({self.path!r}, plays={self.play_count})"


class Genre(Entity):
    NAMES = ["Rock", "Pop", "Jazz", "Classical", "Hip-Hop",
             "Electronic", "Metal", "Folk", "Blues", "Other"]

    def get_info(self):
        return f"Genre: {self.name}"

    @staticmethod
    def default_genres():
        return [Genre(name) for name in Genre.NAMES]

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(("genre", self.name))

    def __repr__(self):
        return f"Genre({self.name!r})"


class User(Entity):
    def __init__(self, login):
        super().__init__(login)
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._name

    @login.setter
    def login(self, value):
        self._name = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def get_info(self):
        return f"User {self.login}, entered {self.time_in.strftime(TIME_FORMAT)}"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.login == other.login

    def __hash__(self):
        return hash(("user", self.login))

    def __repr__(self):
        return f"User({self.login!r})"

    def __str__(self):
        return f"User: {self.login}"


class GenreMap:
    #  простая замена словарю жанр ищется в двух параллельных списках.
    def __init__(self):
        self._keys = []
        self._values = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, value):
        self._keys = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value

    def set(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return None

    def __len__(self):
        return len(self._keys)

    def __eq__(self, other):
        if not isinstance(other, GenreMap):
            return NotImplemented
        return self._keys == other._keys and self._values == other._values

    def __lt__(self, other):
        if not isinstance(other, GenreMap):
            return NotImplemented
        return self._keys < other._keys

    def __repr__(self):
        return f"GenreMap({len(self)} items)"

    def __str__(self):
        return f"GenreMap: {len(self)} items"


