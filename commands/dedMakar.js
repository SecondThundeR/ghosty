'use strict';
const getRandomUser = require('../libs/getRandomUser');
const sharedVars = require('../data/variables');

function reverseString(str) {
	return str.split('').reverse().join('');
}

async function dedMakar(msg, args) {
	let username;
	if (!args.length) {
		const userInfo = await getRandomUser(msg);
		username = userInfo[1];
	}
	else if (args[0].startsWith('<@&')) {
		msg.channel.send(sharedVars.text.makarErrorParsing);
		return;
	}
	else if (args[0].startsWith('<@!')) {
		const userInfo = await msg.guild.members.fetch(args[0].slice(3).slice(0, -1));
		username = userInfo.displayName;
	}
	else if (args[0].startsWith('<:')) {
		msg.channel.send(sharedVars.text.makarErrorEmoji);
		return;
	}
	else {
		const textString = args.join(' ');
		username = textString;
	}
	msg.channel.send(`${sharedVars.text.makarDefaultText}${reverseString(username)}`);
	return;
}

module.exports = {
	name: 'dedMakar',
	description: 'Module returns a text sentence with reversed name of user',
	execute(msg, args) {
		dedMakar(msg, args);
	},
};
