'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const getRandomUser = require('../libs/getRandomUser');
const spamChecker = require('../libs/spamChecker');
const randomWordsArray = JSONLib.getWordsArray();
const delayTime = 3000;

async function getRandomWord(msg, args) {
	const randomWordFromArray = Math.floor(Math.random() * JSONLib.getWordsArray().length);
	const isSpamWarningTriggered = spamChecker(msg);
	let currentUser = '';

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
		if (args[0] === 'рандом') {
			const userInfo = await getRandomUser(msg);
			currentUser = userInfo[0];
		}
		else if (args.length === 0) {
			currentUser = msg.author;
		}
		else {
			currentUser = args[0];
		}
		msg.channel.send(`${currentUser} ${randomWordsArray[randomWordFromArray]}`);
		break;
	}
}

module.exports = {
	name: 'getRandomWord',
	description: 'Module returns a random word from JSON array',
	cooldown: 2,
	execute(msg, args) {
		getRandomWord(msg, args);
	},
};
