const fs = require('fs');
const sharedVars = require('../data/variables');

function getJSONContents() {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const convertedData = JSON.parse(data);
	return convertedData;
}

function randomCringe(msg) {
	const warningText = noSpamWarning(msg);

	if (warningText === sharedVars.vars.warningForSpam) {
		return `${msg.author} ` + warningText;
	}
	else {
		const cringeArray = getJSONContents();
		const randomWord = Math.floor(Math.random() * cringeArray.length);
		return `${msg.author} ` + cringeArray[randomWord];
	}
}

function noSpamWarning(msg) {
	if (sharedVars.vars.spammerCount >= 3 && sharedVars.vars.spammerID === msg.author.id) {
		sharedVars.vars.spammerCount = 0;
		return sharedVars.vars.warningForSpam;
	}
	else if (sharedVars.vars.spammerCount < 3 && sharedVars.vars.spammerID === msg.author.id) {
		sharedVars.vars.spammerCount++;
	}
	else {
		sharedVars.vars.spammerID = msg.author.id;
		sharedVars.vars.spammerCount = 1;
	}
}

module.exports = {
	name: 'randomCringe',
	description: 'Returns random word from cringe array + check for spam',
	execute(msg) {
		msg.channel.send(randomCringe(msg));
	},
};
