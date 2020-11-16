'use strict';
const fs = require('fs');

function deleteWordRoulette(msg, fileChooser, textString) {
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
	if (wordInArray !== -1) {
		rouletteArray.splice(wordInArray, 1);
		fs.writeFileSync(path, JSON.stringify(rouletteArray, null, 2));
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
	name: 'deleteWordRoulette',
	description: 'Deleting old word from JSON Array (Roulette)',
	execute(msg, fileChooser, textString) {
		deleteWordRoulette(msg, fileChooser, textString);
	},
};
