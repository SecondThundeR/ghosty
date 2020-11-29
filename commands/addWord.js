'use strict';
const fs = require('fs');
const JSONLib = require('../libs/JSONHandlerLib');
const preloadedArrays = JSONLib.loadAllJSONArrays();
const arrayPaths = JSONLib.loadAllJSONPaths();

function chooseArrayToModify(msg, args) {
	if (args.length === 1) {
		addWord(msg, args)
	}
	else if (args.length >= 2 && args[0] === 'bot') {
		addBot(msg, args)
	}
	else if (args.length >= 3 && args[0] === 'roulette') {
		addWordRoulette(msg, args);
	}
	else {
		return;
	}
}

function addWord(msg, args) {
	const textString = args.join(' ');
	const wordInArray = preloadedArrays[0].indexOf(textString);
	if (wordInArray === -1) {
		preloadedArrays[0].push(textString);
		fs.writeFileSync(arrayPaths[0], JSON.stringify(preloadedArrays[0], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

function addBot(msg, args) {
	const botID = args[1];
	const botInArray = preloadedArrays[1].indexOf(botID);
	if (botInArray === -1) {
		preloadedArrays[1].push(botID);
		fs.writeFileSync(arrayPaths[1], JSON.stringify(preloadedArrays[1], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я добавил этого бота в исключения! Теперь я буду его игнорировать')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Данный бот уже есть у меня в исключениях!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

function addWordRoulette(msg, args) {
	const textString = args.splice(0, 2).join(' ');
	let numberOfArray = 0;
	if (args[1] === 'win') {
		numberOfArray = 2;
	}
	else if (args[1] === 'lose') {
		numberOfArray = 3;
	}
	else if (args[1] === 'zero') {
		numberOfArray = 4;
	}
	else if (args[1] === 'minus') {
		numberOfArray = 5;
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	const wordInArray = preloadedArrays[numberOfArray].indexOf(textString);
	if (wordInArray === -1) {
		preloadedArrays[numberOfArray].push(textString);
		fs.writeFileSync(arrayPaths[numberOfArray], JSON.stringify(preloadedArrays[numberOfArray], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'addWord',
	description: 'Adding new word to JSON Array',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
