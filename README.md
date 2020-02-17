# PyLight (Java, Python)
PyLight is a suite to improve responsiveness of YeeLight bulbs, using:
a local Raspberry Pi running an API, LAN mode (enables API support for YeeLight) and an Android app.

I intend to significantly cut down on delays of actions, and automate lights via cron jobs.

API currently supports GET requests only. Adding PUT support for direct control soon
API domain to be changed to my personal domain
Uses Localhost currently, for ease of prototyping

# WHY?
Whilst the YeeLight app is "functional", the app exhibits delays of up to 5 seconds, possibly due to server overload and ping (singapore based server). Unsure of other firmware issues causing delay, however I intend to diagnose these in future. The python proof of concept has been observed to be far more responsive. Also fun.

# WHO?
Deployment is initially intended for myself and friends, as networking is hardcoded (ugh I'm so sorry). In future I hope to have a stable, deployable release.

# WHEN?
God, who knows, honestly. Have you seen my commit history?

# WHERE?
Network connectivity required, control of local network currently necessary
