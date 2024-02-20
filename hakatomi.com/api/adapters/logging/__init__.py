import datetime


def log(action, actor, asset, outcome, **kwargs):
    event = (
        f"{datetime.datetime.now()} {action:>10} {actor:>10} {asset:>10} {outcome:>10} {','.join(f'{k}={v}' for k, v in kwargs.items())}"
    )
    print(event)
