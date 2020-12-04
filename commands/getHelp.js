'use strict';
const sharedVars = require('../data/variables');
const rawText = new Buffer.from(sharedVars.text.helpMessageBase64, 'base64');
const decodedText = rawText.toString('utf-8');
const delayTime = 20000;

function sendHelpMessage(msg) {
	msg.delete({ timeout: delayTime });
	msg.channel.send(decodedText)
		.then(msg => {
			msg.delete({ timeout: delayTime });
		});
	return;
}

module.exports = {
	name: 'getHelp',
	description: 'Module returns all commands of bot',
	cooldown: 10,
	execute(msg) {
		sendHelpMessage(msg);
	},
};
