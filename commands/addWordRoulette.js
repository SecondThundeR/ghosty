'use strict';
const fs = require('fs');

function addWordRoulette(msg, fileChooser, textString) {
	let path = '';
	if (fileChooser === 'lose') {
		path = './jsonArrays/russianRouletteWords/rouletteWordsLose.json';
	}
	else if (fileChooser === 'minus') {
		path = './jsonArrays/russianRouletteWords/rouletteWordsMinus.json';
	}
	else if (fileChooser === 'win') {
		path = './jsonArrays/russianRouletteWords/rouletteWordsWin.json';
	}
	else if (fileChooser === 'zero') {
		path = './jsonArrays/russianRouletteWords/rouletteWordsZero.json';
	}
	else {
		msg.delete({ timeout: 3000 });
		msg.channel.send('Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
	const data = fs.readFileSync(path);
	const rouletteArray = JSON.parse(data);
	const wordInArray = rouletteArray.indexOf(textString);
	if (wordInArray === -1) {
		rouletteArray.push(textString);
		fs.writeFileSync(path, JSON.stringify(rouletteArray, null, 2));
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
	name: 'addWordRoulette',
	description: 'Adding new word to JSON Array (Roulette)',
	execute(msg, fileChooser, textString) {
		addWordRoulette(msg, fileChooser, textString);
	},
};
