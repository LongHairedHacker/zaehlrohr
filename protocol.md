Zählrohr communication protocol
===============================

General infos
-------------
All messages are plain ASCII and \n terminated 
Acknowledgments have a 100ms timeout
Timestamps are normal unix timestamps (seconds since the epoch)
Speed is measured in m/s

Initial time synchronization 
----------------------------
```
bone:		set <timestamp>
kaboard:	ack
```

Measurements
------------
```
kaboard: 	capsule	<tube number> <"in"/"out"> <timestamp> <speed> 
bone:		ack
```