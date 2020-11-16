/* eslint-disable no-shadow */
'use strict';
const fs = require('fs');

function addBot(msg, args) {
	const data = fs.readFileSync('./jsonArrays/botIDs.json');
	const botIDsArray = JSON.parse(data);
	const botID = args[0];
	const botInArray = botIDsArray.indexOf(botID);
	if (botInArray === -1) {
		botIDsArray.push(botID);
		fs.writeFileSync('./jsonArrays/botIDs.json', JSON.stringify(botIDsArray, null, 2));
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

module.exports = {
	name: 'addBot',
	description: 'Adding new bot to JSON Array',
	execute(msg, args) {
		addBot(msg, args);
	},
};
