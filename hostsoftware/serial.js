var serialport = require('serialport')

var RetransmitTimer;

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

function sendWithRetrasmit(data) {
	RetransmitTimer = setInterval(function() {
		process.stdout.write("data send: " + data);
		serialPort.write(data);
	},100);
}

var startTimestamp = 0;

function onData(data) {
	console.log('data received: ' + data);
	
	if(data == "Reset ack") {
		clearInterval(RetransmitTimer);
		syncTime();
	}
	else if(data == "Sync ack") {
		clearInterval(RetransmitTimer);
	}
	else {
		parts = data.split(" ");
		if(parts[0] == "Capsule") {
			serialPort.write("Ack\n");

			tubenumber = parseInt(parts[1]);
			timestamp = parseInt(parts[2])
			date = new Date(timestamp * 1000)
			console.log("Capsule:")
			console.log("\tTube: " + tubenumber);
			console.log("\tTime: " + date);
			console.log("\tDirection: " + parts[3]);
			speed = 0.5 / (parseInt(parts[4]) / 1000.0) 
			console.log("\tSpeed: " + speed + " m/s");
		}


	}

}

function reset() {
	sendWithRetrasmit("Reset\n");
}

function syncTime() {
	startTimestamp = getSencondsTimestamp();
	console.log('Syncing Time: ' + startTimestamp);
	sendWithRetrasmit('Set ' + startTimestamp + '\n');
}

function onOpen() {
	console.log('Port is open');
	serialPort.on('data',onData);
	reset();
}

serialPort.on('open', onOpen);

