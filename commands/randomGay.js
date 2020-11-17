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

async function randomGay(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));
	getJSONContents();

	if (sharedVars.vars.gayActivated === false && sharedVars.vars.gayInActive === false) {
		sharedVars.vars.gayInActive = true;
		sharedVars.vars.gayActivated = true;
		sharedVars.vars.gayDate = new Date();
		sharedVars.vars.gayDate.setDate(sharedVars.vars.gayDate.getDate() + 1);
		sharedVars.vars.gayDate.setHours(0, 0, 0, 0);
		sharedVars.vars.gayDate = Math.round(sharedVars.vars.gayDate / 1000 + (3 * 60 * 60));
		await gayGetUsers(msg);
		const gayPercent = Math.floor(Math.random() * 101);
		if (gayPercent === 100) {
			sharedVars.vars.gayText = `${sharedVars.vars.randomUserInfoGay} гей на %!\nГотов ли он служить ♂Dungeon Master'у♂?`;
		}
		else if (gayPercent === 0) {
			sharedVars.vars.gayText = `${sharedVars.vars.randomUserInfoGay} гей на ${gayPercent}%!\nНеужели он не настоящий ♂Fucking Slave♂?`;
		}
		else {
			sharedVars.vars.gayText = `${sharedVars.vars.randomUserInfoGay} гей на ${gayPercent}%!`;
		}
		await gayFirstRun(msg, sharedVars.vars.gayText);
		sharedVars.vars.gayInActive = false;
	}
	else if (sharedVars.vars.gayInActive === true) {
		return;
	}
	else if (sharedVars.vars.gayActivated === true && currentDate < sharedVars.vars.gayDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.gayText + '\n\n*Следующяя проверка будет доступна ' + gayNextDay() + ' в 00:00*');
	}
	else if (sharedVars.vars.gayActivated === true && currentDate > sharedVars.vars.gayDate) {
		sharedVars.vars.gayActivated = false;
		await randomGay(msg);
	}
}

async function gayGetUsers(msg) {
	sharedVars.vars.usersGay = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayGay = [ ...sharedVars.vars.usersGay.keys() ];
	gayDeleteBots();
	sharedVars.vars.randomUserGay = Math.floor(Math.random() * sharedVars.vars.usersArrayGay.length);
	sharedVars.vars.randomUserInfoGay = await msg.guild.members.fetch(sharedVars.vars.usersArrayGay[sharedVars.vars.randomUserGay]);
	sharedVars.vars.randomUsernameGay = sharedVars.vars.randomUserInfoGay.displayName;
}

function gayDeleteBots() {
	for (let i = 0; i < botIDs.length; i++) {
		const botInGayArray = sharedVars.vars.usersArrayGay.indexOf(botIDs[i]);
		if (botInGayArray !== -1) {
			sharedVars.vars.usersArrayGay.splice(botInGayArray, 1);
		}
		else {
			continue;
		}
	}
}

async function gayFirstRun(msg, text) {
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const randomTime4 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];
	const currTime4 = msgTime[randomTime4];

	msg.channel.send('*Захожу в* ♂**Gay Party**♂');
	await new Promise(r => setTimeout(r, currTime1));
	msg.channel.send('*Ищу* ♂**Dungeon Master**♂');
	await new Promise(r => setTimeout(r, currTime2));
	msg.channel.send('*Зову нашего* ♂**Fucking Slave**♂');
	await new Promise(r => setTimeout(r, currTime3));
	msg.channel.send('*Говорю ему* ♂**Welcome to the club, buddy**♂');
	await new Promise(r => setTimeout(r, currTime4));
	msg.channel.send('**Cегодня: **' + text);
}

function gayNextDay() {
	const gayDayString = new Date(sharedVars.vars.gayDate * 1000);
	let gayDayText = '';

	if (gayDayString.toUTCString().includes('Mon') === true) {
		gayDayText = 'в Понедельник';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Tue') === true) {
		gayDayText = 'во Вторник';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Wed') === true) {
		gayDayText = 'в Среду';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Thu') === true) {
		gayDayText = 'в Четверг';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Fri') === true) {
		gayDayText = 'в Пятницу';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Sat') === true) {
		gayDayText = 'в Субботу';
		return gayDayText;
	}
	else if (gayDayString.toUTCString().includes('Sun') === true) {
		gayDayText = 'в Воскресенье';
		return gayDayText;
	}
}

module.exports = {
	name: 'randomGay',
	description: 'Choosing random gay of the day',
	execute(msg) {
		randomGay(msg);
	},
};
