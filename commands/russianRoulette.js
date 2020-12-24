'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const wordsArray = JSONLib.getRouletteArrays();
const delayTime = 3000;

function getRandomWords() {
	const randomWinWord = wordsArray[0][Math.floor(Math.random() * wordsArray[0].length)];
	const randomLoseWord = wordsArray[1][Math.floor(Math.random() * wordsArray[1].length)];
	const randomZeroWord = wordsArray[2][Math.floor(Math.random() * wordsArray[2].length)];
	const randomMinusWord = wordsArray[3][Math.floor(Math.random() * wordsArray[3].length)];
	return [ randomWinWord, randomLoseWord, randomZeroWord, randomMinusWord ];
}

function russianRoulette(msg, args) {
	const randomWordArray = getRandomWords();
	const bulletNumberArray = [];
	const playerName = msg.author;
	let bulletToShoot = 0;
	let bulletCount = 0;

	if (!args.length) {
		bulletCount = 1;
	}
	else {
		bulletCount = Number(args);
	}

	if (isNaN(bulletCount)) {
		return;
	}

	if (bulletCount === 0) {
		msg.reply(randomWordArray[2]);
		return;
	}
	else if (bulletCount < 0) {
		msg.reply(randomWordArray[3]);
		return;
	}
	else if (bulletCount === 6) {
		msg.reply(sharedVars.text.rouletteSixBulletsWarning);
		return;
	}
	else if (bulletCount > 6) {
		msg.reply(sharedVars.text.rouletteSixAndMoreBulletsWarning);
		return;
	}
	else {
		for (let i = 0; i < bulletCount; i++) {
			const bulletToShootNumber = Math.floor(Math.random() * 6) + 1;
			const isWordRepeat = bulletNumberArray.includes(bulletToShootNumber);
			if (isWordRepeat === true) {
				i--;
			}
			else {
				bulletNumberArray.push(bulletToShootNumber);
			}
		}
		bulletToShoot = Math.floor(Math.random() * 6) + 1;
		if (bulletNumberArray.includes(bulletToShoot) === true) {
			msg.channel.send(sharedVars.text.rouletteLoseWarning).then((msg) => setTimeout(function() {
				msg.edit(`${playerName} ${randomWordArray[1]}`);
			}, delayTime));
			return;
		}
		else {
			msg.channel.send(sharedVars.text.rouletteWinWarning).then((msg) => setTimeout(function() {
				msg.edit(`${playerName} ${randomWordArray[0]}`);
			}, delayTime));
			return;
		}
	}
}

module.exports = {
	name: 'russianRoulette',
	description: 'Module handles Russian Roulette game',
	cooldown: 2,
	execute(msg, args) {
		russianRoulette(msg, args);
	},
};
