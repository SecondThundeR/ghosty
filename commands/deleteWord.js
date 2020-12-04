'use strict';
const fs = require('fs');
const JSONLib = require('../libs/JSONHandlerLib');
const preloadedArrays = JSONLib.loadAllJSONArrays();
const arrayPaths = JSONLib.loadAllJSONPaths();
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
	const wordInArray = preloadedArrays[0].indexOf(textString);
	switch (wordInArray) {
	case -1:
		preloadedArrays[0].splice(wordInArray, 1);
		fs.writeFileSync(arrayPaths[0], JSON.stringify(preloadedArrays[0], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я удалил это слово у себя. Неужели кто-то очищает меня от этого...')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Прости, я не нашёл это слово у себя и мне нечего удалять')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function deleteBot(msg, args) {
	const botID = args[1];
	const botInArray = preloadedArrays[1].indexOf(botID);
	switch (botInArray) {
	case -1:
		preloadedArrays[1].splice(botInArray, 1);
		fs.writeFileSync(arrayPaths[1], JSON.stringify(preloadedArrays[1], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я удалил этого бота у себя. Теперь я не буду его игнорировать!')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Прости, я не нашёл этого бота у себя и мне некого убирать')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function deleteWordRoulette(msg, args) {
	const textString = args.splice(0, 2).join(' ');
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
		msg.channel.send('Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
	const wordInArray = preloadedArrays[numberOfArray].indexOf(textString);
	switch (wordInArray) {
	case -1:
		preloadedArrays[numberOfArray].splice(wordInArray, 1);
		fs.writeFileSync(arrayPaths[numberOfArray], JSON.stringify(preloadedArrays[numberOfArray], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я удалил это слово у себя. Неужели кто-то очищает меня от этого...')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Прости, я не нашёл это слово у себя и мне нечего удалять')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

module.exports = {
	name: 'deleteWord',
	description: 'Deleting old word from JSON Array',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
