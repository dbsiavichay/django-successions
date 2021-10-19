from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

FIXTURES = {
    "%year%": lambda: datetime.now().year,
    "%month%": lambda: datetime.now().month,
    "%day%": lambda: datetime.now().day,
}


class Succession(models.Model):
    """
    Model to define successions
    The succession allows to define alphanumeric sequences for the models
    """

    # The name will be build by app_labe, model_name and name of field Ex: todo_task_code
    name = models.CharField(unique=True, max_length=128, editable=False)
    prefix = models.CharField(max_length=64, default="")
    suffix = models.CharField(max_length=64, default="")
    padding = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=10),
        ],
        verbose_name=_("numeric padding"),
        help_text=_(
            "total size of the numeric part, will be add zeros to the left for complete this value"
        ),
    )
    increment = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(limit_value=1),
        ],
        verbose_name=_("numeric increment"),
        help_text=_("value of the increment in the following succession"),
    )
    current_value = models.PositiveIntegerField(
        null=True, verbose_name=_("current value")
    )

    def __str__(self):
        return "{}%number%{}".format(self.prefix, self.suffix)

    def get_next_value(self):
        self.current_value = (
            self.current_value + self.increment
            if self.current_value
            else self.increment
        )
        fixtures = {
            **FIXTURES,
            "%number%": lambda: str(self.current_value).zfill(self.padding),
        }
        value = str(self)
        for replace, func in fixtures.items():
            value = value.replace(replace, str(func()))
        return value
