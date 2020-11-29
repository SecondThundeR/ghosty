'use strict';
const sharedVars = require('../data/variables');
const localBuffer = new Buffer.from(sharedVars.text.helpMessageBase64, 'base64');
const decodedText = localBuffer.toString('utf-8');

function helpMessage(msg) {
	msg.delete({ timeout: 30000 });
	msg.channel.send(decodedText)
		.then(msg => {
			msg.delete({ timeout: 30000 });
		});
	return;
}

module.exports = {
	name: 'help',
	description: 'Returns all commands of bot',
	cooldown: 15,
	execute(msg) {
		helpMessage(msg);
	},
};
