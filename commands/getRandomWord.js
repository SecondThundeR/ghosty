'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const randomWordsArray = JSONLib.getJSONWordArray();

function getRandomWord(msg, args) {
	sharedVars.vars.isSpamWarningTriggered = checkForSpam(msg);
	const randomWordFromArray = Math.floor(Math.random() * JSONLib.getJSONWordArray().length);

	if (sharedVars.vars.isSpamWarningTriggered === true) {
		sharedVars.vars.isSpamWarningTriggered = false;
		sharedVars.vars.spammerCount = 0;
		msg.delete({ timeout: 2000 });
		msg.channel.send(`${msg.author} ${sharedVars.text.warningForSpam}`)
			.then(msg => {
				msg.delete({ timeout: 2000 });
			});
		return;
	}
	else if (args.length === 1) {
		msg.channel.send(`${args[0]} ${randomWordsArray[randomWordFromArray]}`);
		return;
	}
	else {
		msg.channel.send(`${msg.author} ${randomWordsArray[randomWordFromArray]}`);
		return;
	}
}

function checkForSpam(msg) {
	if (sharedVars.vars.spammerCount >= 3 && sharedVars.vars.spammerID === msg.author.id) {
		return true;
	}
	else if (sharedVars.vars.spammerCount < 3 && sharedVars.vars.spammerID === msg.author.id) {
		sharedVars.vars.spammerCount++;
		return false;
	}
	else {
		sharedVars.vars.spammerID = msg.author.id;
		sharedVars.vars.spammerCount = 1;
		return false;
	}
}

module.exports = {
	name: 'getRandomWord',
	description: 'This module returns a random word from JSON array (Also, it checking for spam (3-4 messages in a row) and returns a warning)',
	cooldown: 2,
	execute(msg, args) {
		getRandomWord(msg, args);
	},
};
