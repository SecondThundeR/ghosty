'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const randomWordsArray = JSONLib.getWordsArray();
const delayTime = 3000;

function getRandomWordFromArray(msg, args) {
	const randomWordFromArray = Math.floor(Math.random() * JSONLib.getWordsArray().length);
	const isSpamWarningTriggered = spamChecker(msg);

	switch(isSpamWarningTriggered) {
	case true:
		sharedVars.vars.spammerCount = 0;
		msg.delete({ timeout: delayTime });
		msg.reply(sharedVars.text.warningForSpam)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		switch (args.length) {
		case 0:
			msg.channel.send(`${msg.author} ${randomWordsArray[randomWordFromArray]}`);
			return;
		case 1:
			msg.channel.send(`${args[0]} ${randomWordsArray[randomWordFromArray]}`);
			return;
		default:
			return;
		}
	}
}

function spamChecker(msg) {
	switch (true) {
	case sharedVars.vars.spammerCount >= 3 && sharedVars.vars.spammerID === msg.author.id:
		return true;
	case sharedVars.vars.spammerCount < 3 && sharedVars.vars.spammerID === msg.author.id:
		sharedVars.vars.spammerCount++;
		return false;
	default:
		sharedVars.vars.spammerID = msg.author.id;
		sharedVars.vars.spammerCount = 1;
		return false;
	}
}

module.exports = {
	name: 'getRandomWordFromArray',
	description: 'Current module return a random word from JSON array (Also, module check for spam (3-4 messages in a row) and return a warning)',
	cooldown: 2,
	execute(msg, args) {
		getRandomWordFromArray(msg, args);
	},
};
