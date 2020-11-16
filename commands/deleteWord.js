'use strict';
const fs = require('fs');

function deleteWord(msg, args) {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const wordsArray = JSON.parse(data);
	const wordInArray = wordsArray.indexOf(args);
	if (wordInArray !== -1) {
		wordsArray.splice(wordInArray, 1);
		fs.writeFileSync('./jsonArrays/array.json', JSON.stringify(wordsArray, null, 2));
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
		deleteWord(msg, args);
	},
};
