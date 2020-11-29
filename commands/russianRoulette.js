'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const wordsArray = JSONLib.getJSONRouletteData();
const utilityArray = JSONLib.getJSONUtilityData();
let randomWordArray = [];

function getRandomGameWords() {
	randomWordArray = [];
	const randomWordNumWin = Math.floor(Math.random() * wordsArray[0].length);
	randomWordArray.push(wordsArray[0][randomWordNumWin]);
	const randomWordNumLose = Math.floor(Math.random() * wordsArray[1].length);
	randomWordArray.push(wordsArray[1][randomWordNumLose]);
	const randomWordNumZero = Math.floor(Math.random() * wordsArray[2].length);
	randomWordArray.push(wordsArray[2][randomWordNumZero]);
	const randomWordNumMinus = Math.floor(Math.random() * wordsArray[3].length);
	randomWordArray.push(wordsArray[3][randomWordNumMinus]);
	return;
}

async function russianRoulette(msg, args) {
	const randomTimeFromArray = Math.floor(Math.random() * utilityArray[1].length);
	const delayTime = utilityArray[1][randomTimeFromArray];
	getRandomGameWords();

	let bulletCount = 0;
	let bulletNumber = 0;
	let randomNumber = 0;

	bulletCount = Number(args);

	if (bulletCount === 1) {
		bulletNumber = Math.floor(Math.random() * 6) + 1;
		randomNumber = Math.floor(Math.random() * 6) + 1;

		if (bulletNumber === randomNumber) {
			msg.channel.send('**БАХ**').then((msg) => setTimeout(function() {
				msg.edit(`${msg.author} ${randomWordArray[1]}`);
			}, delayTime));
			return;
		}
		else {
			msg.channel.send('*мертвая тишина...*').then((msg) => setTimeout(function() {
				msg.edit(`${msg.author} ${randomWordArray[0]}`);
			}, delayTime));
			return;
		}
	}
	else if (bulletCount === 0) {
		msg.channel.send(`${msg.author} ${randomWordArray[2]}`);
		return;
	}
	else if (bulletCount > 6) {
		msg.channel.send(`${msg.author} по правилам русской рулетки, можно брать только до 6 патронов`);
		return;
	}
	else if (bulletCount === 6) {
		msg.channel.send(`поздравляем! теперь у нас на одного суицидника меньше. им был ${msg.author}`);
		return;
	}
	else if (bulletCount < 0) {
		msg.channel.send(`${msg.author} ${randomWordArray[3]}`);
		return;
	}
	else {
		const bulletNumberArray = [];

		for (let i = 0; i < bulletCount; i++) {
			const bulletNumber = Math.floor(Math.random() * 6) + 1;
			if (bulletNumberArray.includes(bulletNumber) === true) {
				i--;
			}
			else {
				bulletNumberArray.push(bulletNumber);
			}
		}
		randomNumber = Math.floor(Math.random() * 6) + 1;
		if (bulletNumberArray.includes(randomNumber) === true) {
			msg.channel.send('**БАХ**').then((msg) => setTimeout(function() {
				msg.edit(`${msg.author} ${randomWordArray[1]}`);
			}, delayTime));
			return;
		}
		else {
			msg.channel.send('*мертвая тишина...*').then((msg) => setTimeout(function() {
				msg.edit(`${msg.author} ${randomWordArray[0]}`);
			}, delayTime));
			return;
		}
	}
}

module.exports = {
	name: 'russianRoulette',
	description: 'Russian roulette simulator',
	cooldown: 2,
	execute(msg, args) {
		russianRoulette(msg, args);
	},
};
