from .models import Succession


def save_with_succession_value(self, target, **kwargs):
    succession_value = getattr(self, target) if hasattr(self, target) else None
    if not succession_value:
        succession_value = generate_succesion_value(
            **self._meta.get_field(target).get_kwargs()
        )
        setattr(self, target, succession_value)
    super(self.__class__, self).save(**kwargs)


def generate_succesion_value(**kwargs):
    succession = Succession.objects.get_or_create(**kwargs)[0]
    succession_value = succession.get_next_value()
    succession.save()
    return succession_value
