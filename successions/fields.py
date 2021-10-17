from django.db import models
from django.core import checks
from functools import partialmethod
from .models import Succession
from .utils import save_with_succession_value


class SuccessionField(models.CharField):

    description = "Usefull for generate successions in a field"

    def __init__(
        self, prefix="", suffix="", padding=None, increment=1, *args, **kwargs
    ):
        kwargs["editable"] = False
        self.prefix = prefix
        self.suffix = suffix
        self.padding = padding
        self.increment = increment
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_prefix(),
            *self._check_suffix(),
            *self._check_padding(),
            *self._check_increment(),
        ]

    def _check_prefix(self):
        if not isinstance(self.prefix, str):
            return [checks.Error("'prefix' must be a str instance.", obj=self)]
        return []

    def _check_suffix(self):
        if not isinstance(self.suffix, str):
            return [checks.Error("'suffix' must be a str instance.", obj=self)]

        return []

    def _check_padding(self):
        if not isinstance(self.padding, int) or not 1 <= self.padding <= 10:
            return [
                checks.Error(
                    "'padding' must be a positive integer between 1 to 10.", obj=self
                )
            ]

        return []

    def _check_increment(self):
        if not isinstance(self.increment, int) or self.increment < 1:
            return [checks.Error("'increment' must be a positive integer.", obj=self)]

        return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.prefix:
            kwargs["prefix"] = self.prefix
        if self.suffix:
            kwargsk["suffix"] = self.suffix
        if self.padding:
            kwargs["padding"] = self.padding
        if self.increment != 1:
            kwargs["increment"] = self.increment
        return name, path, args, kwargs

    def get_kwargs(self):
        return {
            "name": self.succession_name,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "padding": self.padding,
            "increment": self.increment,
        }

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        meta = cls._meta
        self.succession_name = "{}_{}_{}".format(meta.app_label, meta.model_name, name)
        setattr(
            cls,
            "save",
            partialmethod(save_with_succession_value, name),
        )
