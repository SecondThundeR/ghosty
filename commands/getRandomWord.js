'use strict';
const fs = require('fs');
const sharedVars = require('../data/variables');
const pathToJSON = './jsonArrays/array.json';

function getJSONArrayContent() {
	const rawData = fs.readFileSync(pathToJSON);
	const parsedData = JSON.parse(rawData);
	return parsedData;
}

function getRandomWord(msg) {
	sharedVars.vars.isSpamWarningTriggered = checkForSpam(msg);
	if (sharedVars.vars.isSpamWarningTriggered === true) {
		sharedVars.vars.isSpamWarningTriggered === false;
		sharedVars.vars.spammerCount = 0;
		msg.delete({ timeout: 3000 });
		msg.channel.send(`${msg.author} ${sharedVars.vars.warningForSpam}`)
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
		return;
	}

	else {
		const randomWordsArray = getJSONArrayContent();
		const randomWordFromArray = Math.floor(Math.random() * randomWordsArray.length);
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
	description: 'Returns random word from JSON array + check for spam',
	execute(msg) {
		getRandomWord(msg);
	},
};
