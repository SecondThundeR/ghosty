'use strict';
const fs = require('fs');
const sharedVars = require('../data/variables');
const JSONLib = require('../libs/JSONHandlerLib');
const arrayAndPaths = JSONLib.getAllArraysAndPaths();
const delayTime = 3000;

function chooseArrayToModify(msg, args) {
	switch (args[0]) {
	case 'bot':
		deleteBot(msg, args);
		break;
	case 'roulette':
		deleteWordRoulette(msg, args);
		break;
	default:
		deleteWord(msg, args);
		break;
	}
}

function deleteWord(msg, args) {
	const textString = args.join(' ');
	const wordInArray = arrayAndPaths[1][0].indexOf(textString);
	switch (wordInArray) {
	case -1:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failDeleteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		arrayAndPaths[1][0].splice(wordInArray, 1);
		fs.writeFileSync(arrayAndPaths[0][0], JSON.stringify(arrayAndPaths[1][0], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successDeleteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function deleteBot(msg, args) {
	const botID = args[1];
	const botInArray = arrayAndPaths[1][1].indexOf(botID);
	switch (botInArray) {
	case -1:
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failDeleteBot)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		arrayAndPaths[1][1].splice(botInArray, 1);
		fs.writeFileSync(arrayAndPaths[0][1], JSON.stringify(arrayAndPaths[1][1], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successDeleteBot)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function deleteWordRoulette(msg, args) {
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
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.failDeleteRouletteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		arrayAndPaths[1][numberOfArray].splice(wordInArray, 1);
		fs.writeFileSync(arrayAndPaths[0][numberOfArray], JSON.stringify(arrayAndPaths[1][numberOfArray], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.successDeleteRouletteWord)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

module.exports = {
	name: 'deleteWord',
	description: 'Module delete word from JSON Arrays',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
