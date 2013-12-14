Zählrohr json api
=================
This document is a request for comments and may change.

Naming conventions
------------------
* Tubes vs. Streams: Tubes can be used in two directions.
  Therefore a tube virtually carries two streams of capsules.
  Computing more complex values like the total throughput of a switching node
  requires data for the streams and not just for the tubes.
  On the other hand for providing a quick overview on the overall performance,
  the data for the tubes might be a better choice.
  Therefore both representations are provided.

* Tube names: A tube is named after its endpoints.
  The name scheme looks like this "[end point 1]-[end point 2]".
  With the endpoint names sorted in alphabetical order.
  E.g. the Tube connecting C to A is names "A-C".

* Stream names: Streams are named after their endpoints as well.
  The name scheme is "[source endpoint]-[destination endpoint]".

Summary
-------
* Provides combined statistics for all tubes equipped with sensors
* URL: [server]/summary
```
{
	"StartTimestamp" : <timestamp of the first event in the database>,
	"EndTimestamp" : <timestamp of the last event in the database>,
	"Overall" : {
		"CapsuleCount" : <total number of all capsules counted in all tubes>,
		"CapsulesPerMinute" : <average number of capsules per minute for all tubes>,
		"MinCapsulesPerMinute" : <minimum number of capsules per minute for all tubes>,
		"MaxCapsulesPerMinute" : <maximum number of capsules per minute for all tubes>,
		"AverageCapsuleVelocity" : <average velocity of capsules for all tubes>,
		"MinCapsulesVelocity" : <minimum velocity of capsules for all tubes>,
		"MaxCapsulesVelocity" : <maximum velocity of capsules for all tubes>,
	},
	"Tubes" : {
		<Name that identifies this tube> : {
			"CapsuleCount" : <total number of all capsules counted in this tube>,
			"CapsulesPerMinute" : <average number of capsules per minute in this tube>,
			"MinCapsulesPerMinute" : <minimum number of capsules per minute in this tube>,
			"MaxCapsulesPerMinute" : <maximum number of capsules per minute in this tube>,
			"AverageCapsuleVelocity" : <average velocity of capsules for in this tube>,
			"MinCapsulesVelocity" : <minimum velocity of capsules for in this tube>,
			"MaxCapsulesVelocity" : <maximum velocity of capsules for in this tube>,
		},
		<Name that identifies this totally different tube> : {
			...
		},
		...
	},

	"Streams" : {
		<Name that identifies this stream> : {
			"CapsuleCount" : <total number of all capsules counted in this stream>,
			"CapsulesPerMinute" : <average number of capsules per minute in this stream>,
			"MinCapsulesPerMinute" : <minimum number of capsules per minute in this stream>,
			"MaxCapsulesPerMinute" : <maximum number of capsules per minute in this stream>,
			"AverageCapsuleVelocity" : <average velocity of capsules for in this stream>,
			"MinCapsulesVelocity" : <minimum velocity of capsules for in this stream>,
			"MaxCapsulesVelocity" : <maximum velocity of capsules for in this stream>,
		},
		<Name that identifies this totally different stream> : {
			...
		},
		...
	},
}
```

Interval values
---------------
* Provides values aggregated over intervals
* URL: [server]/[name]/[interval]/
* name: can be any valid tube or stream name
* interval: can be minute, hour, day

```
[
	{
		"time" : <timestamp at the start of the interval>,
		"CapsuleCount" : <total number of capsules counted until the end of this interval>,
		"CapsulesPerInterval" : <number of capsules counted during this interval>,
		"AverageCapsuleVelocity" : <average velocity of capsules for this interval>,
		"MinCapsulesVelocity" : <minimum velocity of capsules for this interval>,
		"MaxCapsulesVelocity" : <maximum velocity of capsules for this interval>,
	},
	{
		"time" : <timestamp at the start of the interval>,
		...
	},
	...
]
```

Raw events
----------
* Provides all raw samples in case you want to analyze the data yourself
* URL: [server]/raw

```
[
	{
		"time"  : <timestamp of the event>,
		"stream" : <stream name>,
		"speed" : <speed of the capsule>,
	},
]
```







