'use strict';
const JSONLib = require('./JSONHandlerLib');
const botIDs = JSONLib.getBotIDsArray();

async function getRandomUser(msg, mode = 'typical') {
	switch (mode) {
	case 'typical': {
		const users = await msg.guild.members.fetch({ force: true });
		const usersArray = [ ...users.keys() ];
		deleteBotsFromArray(usersArray);
		const randomUser = Math.floor(Math.random() * usersArray.length);
		const randomUserInfo = await msg.guild.members.fetch(usersArray[randomUser]);
		const randomUsername = randomUserInfo.displayName;
		return [ randomUserInfo, randomUsername ];
	}
	case 'shipping': {
		const users = await msg.guild.members.fetch({ force: true });
		const usersArray = [ ...users.keys() ];
		deleteBotsFromArray(usersArray);
		const firstRandomUser = Math.floor(Math.random() * usersArray.length);
		const firstRandomUserInfo = await msg.guild.members.fetch(usersArray[firstRandomUser]);
		usersArray.splice(firstRandomUser, 1);
		const secondRandomUser = Math.floor(Math.random() * usersArray.length);
		const secondRandomUserInfo = await msg.guild.members.fetch(usersArray[secondRandomUser]);
		const firstShipUsername = firstRandomUserInfo.displayName;
		const secondShipUsername = secondRandomUserInfo.displayName;
		const finalShipname = firstShipUsername.slice(0, firstShipUsername.length / 2) + secondShipUsername.slice(secondShipUsername.length / 2, secondShipUsername.length);
		return [ firstRandomUserInfo, secondRandomUserInfo, firstShipUsername, secondShipUsername, finalShipname ];
	}
	default:
		return;
	}
}

function deleteBotsFromArray(usersID) {
	for (let i = 0; i < botIDs.length; i++) {
		const botInUsers = usersID.indexOf(botIDs[i]);
		if (botInUsers !== -1) {
			usersID.splice(botInUsers, 1);
		}
		else {
			continue;
		}
	}
	return;
}

module.exports = getRandomUser;
