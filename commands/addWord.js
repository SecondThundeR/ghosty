'use strict';
const fs = require('fs');
const sharedVars = require('../data/variables');
const JSONLib = require('../libs/JSONHandlerLib');
const arrayAndPaths = JSONLib.getAllArraysAndPaths();
const delayTime = 3000;

function chooseArrayToModify(msg, args) {
	if (!args.length) {
		msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
	}
	else {
		switch (args[0]) {
		case 'bot':
			addBot(msg, args);
			break;
		case 'roulette':
			addWordRoulette(msg, args);
			break;
		default:
			addWord(msg, args);
			break;
		}
	}
}

function addWord(msg, args) {
	const textString = args.join(' ');
	const wordInArray = arrayAndPaths[1][0].indexOf(textString);
	switch (wordInArray) {
	case -1:
		arrayAndPaths[1][0].push(textString);
		fs.writeFileSync(arrayAndPaths[0][0], JSON.stringify(arrayAndPaths[1][0], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successAddWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failAddWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function addBot(msg, args) {
	const botID = args[1];
	const botInArray = arrayAndPaths[1][1].indexOf(botID);
	switch (botInArray) {
	case -1:
		arrayAndPaths[1][1].push(botID);
		fs.writeFileSync(arrayAndPaths[0][1], JSON.stringify(arrayAndPaths[1][1], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successAddBot)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failAddBot)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function addWordRoulette(msg, args) {
	let numberOfArray = 0;
	switch (args[1]) {
	case 'win':
		numberOfArray = 2;
		break;
	case 'lose':
		numberOfArray = 3;
		break;
	case 'zero':
		numberOfArray = 4;
		break;
	case 'minus':
		numberOfArray = 5;
		break;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.notFoundFileRoulette)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
	args.splice(0, 2);
	const textString = args.join(' ');
	const wordInArray = arrayAndPaths[1][numberOfArray].indexOf(textString);
	switch (wordInArray) {
	case -1:
		arrayAndPaths[1][numberOfArray].push(textString);
		fs.writeFileSync(arrayAndPaths[0][numberOfArray], JSON.stringify(arrayAndPaths[1][numberOfArray], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successAddRouletteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failAddRouletteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

module.exports = {
	name: 'addWord',
	description: 'Module add new word to JSON Arrays',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
