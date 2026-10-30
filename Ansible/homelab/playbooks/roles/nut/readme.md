Default messages upsmon.conf
```conf
# --------------------------------------------------------------------------
# NOTIFYMSG - change messages sent by upsmon when certain events occur
#
# You can change the default messages to something else if you like.
#
# NOTIFYMSG <notify type> "message"
#
# NOTIFYMSG ONLINE      "UPS %s on line power"
# NOTIFYMSG ONBATT      "UPS %s on battery"
# NOTIFYMSG LOWBATT     "UPS %s battery is low"
# NOTIFYMSG FSD         "UPS %s: forced shutdown in progress"
# NOTIFYMSG COMMOK      "Communications with UPS %s established"
# NOTIFYMSG COMMBAD     "Communications with UPS %s lost"
# NOTIFYMSG SHUTDOWN    "Auto logout and shutdown proceeding"
# NOTIFYMSG REPLBATT    "UPS %s battery needs to be replaced"
# NOTIFYMSG NOCOMM      "UPS %s is unavailable"
# NOTIFYMSG NOPARENT    "upsmon parent process died - shutdown impossible"
```

NOTIFYMSG Types

```conf
# Possible values for <notify type>:
#
# ONLINE   : UPS is back online
# ONBATT   : UPS is on battery
# LOWBATT  : UPS has a low battery (if also on battery, it's "critical")
# FSD      : UPS is being shutdown by the primary (FSD = "Forced Shutdown")
# COMMOK   : Communications established with the UPS
# COMMBAD  : Communications lost to the UPS
# SHUTDOWN : The system is being shutdown
# REPLBATT : The UPS battery is bad and needs to be replaced
# NOCOMM   : A UPS is unavailable (can't be contacted for monitoring)
# NOPARENT : The process that shuts down the system has died (shutdown impossible)
```