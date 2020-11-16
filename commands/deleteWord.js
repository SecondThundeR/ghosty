/* eslint-disable no-shadow */
const fs = require('fs');

function deleteWord(msg, textString) {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const convertedData = JSON.parse(data);
	const wordInArray = convertedData.indexOf(textString);
	if (wordInArray !== -1) {
		convertedData.splice(wordInArray, 1);
		fs.writeFileSync('./jsonArrays/array.json', JSON.stringify(convertedData, null, 2));
		msg.delete({ timeout: 4000 });
		msg.channel.send('Я удалил это слово у себя. Неужели кто-то очищает меня от этого...')
			.then(msg => {
				msg.delete({ timeout: 4000 });
			});
	}
	else {
		msg.delete({ timeout: 4000 });
		msg.channel.send('Прости, я не нашёл это слово у себя и мне нечего удалять')
			.then(msg => {
				msg.delete({ timeout: 4000 });
			});
	}
}

module.exports = {
	name: 'deleteWord',
	description: 'Deleting old word from JSON Array',
	execute(msg, textString) {
		deleteWord(msg, textString);
	},
};
