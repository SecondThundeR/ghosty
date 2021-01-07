'use strict';
const getRandomUser = require('../libs/getRandomUser');
const sharedVars = require('../data/variables');

async function userChecker(msg, args, command) {
	const randomPercent = Math.floor(Math.random() * 101);
	let currentUser;
	if (args[0] === 'рандом') {
		const userInfo = await getRandomUser(msg);
		currentUser = userInfo[0];
	}
	else if (args[0] === 'тест' && args.length === 1) {
		currentUser = msg.author;
	}
	else {
		args.shift();
		currentUser = args.join(' ');
	}
	switch (randomPercent) {
	case 0:
		msg.channel.send(`${currentUser}${sharedVars.text.noneSomeone1}${command}${sharedVars.text.noneSomeone2}`);
		break;
	case 100:
		msg.channel.send(`${currentUser}${sharedVars.text.fullSomeone1}${command}${sharedVars.text.fullSomeone2}${randomPercent}${sharedVars.text.someonePercent}`);
		break;
	default:
		msg.channel.send(`${currentUser} ${command}${sharedVars.text.someoneDefaultPart}${randomPercent}${sharedVars.text.someonePercent}`);
		break;
	}
}

module.exports = {
	name: 'userChecker',
	description: 'Module returns a random percentage that shows how someone is',
	cooldown: 2,
	execute(msg, args, command) {
		userChecker(msg, args, command);
	},
};
