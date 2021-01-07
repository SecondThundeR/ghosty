'use strict';
const sharedVars = require('../data/variables');
const getRandomUser = require('../libs/getRandomUser');
const getNextDay = require('../libs/getNextDay');
const getDayString = require('../libs/getDayString');
const initRunMessages = require('../libs/initRunMessages');
const delayTime = 1500;
const deleteTime = 5000;

function shipChooser(msg, args) {
	if (args[0] === 'скип') {
		shipSkip(msg);
	}
	else {
		switch (args.length) {
		case 1:
			return;
		case 2:
			customShipping(msg, args);
			return;
		default:
			randomShipping(msg);
			return;
		}
	}
}

async function randomShipping(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.shipActivated === false && sharedVars.vars.shipInActive === false) {
		sharedVars.vars.shipInActive = sharedVars.vars.shipActivated = true;
		sharedVars.vars.shipDate = getNextDay();
		const userInfo = await getRandomUser(msg, 'shipping');
		sharedVars.vars.firstRandomUserInfo = userInfo[0];
		sharedVars.vars.secondRandomUserInfo = userInfo[1];
		sharedVars.vars.firstUsername = userInfo[2];
		sharedVars.vars.secondUsername = userInfo[3];
		sharedVars.vars.finalShipname = userInfo[4];
		sharedVars.vars.shipTextShort = `${sharedVars.vars.firstRandomUserInfo} + ${sharedVars.vars.secondRandomUserInfo}`;
		sharedVars.vars.shipTextFull = `${sharedVars.vars.firstUsername} + ${sharedVars.vars.secondUsername}, #${sharedVars.vars.finalShipname}`;
		await initRunMessages(msg, sharedVars.vars.shipTextShort, sharedVars.text.shipFirstRunArray);
		sharedVars.vars.shipInActive = false;
		return;
	}
	else if (sharedVars.vars.shipInActive === true) {
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate < sharedVars.vars.shipDate) {
		const nextDateStr = getDayString(sharedVars.vars.shipDate);
		msg.channel.send(`${sharedVars.text.shipSendPart1}${sharedVars.vars.shipTextFull}${sharedVars.text.shipSendPart2}${nextDateStr}`);
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate > sharedVars.vars.shipDate) {
		sharedVars.vars.shipActivated = false;
		await randomShipping(msg);
	}
	else {
		return;
	}
}

async function customShipping(msg, args) {
	let firstUser, secondUser;
	if (args[0].startsWith('<@&') || args[1].startsWith('<@&')) {
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.warnBotShipping)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
		return;
	}
	else {
		if (args[0].startsWith('<@!')) {
			const firstRandomUserInfo = await msg.guild.members.fetch(args[0].slice(3).slice(0, -1));
			firstUser = firstRandomUserInfo.displayName;
		}
		else {
			firstUser = args[0];
		}
		if (args[1].startsWith('<@!')) {
			const secondRandomUserInfo = await msg.guild.members.fetch(args[1].slice(3).slice(0, -1));
			secondUser = secondRandomUserInfo.displayName;
		}
		else {
			secondUser = args[1];
		}
	}
	const firstUsernamePart = firstUser.slice(0, firstUser.length / 2);
	const secondUsernamePart = secondUser.slice(secondUser.length / 2, secondUser.length);
	const finalName = firstUsernamePart + secondUsernamePart;
	msg.channel.send(`${sharedVars.text.customShippingMessage} **${finalName}!**`);
	return;
}

function shipSkip(msg) {
	sharedVars.vars.shipDate = '';
	sharedVars.vars.shipTextShort = '';
	sharedVars.vars.shipTextFull = '';
	sharedVars.randomUserInfoGoro = '',
	sharedVars.randomUsernameGoro = '',
	sharedVars.vars.shipActivated = false;
	msg.delete({ timeout: deleteTime });
	msg.channel.send(sharedVars.text.shipInfoMessage)
		.then(msg => {
			msg.delete({ timeout: deleteTime });
		});
}

module.exports = {
	name: 'randomShip',
	description: 'TODO',
	execute(msg, args) {
		shipChooser(msg, args);
	},
};
