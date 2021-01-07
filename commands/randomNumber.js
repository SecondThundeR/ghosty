'use strict';
const sharedVars = require('../data/variables');
const delayTime = 15000;

function randomNumber(msg, args) {
	let rangeNumber, randomNumberSingle, fromRangeNumber, toRangeNumber, randomNumberRange;
	if (args.length > 0 && isNaN(Number(args[0])) === true) {
		msg.delete({ timeout: delayTime });
		msg.reply(sharedVars.text.wrongArgumentWarning)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
	else {
		switch (args.length) {
		case 0:
			msg.delete({ timeout: delayTime });
			msg.reply(sharedVars.text.noRangeWarning)
				.then(msg => {
					msg.delete({ timeout: delayTime });
				});
			break;
		case 1:
			rangeNumber = Number(args[0]);
			if (rangeNumber < 1) {
				msg.reply(`${sharedVars.text.wrongSingleRangeNumberWarning}${rangeNumber}`);
				break;
			}
			else if (rangeNumber === 1) {
				msg.reply(sharedVars.text.equalSingleRangeNumberWarning);
				break;
			}
			else {
				randomNumberSingle = Math.floor(Math.random() * rangeNumber) + 1;
				msg.channel.send(`${sharedVars.text.randomNumberText} ${rangeNumber}: **${randomNumberSingle}**`);
				break;
			}
		case 2:
			fromRangeNumber = Number(args[0]);
			toRangeNumber = Number(args[1]);
			if (fromRangeNumber > toRangeNumber) {
				msg.reply(`${sharedVars.text.wrongRangeNumberWarning1}${fromRangeNumber}${sharedVars.text.wrongRangeNumberWarning2}${toRangeNumber}`);
				break;
			}
			else if (fromRangeNumber === toRangeNumber) {
				msg.reply(`${sharedVars.text.equalRangeNumberWarning1}${fromRangeNumber}${sharedVars.text.equalRangeNumberWarning2}${toRangeNumber}${sharedVars.text.equalRangeNumberWarning3}`);
				break;
			}
			else {
				randomNumberRange = Math.round(Math.random() * (toRangeNumber - fromRangeNumber) + fromRangeNumber);
				msg.channel.send(`${sharedVars.text.randomNumberWithRangeTextPart1} ${fromRangeNumber} ${sharedVars.text.randomNumberWithRangeTextPart2} ${toRangeNumber}: **${randomNumberRange}**`);
				break;
			}
		default:
			break;
		}
	}
}

module.exports = {
	name: 'randomNumber',
	description: 'Module returns a random number (with/without custom range)',
	execute(msg, args) {
		randomNumber(msg, args);
	},
};
