'use strict';
const fs = require('fs');
const JSONLib = require('../libs/JSONHandlerLib');
const preloadedArrays = JSONLib.loadAllJSONArrays();
const arrayPaths = JSONLib.loadAllJSONPaths();

function chooseArrayToModify(msg, args) {
	if (args.length === 1) {
		deleteWord(msg, args)
	}
	else if (args.length >= 2 && args[0] === 'bot') {
		deleteBot(msg, args)
	}
	else if (args.length >= 3 && args[0] === 'roulette') {
		deleteWordRoulette(msg, args);
	}
	else {
		return;
	}
}

function deleteWord(msg, args) {
	const textString = args.join(' ');
	const wordInArray = preloadedArrays[0].indexOf(textString);
	if (wordInArray !== -1) {
		preloadedArrays[0].splice(wordInArray, 1);
		fs.writeFileSync(arrayPaths[0], JSON.stringify(preloadedArrays[0], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я удалил это слово у себя. Неужели кто-то очищает меня от этого...')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Прости, я не нашёл это слово у себя и мне нечего удалять')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

function deleteBot(msg, args) {
	const botID = args[1];
	const botInArray = preloadedArrays[1].indexOf(botID);
	if (botInArray !== -1) {
		preloadedArrays[1].splice(botInArray, 1);
		fs.writeFileSync(arrayPaths[1], JSON.stringify(preloadedArrays[1], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я удалил этого бота у себя. Теперь я не буду его игнорировать!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Прости, я не нашёл этого бота у себя и мне некого убирать')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

function deleteWordRoulette(msg, args) {
	let numberOfArray = 0;
	if (fileChooser === 'win') {
		numberOfArray = 2;
	}
	else if (fileChooser === 'lose') {
		numberOfArray = 3;
	}
	else if (fileChooser === 'zero') {
		numberOfArray = 4;
	}
	else if (fileChooser === 'minus') {
		numberOfArray = 5;
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	const wordInArray = preloadedArrays[numberOfArray].indexOf(args.splice(0, 2).join(' '));
	if (wordInArray !== -1) {
		preloadedArrays[numberOfArray].splice(wordInArray, 1);
		fs.writeFileSync(arrayPaths[numberOfArray], JSON.stringify(preloadedArrays[numberOfArray], null, 2));
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я удалил это слово у себя. Неужели кто-то очищает меня от этого...')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Прости, я не нашёл это слово у себя и мне нечего удалять')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'deleteWord',
	description: 'Deleting old word from JSON Array',
	execute(msg, args) {
		chooseArrayToModify(msg, args);
	},
};
