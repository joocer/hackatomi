# hakatomi

**overview**

You are John, protecting hakatomi.com from a cyber attack from Hans.

hakatomi.com exists as a simple website, but we see hakatomi.com as only its audit logs and some basic charts.

**Charts**
- successful log-ins per second
- failed log-ins per second
- network ingress and egress
- log head

**Actors**

Our users are implemented as a bot that sends traffic to hakatomi.com, we see their actions, such as failed and successful logins and actions on the system, in the logs. Users are basic in their actions.

Hans is implemented as another bot, he sends malicious traffic to hakatomi.com, we can also see his actions in the logs, as well as the impact it has on legitimate users.

**Goal**

Hans is trying to extort money from us, he wins when all of the users are locked out or he completes a data breach.
