Zählrohr communication protocol
===============================

General infos
-------------
* All messages are plain ASCII and \n terminated 
* Acknowledgments have a 50ms timeout
* Capsule transmissions will be repeated until acked by the bone
* Timestamps are normal unix timestamps (seconds since the epoch)
* Speed is measured in m/s

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
kaboard: 	Capsule	<tube number> <"OneToTwo"/"TwoToOne"> <timestamp> <speed> 
bone:		Capsule ack
```

* The "OneToTwo"/"TwoToOne" indicates the direction, from sensor one to sensor two or the other way.

