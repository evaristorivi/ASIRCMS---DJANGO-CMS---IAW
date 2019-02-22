from django.dispatch import receiver
from .signals import example_signal


@receiver(example_signal)
def example_signal_handler(sender, **kwargs):
    print kwargs['arg1']
    print kwargs['arg2']
