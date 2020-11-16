/* eslint-disable no-shadow */
const fs = require('fs');

function addWord(msg, textString) {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const cringeArray = JSON.parse(data);
	const wordInArray = cringeArray.indexOf(textString);
	if (wordInArray === -1) {
		cringeArray.push(textString);
		fs.writeFileSync('./jsonArrays/array.json', JSON.stringify(cringeArray, null, 2));
		msg.delete({ timeout: 4000 });
		msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
			.then(msg => {
				msg.delete({ timeout: 4000 });
			});
	}
	else {
		msg.delete({ timeout: 4000 });
		msg.channel.send('Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего')
			.then(msg => {
				msg.delete({ timeout: 4000 });
			});
	}

}

module.exports = {
	name: 'addWord',
	description: 'Adding new word to JSON Array',
	execute(msg, textString) {
		addWord(msg, textString);
	},
};
