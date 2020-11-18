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

async function randomAnime(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));
	getJSONContents();

	if (sharedVars.vars.animeActivated === false && sharedVars.vars.animeInActive === false) {
		sharedVars.vars.animeInActive = true;
		sharedVars.vars.animeActivated = true;
		sharedVars.vars.animeDate = new Date();
		sharedVars.vars.animeDate.setDate(sharedVars.vars.animeDate.getDate() + 1);
		sharedVars.vars.animeDate.setHours(0, 0, 0, 0);
		sharedVars.vars.animeDate = Math.round(sharedVars.vars.animeDate / 1000 + (3 * 60 * 60));
		await animeGetUsers(msg);
		const animePercent = Math.floor(Math.random() * 101);
		if (animePercent === 100) {
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime} анимешница на ${animePercent}%!`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime} анимешница на ${animePercent}%!\nТы настоящая кошкодевочка!`;
		}
		else if (animePercent === 0) {
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime} анимешница на ${animePercent}%!`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime} анимешница на ${animePercent}%!\nПохоже ты не смотрел SAO и Токийский гуль...`;
		}
		else {
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime} анимешница на ${animePercent}%!`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime} анимешница на ${animePercent}%!`;
		}
		await animeFirstRun(msg, sharedVars.vars.animeTextFull);
		sharedVars.vars.animeInActive = false;
	}
	else if (sharedVars.vars.animeInActive === true) {
		return;
	}
	else if (sharedVars.vars.animeActivated === true && currentDate < sharedVars.vars.animeDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.animeTextShort + '\n\n*Следующяя проверка будет доступна ' + animeNextDay() + ' в 00:00*');
	}
	else if (sharedVars.vars.animeActivated === true && currentDate > sharedVars.vars.animeDate) {
		sharedVars.vars.animeActivated = false;
		await randomAnime(msg);
	}
}

async function animeGetUsers(msg) {
	sharedVars.vars.usersAnime = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayAnime = [ ...sharedVars.vars.usersAnime.keys() ];
	animeDeleteBots();
	sharedVars.vars.randomUserAnime = Math.floor(Math.random() * sharedVars.vars.usersArrayAnime.length);
	sharedVars.vars.randomUserInfoAnime = await msg.guild.members.fetch(sharedVars.vars.usersArrayAnime[sharedVars.vars.randomUserAnime]);
	sharedVars.vars.randomUsernameAnime = sharedVars.vars.randomUserInfoAnime.displayName;
}

function animeDeleteBots() {
	for (let i = 0; i < botIDs.length; i++) {
		const botInAnimeArray = sharedVars.vars.usersArrayAnime.indexOf(botIDs[i]);
		if (botInAnimeArray !== -1) {
			sharedVars.vars.usersArrayAnime.splice(botInAnimeArray, 1);
		}
		else {
			continue;
		}
	}
}

async function animeFirstRun(msg, text) {
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const randomTime4 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];
	const currTime4 = msgTime[randomTime4];

	msg.channel.send('*Ищу тесты на анимешницу...*');
	await new Promise(r => setTimeout(r, currTime1));
	msg.channel.send('*Вбиваю кого-то из нас...*');
	await new Promise(r => setTimeout(r, currTime2));
	msg.channel.send('*Получаю результаты...*');
	await new Promise(r => setTimeout(r, currTime3));
	msg.channel.send('*И вот что мы получаем сегодня...*');
	await new Promise(r => setTimeout(r, currTime4));
	msg.channel.send('**Cегодня: **' + text);
}

function animeNextDay() {
	const animeDayString = new Date(sharedVars.vars.animeDate * 1000);
	let animeDayText = '';

	if (animeDayString.toUTCString().includes('Mon') === true) {
		animeDayText = 'в Понедельник';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Tue') === true) {
		animeDayText = 'во Вторник';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Wed') === true) {
		animeDayText = 'в Среду';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Thu') === true) {
		animeDayText = 'в Четверг';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Fri') === true) {
		animeDayText = 'в Пятницу';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Sat') === true) {
		animeDayText = 'в Субботу';
		return animeDayText;
	}
	else if (animeDayString.toUTCString().includes('Sun') === true) {
		animeDayText = 'в Воскресенье';
		return animeDayText;
	}
}

module.exports = {
	name: 'randomAnime',
	description: 'Choosing random anime girl of the day',
	execute(msg) {
		randomAnime(msg);
	},
};
