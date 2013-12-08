var serialport = require('serialport')

var initialTimer;

var serialPort = new serialport.SerialPort('/tmp/ttyTest1', {
  'baudrate' : 38400,
  'databits' : 8,
  'stopbits' : 1,
  'parity' : 'none',
  'parser': serialport.parsers.readline('\n')
});

function getSencondsTimestamp() {
	var milliseconds =new Date().getTime();
	return Math.round(milliseconds / 1000);
}

var startTimestamp = 0;

function onData(data) {
	console.log('data received: ' + data);
	var timestamp = parseInt(data.substr(11,10));
	var seconds = getSencondsTimestamp();
	console.log('difference: ' + (timestamp - seconds) + ' over ' + (seconds - startTimestamp));


	clearInterval(initialTimer);
}

function setTime() {
	startTimestamp = getSencondsTimestamp();
	console.log('Setting inital Time: ' + startTimestamp);
	serialPort.write(startTimestamp + '\n');
}

function onOpen() {
	console.log('Port is open');
	serialPort.on('data',onData);
	initialTimer = setInterval(setTime,100);
}

serialPort.on('open', onOpen);

