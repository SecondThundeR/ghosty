/* eslint-disable no-shadow */
const fs = require('fs');

function addWord(msg, textString) {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const cringeArray = JSON.parse(data);
	cringeArray.push(textString);
	fs.writeFileSync('./jsonArrays/array.json', JSON.stringify(cringeArray, null, 2));
	msg.channel.send('Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(')
		.then(msg => {
			msg.delete({ timeout: 5000 });
		});
}

module.exports = {
	name: 'addWord',
	description: 'Adding new word to JSON Array',
	execute(msg, textString) {
		addWord(msg, textString);
	},
};
