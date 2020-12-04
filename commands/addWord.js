'use strict';
const fs = require('fs');
const JSONLib = require('../libs/JSONHandlerLib');
const preloadedArrays = JSONLib.loadAllJSONArrays();
const arrayPaths = JSONLib.loadAllJSONPaths();
const delayTime = 3000;

function chooseArrayToModify(msg, args) {
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

function addWord(msg, args) {
	const textString = args.join(' ');
	const wordInArray = preloadedArrays[0].indexOf(textString);
	switch (wordInArray) {
	case -1:
		preloadedArrays[0].push(textString);
		fs.writeFileSync(arrayPaths[0], JSON.stringify(preloadedArrays[0], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function addBot(msg, args) {
	const botID = args[1];
	const botInArray = preloadedArrays[1].indexOf(botID);
	switch (botInArray) {
	case -1:
		preloadedArrays[1].push(botID);
		fs.writeFileSync(arrayPaths[1], JSON.stringify(preloadedArrays[1], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я добавил этого бота в исключения! Теперь я буду его игнорировать')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Данный бот уже есть у меня в исключениях!')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

function addWordRoulette(msg, args) {
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
		preloadedArrays[numberOfArray].push(textString);
		fs.writeFileSync(arrayPaths[numberOfArray], JSON.stringify(preloadedArrays[numberOfArray], null, 2));
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	default:
		msg.delete({ timeout: delayTime });
		msg.channel.send('Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего')
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
}

module.exports = {
	name: 'addWord',
	description: 'Adding new word to JSON Array',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
