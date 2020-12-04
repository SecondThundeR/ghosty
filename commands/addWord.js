'use strict';
const fs = require('fs');
const JSONLib = require('../libs/JSONHandlerLib');
const arrayAndPaths = JSONLib.getAllArraysAndPaths();
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
	const wordInArray = arrayAndPaths[1][0].indexOf(textString);
	switch (wordInArray) {
	case -1:
		arrayAndPaths[1][0].push(textString);
		fs.writeFileSync(arrayAndPaths[0][0], JSON.stringify(arrayAndPaths[1][0], null, 2));
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
	const botInArray = arrayAndPaths[1][1].indexOf(botID);
	switch (botInArray) {
	case -1:
		arrayAndPaths[1][1].push(botID);
		fs.writeFileSync(arrayAndPaths[0][1], JSON.stringify(arrayAndPaths[1][1], null, 2));
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
	args.splice(0, 2);
	const textString = args.join(' ');
	const wordInArray = arrayAndPaths[1][numberOfArray].indexOf(textString);
	switch (wordInArray) {
	case -1:
		arrayAndPaths[1][numberOfArray].push(textString);
		fs.writeFileSync(arrayAndPaths[0][numberOfArray], JSON.stringify(arrayAndPaths[1][numberOfArray], null, 2));
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
