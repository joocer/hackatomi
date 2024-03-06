import datetime
from adapters.logging.rolling_log import RollingLog

logfile = RollingLog("hakatomi.txt")

def log(action, actor, outcome, **kwargs):
    event = f"{datetime.datetime.now()} {action:>10} {actor:>10} {outcome:>10} {','.join(f'{k}={v}' for k, v in kwargs.items())}"
    logfile.append(event)
    print(event)
