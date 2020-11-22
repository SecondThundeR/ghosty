'use strict';
const fs = require('fs');

let convertedDataWin;
let convertedDataLose;
let convertedDataZero;
let convertedDataMinus;

let randomWordWin;
let randomWordLose;
let randomWordZero;
let randomWordMinus;

let msgTime;

let ttsEnabled = true;

function getJSONContents() {
	const dataWin = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsWin.json');
	convertedDataWin = JSON.parse(dataWin);
	const dataLose = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsLose.json');
	convertedDataLose = JSON.parse(dataLose);
	const dataZero = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsZero.json');
	convertedDataZero = JSON.parse(dataZero);
	const dataMinus = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsMinus.json');
	convertedDataMinus = JSON.parse(dataMinus);
	const msgTimeData = fs.readFileSync('./jsonArrays/msgTime.json');
	msgTime = JSON.parse(msgTimeData);

	const randomWordNumWin = Math.floor(Math.random() * convertedDataWin.length);
	randomWordWin = convertedDataWin[randomWordNumWin];
	const randomWordNumLose = Math.floor(Math.random() * convertedDataLose.length);
	randomWordLose = convertedDataLose[randomWordNumLose];
	const randomWordNumZero = Math.floor(Math.random() * convertedDataZero.length);
	randomWordZero = convertedDataZero[randomWordNumZero];
	const randomWordNumMinus = Math.floor(Math.random() * convertedDataMinus.length);
	randomWordMinus = convertedDataMinus[randomWordNumMinus];
	return;
}

async function russianRoulette(msg, args) {
	getJSONContents();

	const randomTime = Math.floor(Math.random() * msgTime.length);
	const currTime = msgTime[randomTime];

	let bulletCount = 0;
	let bulletNumber = 0;
	let randomNumber = 0;
	let ttsTrigger = false;

	if (typeof args === 'string') {
		bulletCount = Number(args);
	}
	else if (typeof args === 'boolean') {
		ttsTrigger = true;
	}
	else {
		bulletCount = args;
	}

	if (ttsTrigger === true) {
		if (ttsEnabled === true) {
			ttsEnabled = false;
			msg.channel.send('Теперь сообщения не будут работать с TTS');
		}
		else {
			ttsEnabled = true;
			msg.channel.send('Теперь сообщения будут работать с TTS');
		}
		ttsTrigger = false;
		return;
	}
	else {
		ttsTrigger = false;
	}

	if (bulletCount === 1) {
		bulletNumber = Math.floor(Math.random() * 6) + 1;
		randomNumber = Math.floor(Math.random() * 6) + 1;

		if (bulletNumber === randomNumber) {
			msg.channel.send('БАХ', {
				tts: ttsEnabled,
			}).then((msg) => setTimeout(function() {
				msg.edit('*БАХ*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordLose}`);
		}
		else {
			msg.channel.send('мертвая тишина...', {
				tts: ttsEnabled,
			}).then((msg) => setTimeout(function() {
				msg.edit('*мертвая тишина...*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordWin}`);
		}
	}
	else if (bulletCount === 0) {
		msg.channel.send(`${randomWordZero}`);
	}
	else if (bulletCount > 6) {
		msg.channel.send(`${msg.author} по правилам русской рулетки, можно брать только до 6 патронов`);
	}
	else if (bulletCount === 6) {
		msg.channel.send(`поздравляем! теперь у нас на одного суицидника меньше. им был ${msg.author}`);
	}
	else if (bulletCount < 0) {
		msg.channel.send(`${randomWordMinus}`, {
			tts: ttsEnabled,
		});
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
				tts: ttsEnabled,
			}).then((msg) => setTimeout(function() {
				msg.edit('*БАХ*');
			}, 4000));
			await new Promise(r => setTimeout(r, currTime));
			msg.channel.send(`${msg.author} ${randomWordLose}`);
		}
		else {
			msg.channel.send('мертвая тишина...', {
				tts: ttsEnabled,
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
	cooldown: 2,
	execute(msg, args) {
		russianRoulette(msg, args);
	},
};
