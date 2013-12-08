Zählrohr
=========

TLDR;
-----
Zaehlrohr is a simple approach to measure the performance 
of project seidenstrasse (see http://events.ccc.de/congress/2013/wiki/Projects:Seidenstrasse).

Its aim is to count the capsules which are being send to and from a switching node.
This is done by attaching two light barriers to each tube
connecting the switching node with its neighbors.
As a by-product this setup also provides the possibility to calculate speed of each capsule.
All measurements will be aggregated to a node status website.

Technical details
-----------------
The capsule detection is done by two super bright leds and two photo resistors
attached to the outside of a tube.
Drilling holes into the tube is not necessary since it is just transparent enough.

The signals of the photo resistors will be preprocessed by a simple operational amplifier circuit.
First a capacitor is used to filter out any DC-offset on the signal caused by ambient light.
After that the signal may still contain noise,
like the 50Hz sine produced by fluorescent light tubes.
Therefore a comparator is used to filter out this noise floor below a configurable threshold voltage.
It also amplifies anything above the threshold to 5v, leaving us with a AVR friendly 0v to 5v signal.
The passing capsule will usually decrease the voltage coming from the photo resistor about 1v.
Therefore the threshold should be chose between 0,2v and 1,2v.

The output of each comparator circuit is directly attached to the digital IO-Pins of a AVR based
micro controller board (e.g. a Kaboard).
The board calculates direction and speed of each capsule and sends the data to a beagle bone using a 
simple usb uart bridge.
The datasets will be saved in database for easier aggregation, by a javascript running under nodejs.
The aggregated data (capsules per time, total numbers of capsules, minimum, maximum and average speed ...),
will be accessible via HTTP as json data.
There will also be website that displays the data as nice graphs using chart.js.
In case the beaglebone has not enough power to serve all requests,
an additional webservers can be used as reverse proxies.

 
