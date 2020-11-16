/* eslint-disable no-shadow */
'use strict';
const fs = require('fs');

function deleteBot(msg, args) {
	const data = fs.readFileSync('./jsonArrays/botIDs.json');
	const botIDsArray = JSON.parse(data);
	const botInArray = botIDsArray.indexOf(args);
	if (botInArray !== -1) {
		botIDsArray.splice(botInArray, 1);
		fs.writeFileSync('./jsonArrays/botIDs.json', JSON.stringify(botIDsArray, null, 2));
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

module.exports = {
	name: 'deleteBot',
	description: 'Deleting bot from JSON Array',
	execute(msg, args) {
		deleteBot(msg, args);
	},
};
