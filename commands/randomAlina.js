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

async function randomAlina(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));
	getJSONContents();

	if (sharedVars.vars.alinaActivated === false && sharedVars.vars.alinaInActive === false) {
		sharedVars.vars.alinaInActive = true;
		sharedVars.vars.alinaActivated = true;
		sharedVars.vars.alinaDate = new Date();
		sharedVars.vars.alinaDate.setDate(sharedVars.vars.alinaDate.getDate() + 1);
		sharedVars.vars.alinaDate.setHours(0, 0, 0, 0);
		sharedVars.vars.alinaDate = Math.round(sharedVars.vars.alinaDate / 1000 + (3 * 60 * 60));
		await alinaGetUsers(msg);
		const alinaPercent = Math.floor(Math.random() * 101);
		if (alinaPercent === 100) {
			sharedVars.vars.alinaText = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!\nНе пора ли разлогинится?`;
		}
		else if (alinaPercent === 0) {
			sharedVars.vars.alinaText = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!\nМог бы постараться немного...`;
		}
		else {
			sharedVars.vars.alinaText = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!`;
		}
		await alinaFirstRun(msg, sharedVars.vars.alinaText);
		sharedVars.vars.alinaInActive = false;
	}
	else if (sharedVars.vars.alinaInActive === true) {
		return;
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate < sharedVars.vars.alinaDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.alinaText + '\n\n*Следующяя проверка будет доступна ' + alinaNextDay() + ' в 00:00*');
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate > sharedVars.vars.alinaDate) {
		sharedVars.vars.alinaActivated = false;
		await randomAlina(msg);
	}
}

async function alinaGetUsers(msg) {
	sharedVars.vars.usersAlina = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayAlina = [ ...sharedVars.vars.usersAlina.keys() ];
	alinaDeleteBots();
	sharedVars.vars.randomUserAlina = Math.floor(Math.random() * sharedVars.vars.usersArrayAlina.length);
	sharedVars.vars.randomUserInfoAlina = await msg.guild.members.fetch(sharedVars.vars.usersArrayAlina[sharedVars.vars.randomUserAlina]);
	sharedVars.vars.randomUsernameAlina = sharedVars.vars.randomUserInfoAlina.displayName;
}

function alinaDeleteBots() {
	for (let i = 0; i < botIDs.length; i++) {
		const botInAlinaArray = sharedVars.vars.usersArrayAlina.indexOf(botIDs[i]);
		if (botInAlinaArray !== -1) {
			sharedVars.vars.usersArrayAlina.splice(botInAlinaArray, 1);
		}
		else {
			continue;
		}
	}
}

async function alinaFirstRun(msg, text) {
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const randomTime4 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];
	const currTime4 = msgTime[randomTime4];

	msg.channel.send('*Загадочность удивляет...*');
	await new Promise(r => setTimeout(r, currTime1));
	msg.channel.send('*Но что-то в ней точно есть...*');
	await new Promise(r => setTimeout(r, currTime2));
	msg.channel.send('*А что же в ней есть?...*');
	await new Promise(r => setTimeout(r, currTime3));
	msg.channel.send('*Сейчас я вам и поведаю...*');
	await new Promise(r => setTimeout(r, currTime4));
	msg.channel.send('**Cегодня: **' + text);
}

function alinaNextDay() {
	const alinaDayString = new Date(sharedVars.vars.alinaDate * 1000);
	let alinaDayText = '';

	if (alinaDayString.toUTCString().includes('Mon') === true) {
		alinaDayText = 'в Понедельник';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Tue') === true) {
		alinaDayText = 'во Вторник';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Wed') === true) {
		alinaDayText = 'в Среду';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Thu') === true) {
		alinaDayText = 'в Четверг';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Fri') === true) {
		alinaDayText = 'в Пятницу';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Sat') === true) {
		alinaDayText = 'в Субботу';
		return alinaDayText;
	}
	else if (alinaDayString.toUTCString().includes('Sun') === true) {
		alinaDayText = 'в Воскресенье';
		return alinaDayText;
	}
}

module.exports = {
	name: 'randomAlina',
	description: 'Choosing random alina girl of the day',
	execute(msg) {
		randomAlina(msg);
	},
};
