String.prototype.toHHMMSS = function () {
  var sec_num = parseInt(this, 10);
  var hours   = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours < 10) {
    hours = "0" + hours;
  }
  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  if (seconds < 10) {
    seconds = "0" + seconds;
  }
  let time = hours + ':' + minutes + ':' + seconds;
  return time;
}

function uptimeBot(msg) {
	var time = process.uptime();
  var uptime = (time + "").toHHMMSS();
  msg.channel.send(`Я не спал уже на протяжении ${uptime}.\n\nдайте поспать :(`);
}

module.exports = {
	name: 'uptime',
	description: 'Get uptime of bot',
	execute(msg) {
		uptimeBot(msg);
	},
};
