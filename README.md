Zaehlrohr
=========

TLDR;
-----
Zaehlrohr is a simple approach to measure the performance 
of project seidenstrasse (see http://events.ccc.de/congress/2013/wiki/Projects:Seidenstrasse).

Its aim is to count the capsules which are being send to and from a switching node.
This is done by attaching two light barriers to each tube
connecting the switching node with its neighbors.
As a by-product this setup also provides the possibility to calculate speed of each capsule.
All measurements will be aggregated to node status website.

Technical details
-----------------
The capsule detection is done by two super bright leds and two photo resistors
attached to the outside of a tube.
Drilling holes into the tube is not necessary since the is just transparent enough.

The signals of the photo resistors will be preprocessed by a simple operational amplifier circuit.
First a capacitor is used to filter out any DC-offset on the signal caused by ambient light.
After that the signal may still contain noise,
like the 50Hz sine produced by fluorescent light tubes.
Therefore a comparator is used to filter out this noise floor below a configurable threshold voltage.
It also amplifies anything above the threshold to 5v, leaving us with a AVR friendly 0v or 5v signal.
The passing capsule will usually decrease the voltage coming from the photo resistor about 1v.
Therefore the threshold should be chose between 0,2v and 5v.

The output of each comparator circuit is directly attached to the digital IO-Pins of a AVR based
micro controller board (e.g. a Kaboard).
The board calculates direction and speed of each capsule and sends the data to a beagle bone using a 
simple usb uart bridge.
The datasets will be saved in database for easier aggregation.
A cronjob will then be used to provide aggregated data (capsules per time, 
minimum, maximum and average speed) as an html file.
There will also be a json file containing raw datasets for each capsule for anyone who wants to provide
an alternative frontend.
The files will then be uploaded to a web server from which the can be accessed by the rest of the universe.
 