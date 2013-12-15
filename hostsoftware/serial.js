var serialport = require('serialport')

var syncRetryTimer;

var serialPort = new serialport.SerialPort('/dev/kaboard', {
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

	if(data == "Sync ack") {
		clearInterval(syncRetryTimer);
	}

	var timestamp = parseInt(data.substr(11,10));
	var seconds = getSencondsTimestamp();
	console.log('difference: ' + (timestamp - seconds) + ' over ' + (seconds - startTimestamp));
}

function syncTime() {
	startTimestamp = getSencondsTimestamp();
	console.log('Syncing Time: ' + startTimestamp);
	serialPort.write('Set ' + startTimestamp + '\n');
}

function onOpen() {
	console.log('Port is open');
	serialPort.on('data',onData);
	syncRetryTimer = setInterval(syncTime,100);
}

serialPort.on('open', onOpen);

