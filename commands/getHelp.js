'use strict';
const sharedVars = require('../data/variables');
const delayTime = 20000;

function sendHelpMessage(msg) {
	msg.delete({ timeout: delayTime });
	msg.channel.send(sharedVars.text.helpMessage)
		.then(msg => {
			msg.delete({ timeout: delayTime });
		});
}

module.exports = {
	name: 'getHelp',
	description: 'Module returns all commands of bot',
	cooldown: 5,
	execute(msg) {
		sendHelpMessage(msg);
	},
};
