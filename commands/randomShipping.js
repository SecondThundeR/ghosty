'use strict';
const fs = require('fs');
const sharedVars = require('../data/variables');

let botIDs;
let msgTime;

function getJSONContents() {
	const botIDsData = fs.readFileSync('./jsonArrays/botIDs.json');
	const msgTimeData = fs.readFileSync('./jsonArrays/msgTime.json');
	botIDs = JSON.parse(botIDsData);
	msgTime = JSON.parse(msgTimeData);
	return;
}

async function randomShipping(msg) {
	const currentDate = new Date();
	getJSONContents();

	if (sharedVars.vars.shipActivated === false && sharedVars.vars.shipInActive === false) {
		sharedVars.vars.shipInActive = true;
		sharedVars.vars.shipActivated = true;
		sharedVars.vars.shipDate = new Date();
		sharedVars.vars.shipDate.setDate(sharedVars.vars.shipDate.getDate() + 1);
		sharedVars.vars.shipDate.setHours(0, 0, 0, 0);
		await shipGetUsers(msg);
		sharedVars.vars.shipTextShort = `${sharedVars.vars.firstRandomUserInfo}` + ' + ' + `${sharedVars.vars.secondRandomUserInfo}`;
		sharedVars.vars.shipTextFull = `${sharedVars.vars.firstUsername}` + ' + ' + `${sharedVars.vars.secondUsername}, #${sharedVars.vars.finalShipname}`;
		await shippingFirstRun(msg, sharedVars.vars.shipTextShort);
		sharedVars.vars.shipInActive = false;
	}
	else if (sharedVars.vars.shipInActive === true) {
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate < sharedVars.vars.shipDate) {
		msg.channel.send('**Парочка дня на сегодня: **' + sharedVars.vars.shipTextFull + ' \:hearts:' + '\n\n*Следующий шиппинг будет доступен ' + getShippingNextDay() + ' в 00:00*');
	}
	else if (sharedVars.vars.shipActivated === true && currentDate > sharedVars.vars.shipDate) {
		sharedVars.vars.shipActivated = false;
		await randomShipping(msg);
	}
}

async function shipGetUsers(msg) {
	sharedVars.vars.users = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArray = [ ...sharedVars.vars.users.keys() ];
	shipDeleteBots();
	sharedVars.vars.firstRandomUser = Math.floor(Math.random() * sharedVars.vars.usersArray.length);
	sharedVars.vars.secondRandomUser = Math.floor(Math.random() * sharedVars.vars.usersArray.length);
	sharedVars.vars.firstRandomUserInfo = await msg.guild.members.fetch(sharedVars.vars.usersArray[sharedVars.vars.firstRandomUser]);
	sharedVars.vars.secondRandomUserInfo = await msg.guild.members.fetch(sharedVars.vars.usersArray[sharedVars.vars.secondRandomUser]);
	sharedVars.vars.firstUsername = sharedVars.vars.firstRandomUserInfo.displayName;
	sharedVars.vars.secondUsername = sharedVars.vars.secondRandomUserInfo.displayName;
	sharedVars.vars.firstShipnamePart = sharedVars.vars.firstUsername.slice(0, sharedVars.vars.firstUsername.length / 2);
	sharedVars.vars.secondShipnamePart = sharedVars.vars.secondUsername.slice(sharedVars.vars.secondUsername.length / 2, sharedVars.vars.secondUsername.length);
	sharedVars.vars.finalShipname = sharedVars.vars.firstShipnamePart + sharedVars.vars.secondShipnamePart;
}

function shipDeleteBots() {
	for (let i = 0; i < botIDs.length; i++) {
		const botInShipArray = sharedVars.vars.usersArray.indexOf(botIDs[i]);
		if (botInShipArray !== -1) {
			sharedVars.vars.usersArray.splice(botInShipArray, 1);
		}
		else {
			continue;
		}
	}
}

async function shippingFirstRun(msg, text) {
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];

	msg.channel.send('**МОРЕ ВОЛНУЕТСЯ РАЗ**');
	await new Promise(r => setTimeout(r, currTime1));
	msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ДВА**');
	await new Promise(r => setTimeout(r, currTime2));
	msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ТРИ**');
	await new Promise(r => setTimeout(r, currTime3));
	msg.channel.send('**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ **' + text + ' \:hearts:');
}

function getShippingNextDay() {
	const shipDayString = sharedVars.vars.shipDate.toString();
	let shipDayText = '';

	if (shipDayString.includes('Mon') === true) {
		shipDayText = 'в Понедельник';
		return shipDayText;
	}
	else if (shipDayString.includes('Tue') === true) {
		shipDayText = 'во Вторник';
		return shipDayText;
	}
	else if (shipDayString.includes('Wed') === true) {
		shipDayText = 'в Среду';
		return shipDayText;
	}
	else if (shipDayString.includes('Thu') === true) {
		shipDayText = 'в Четверг';
		return shipDayText;
	}
	else if (shipDayString.includes('Fri') === true) {
		shipDayText = 'в Пятницу';
		return shipDayText;
	}
	else if (shipDayString.includes('Sat') === true) {
		shipDayText = 'в Субботу';
		return shipDayText;
	}
	else if (shipDayString.includes('Sun') === true) {
		shipDayText = 'в Воскресенье';
		return shipDayText;
	}
}

function customShipping(msg, args) {
	const firstName = args[0];
	const secondName = args[1];
	const firstNamePart = firstName.slice(0, firstName.length / 2);
	const secondNamePart = secondName.slice(secondName.length / 2, secondName.length);
	const finalName = firstNamePart + secondNamePart;
	msg.channel.send(`Данная парочка смело бы называлась - **${finalName}!**`);
}

module.exports = {
	name: 'randomShipping',
	description: 'Returns two random users',
	execute(msg, args, isCustom) {
		if (isCustom === true) {
			customShipping(msg, args);
		}
		else {
			randomShipping(msg).then(() => console.log);
		}

	},
};
