'use strict';
const fs = require('fs');
const sharedVars = require('../data/variables');
const pathToJSON = './jsonArrays/array.json';
const warningText = sharedVars.vars.warningForSpam;

function getJSONArrayContent() {
	const rawData = fs.readFileSync(pathToJSON);
	const parsedData = JSON.parse(rawData);
	return parsedData;
}

function getRandomWord(msg) {
	checkForSpam(msg);
	if (sharedVars.vars.isSpamWarningTriggered === true) {
		sharedVars.vars.isSpamWarningTriggered === false;
		sharedVars.vars.spammerCount = 0;
		msg.delete({ timeout: 3000 });
		msg.channel.send(`${msg.author} ` + warningText)
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
		return;
	}
	else {
		const randomWordsArray = getJSONArrayContent();
		const randomWordFromArray = Math.floor(Math.random() * randomWordFromArray.length);
		return `${msg.author} ` + randomWordsArray[randomWordFromArray];
	}
}

function checkForSpam(msg) {
	if (sharedVars.vars.spammerCount >= 3 && sharedVars.vars.spammerID === msg.author.id) {
		sharedVars.vars.isSpamWarningTriggered = true;
		return;
	}
	else if (sharedVars.vars.spammerCount < 3 && sharedVars.vars.spammerID === msg.author.id) {
		sharedVars.vars.spammerCount++;
		return;
	}
	else {
		sharedVars.vars.spammerID = msg.author.id;
		sharedVars.vars.spammerCount = 1;
		return;
	}
}

module.exports = {
	name: 'getRandomWord',
	description: 'Returns random word from JSON array + check for spam',
	execute(msg) {
		msg.channel.send(getRandomWord(msg));
	},
};
