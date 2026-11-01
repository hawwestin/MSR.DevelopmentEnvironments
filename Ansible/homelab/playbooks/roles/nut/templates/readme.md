# NUT Role Templates

The role configures a NUT server on the UPS-connected host and NUT clients on other hosts. The role currently targets `malina` as the server and `proxmox` as clients.

## Files Deployed

| File | Server | Clients | Purpose |
| --- | --- | --- | --- |
| `nut.conf.j2` | Yes | Yes | Sets NUT mode to `netserver` or `netclient`. |
| `upsmon.conf.j2` | Yes | Yes | Defines the UPS monitor account, role, shutdown command, and event notifications. |
| `upssched.conf.j2` | Yes | Yes | Maps UPS events to timers and callback commands. |
| `upssched-cmd` | Yes | Yes | Handles scheduled events and checks UPS status, runtime, and load. It is rendered as a template so thresholds come from role defaults. |
| `ups.conf.j2` | Yes | No | Configures the physical UPS driver and the QNAP compatibility dummy UPS. |
| `upsd.conf.j2` | Yes | No | Listens on localhost and the configured server address and port. |
| `upsd.users.j2` | Yes | No | Defines the UPS monitor, administrator, and QNAP compatibility accounts. |

The role installs server packages on the server and client packages on clients. It sets deployed configuration files to root ownership and the `nut` group.

## Current Event Behavior

`upsmon.conf.j2` configures the monitor to report events to `upssched`. The server is assigned the primary monitor role; clients use the secondary role. `MONITOR` power value and `MINSUPPLIES` are separate settings.

`upssched.conf.j2` starts an `onbatt` timer when the UPS reports `ONBATT`; `ONLINE` cancels that timer. When the timer expires, the callback logs the event. `LOWBATT`, communication events, and `SHUTDOWN` are sent directly to the callback.

The callback logs `LOWBATT` and checks on-battery status, runtime, and load, but does not request forced shutdown for that event. For `SHUTDOWN`, it requests NUT forced shutdown only when the UPS is on battery, runtime is below the configured limit, and load is at or above the configured limit.

## Current Service State

The role explicitly stops and disables `nut-monitor` on managed hosts. It does not later start or enable that service, so monitor event processing is currently inactive even though its configuration files are deployed.

On the server, the role enables and starts `nut-server`, and starts `nut-driver-enumerator` if its unit is present. On clients, any existing local `nut-server` and `nut-driver-enumerator` services are stopped and disabled.

`nut_test_mode` defaults to `false`. When enabled, the generated monitor configuration has `MONITOR` power value `0` and a logger-only `SHUTDOWNCMD`; the callback logs to syslog and `wall` and suppresses the FSD request. Scheduler test events use separate runtime files and a five-second timer. The service remains stopped and disabled.

Do not enable `nut-monitor` or rely on its production shutdown behavior until the Proxmox HA and Ceph shutdown sequence is designed, reviewed, and explicitly approved.

## Credentials

The templates expect `vault_nut_monitor_password`, `vault_nut_admin_password`, and `vault_nut_qnap_admin_password`.



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