'use strict';
const sharedVars = require('../data/variables');

function checkerSelector(msg, args, command) {
	switch(command) {
	case 'гей':
		msg.channel.send(gayChecker(msg, args));
		break;
	case 'аниме':
		msg.channel.send(animeChecker(msg, args));
		break;
	case 'алина':
		msg.channel.send(alinaChecker(msg, args));
		break;
	case 'влад':
		msg.channel.send(vladChecker(msg, args));
		break;
	default:
		break;
	}
}

function gayChecker(msg, args) {
	const randomPercent = Math.floor(Math.random() * 101);
	switch (args.length) {
	case 1:
		switch (randomPercent) {
		case 0:
			return `${msg.author} ${sharedVars.text.noneGay}`;
		case 100:
			return `${msg.author} ${sharedVars.text.fullGay} ${randomPercent}${sharedVars.text.gayPercent}`;
		default:
			return `${msg.author} ${sharedVars.text.gayDefaultPart} ${randomPercent}${sharedVars.text.gayPercent}`;
		}
	case 2:
		switch (randomPercent) {
		case 0:
			return `${args[1]} ${sharedVars.text.noneGay}`;
		case 100:
			return `${args[1]} ${sharedVars.text.fullGay} ${randomPercent}${sharedVars.text.gayTextPercent}`;
		default:
			return `${args[1]} ${sharedVars.text.gayDefaultPart} ${randomPercent}${sharedVars.text.gayPercent}`;
		}
	default:
		break;
	}
}

function animeChecker(msg, args) {
	const randomPercent = Math.floor(Math.random() * 101);
	switch (args.length) {
	case 1:
		switch (randomPercent) {
		case 0:
			return `${msg.author} ${sharedVars.text.noneAnime}`;
		case 100:
			return `${msg.author} ${sharedVars.text.fullAnime} ${randomPercent}${sharedVars.text.animePercent}`;
		default:
			return `${msg.author} ${sharedVars.text.animeDefaultPart} ${randomPercent}${sharedVars.text.animePercent}`;
		}
	case 2:
		switch (randomPercent) {
		case 0:
			return `${args[1]} ${sharedVars.text.noneAnime}`;
		case 100:
			return `${args[1]} ${sharedVars.text.fullAnime} ${randomPercent}${sharedVars.text.animePercent}`;
		default:
			return `${args[1]} ${sharedVars.text.animeDefaultPart} ${randomPercent}${sharedVars.text.animePercent}`;
		}
	default:
		break;
	}
}

function alinaChecker(msg, args) {
	const randomPercent = Math.floor(Math.random() * 101);
	switch (args.length) {
	case 1:
		switch (randomPercent) {
		case 0:
			return `${msg.author} ${sharedVars.text.noneAlina}`;
		case 100:
			return `${msg.author} ${sharedVars.text.fullAlina} ${randomPercent}${sharedVars.text.alinaPercent}`;
		default:
			return `${msg.author} ${sharedVars.text.alinaDefaultPart} ${randomPercent}${sharedVars.text.alinaPercent}`;
		}
	case 2:
		switch (randomPercent) {
		case 0:
			return `${args[1]} ${sharedVars.text.noneAlina}`;
		case 100:
			return `${args[1]} ${sharedVars.text.fullAlina} ${randomPercent}${sharedVars.text.alinaPercent}`;
		default:
			return `${args[1]} ${sharedVars.text.alinaDefaultPart} ${randomPercent}${sharedVars.text.alinaPercent}`;
		}
	default:
		break;
	}
}

function vladChecker(msg, args) {
	const randomPercent = Math.floor(Math.random() * 101);
	switch (args.length) {
	case 1:
		switch (randomPercent) {
		case 0:
			return `${msg.author}${sharedVars.text.noneVlad}`;
		case 100:
			return `${msg.author}${sharedVars.text.fullVlad}${randomPercent}${sharedVars.text.vladPercent}`;
		default:
			return `${msg.author}${sharedVars.text.vladDefaultPart}${randomPercent}${sharedVars.text.vladPercent}`;
		}
	case 2:
		switch (randomPercent) {
		case 0:
			return `${args[1]}${sharedVars.text.noneVlad}`;
		case 100:
			return `${args[1]}${sharedVars.text.fullVlad}${randomPercent}${sharedVars.text.vladPercent}`;
		default:
			return `${args[1]}${sharedVars.text.vladDefaultPart}${randomPercent}${sharedVars.text.vladPercent}`;
		}
	}
}

module.exports = {
	name: 'userChecker',
	description: 'Module returns a random percentage that shows how someone is',
	cooldown: 3,
	execute(msg, args, command) {
		checkerSelector(msg, args, command);
	},
};
