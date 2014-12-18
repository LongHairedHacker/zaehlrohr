Zählrohr communication protocol
===============================

General infos
-------------
* All messages are plain ASCII and \n terminated 
* Acknowledgments have a 100ms timeout
* Capsule transmissions will be repeated until acked by the bone
* Timestamps are normal unix timestamps (seconds since the epoch)
* passage time is the time needed by the capsule for 0.5m, the distance between the two sensors

Time synchronization 
----------------------------
```
bone:		Reset
kaboard:	Reset ack
```


Time synchronization 
----------------------------
```
bone:		Set <timestamp>
kaboard:	Sync ack
```

Measurements
------------
```
kaboard: 	Capsule	<tube number> <direction: "OneToTwo"/"TwoToOne"> <timestamp> <passage time> 
bone:		Capsule ack
```

* The "OneToTwo"/"TwoToOne" indicates the direction, from sensor one to sensor two or the other way.

