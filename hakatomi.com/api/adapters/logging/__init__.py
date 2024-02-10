import datetime


def log(action, actor, asset, **kwargs):
    event = f"{datetime.datetime.now()} - {action:>10} - {actor:>10} - {asset:>10} - {kwargs.items()}"
    print(event)
