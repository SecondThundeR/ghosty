/* eslint-disable no-shadow */
const fs = require('fs');
const { msgTime } = require('../data/arrays');

let convertedDataWin;
let convertedDataLose;
let convertedDataZero;

function getJSONContents() {
	const dataWin = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsWin.json');
	convertedDataWin = JSON.parse(dataWin);
	const dataLose = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsLose.json');
	convertedDataLose = JSON.parse(dataLose);
	const dataZero = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsZero.json');
	convertedDataZero = JSON.parse(dataZero);
}

async function russianRoulette(msg, args) {
	getJSONContents();
	const randomWordNumWin = Math.floor(Math.random() * convertedDataWin.length);
	const randomWordWin = convertedDataWin[randomWordNumWin];

	const randomWordNumLose = Math.floor(Math.random() * convertedDataLose.length);
	const randomWordLose = convertedDataLose[randomWordNumLose];

	const randomWordNumZero = Math.floor(Math.random() * convertedDataZero.length);
	const randomWordZero = convertedDataZero[randomWordNumZero];

	const randomTime = Math.floor(Math.random() * msgTime.length);
	const currTime = msgTime[randomTime];

	let bulletCount = 0;
	let bulletNumber = 0;
	let randomNumber = 0;

	if (typeof args === 'string') {
		bulletCount = Number(args);
	}
	else {
		bulletCount = args;
	}

	if (bulletCount === 1) {
		bulletNumber = Math.floor(Math.random() * 6) + 1;
		randomNumber = Math.floor(Math.random() * 6) + 1;

		if (bulletNumber === randomNumber) {
			msg.channel.send('БАХ', {
				tts: true,
			}).then((msg) => setTimeout(function() {
				msg.edit('*БАХ*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordLose}`);
		}
		else {
			msg.channel.send('мертвая тишина...', {
				tts: true,
			}).then((msg) => setTimeout(function() {
				msg.edit('*мертвая тишина...*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordWin}`);
		}
	}
	else if (bulletCount === 0) {
		msg.channel.send(`${randomWordZero}`)
			.then(msg => {
				msg.delete({ timeout: 5000 });
			});
	}
	else if (bulletCount > 6) {
		msg.channel.send(`${msg.author} по правилам русской рулетки, можно брать только до 6 патронов`);
	}
	else if (bulletCount === 6) {
		msg.channel.send(`поздравляем! теперь у нас на одного суицидника меньше. им был ${msg.author}`);
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
			msg.channel.send('БАХ', {
				tts: true,
			}).then((msg) => setTimeout(function() {
				msg.edit('*БАХ*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordLose}`);
		}
		else {
			msg.channel.send('мертвая тишина...', {
				tts: true,
			}).then((msg) => setTimeout(function() {
				msg.edit('*мертвая тишина...*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordWin}`);
		}
	}
}

module.exports = {
	name: 'russianRoulette',
	description: 'Russian roulette simulator',
	execute(msg, args) {
		russianRoulette(msg, args);
	},
};
