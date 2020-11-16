const { msgTime, botIDs } = require('../data/arrays');
const sharedVars = require('../data/variables');

async function randomAnime(msg) {
	const currentDate = new Date();

	if (sharedVars.vars.animeActivated === false && sharedVars.vars.animeInActive === false) {
		sharedVars.vars.animeInActive = true;
		sharedVars.vars.animeActivated = true;
		sharedVars.vars.animeDate = new Date();
		sharedVars.vars.animeDate.setDate(sharedVars.vars.animeDate.getDate() + 1);
		sharedVars.vars.animeDate.setHours(0, 0, 0, 0);
		await animeGetUsers(msg);
		const animePercent = Math.floor(Math.random() * 101);
		if (animePercent === 100) {
			sharedVars.vars.animeText = `${sharedVars.vars.randomUserInfoAnime} анимешница на %!\nТы настоящая кошкодевочка!`;
		}
		else if (animePercent === 0) {
			sharedVars.vars.animeText = `${sharedVars.vars.randomUserInfoAnime} анимешница на ${animePercent}%!\nПохоже ты не смотрел SAO и Токийский гуль...`;
		}
		else {
			sharedVars.vars.animeText = `${sharedVars.vars.randomUserInfoAnime} анимешница на ${animePercent}%!`;
		}
		await animeFirstRun(msg, sharedVars.vars.animeText);
		sharedVars.vars.animeInActive = false;
	}
	else if (sharedVars.vars.animeInActive === true) {
		return;
	}
	else if (sharedVars.vars.animeActivated === true && currentDate < sharedVars.vars.animeDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.animeText + '\n\n*Следующяя проверка будет доступна ' + animeNextDay() + ' в 00:00*');
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
	const botInAnimeArray1 = sharedVars.vars.usersArrayAnime.indexOf(botIDs[0]);
	if (botInAnimeArray1 !== -1) {
		sharedVars.vars.usersArrayAnime.splice(botInAnimeArray1, 1);
	}
	const botInAnimeArray2 = sharedVars.vars.usersArrayAnime.indexOf(botIDs[1]);
	if (botInAnimeArray2 !== -1) {
		sharedVars.vars.usersArrayAnime.splice(botInAnimeArray2, 1);
	}
	const botInAnimeArray3 = sharedVars.vars.usersArrayAnime.indexOf(botIDs[2]);
	if (botInAnimeArray3 !== -1) {
		sharedVars.vars.usersArrayAnime.splice(botInAnimeArray3, 1);
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
	const animeDayString = sharedVars.vars.animeDate.toString();
	let animeDayText = '';

	if (animeDayString.includes('Mon') === true) {
		animeDayText = 'в Понедельник';
		return animeDayText;
	}
	else if (animeDayString.includes('Tue') === true) {
		animeDayText = 'во Вторник';
		return animeDayText;
	}
	else if (animeDayString.includes('Wed') === true) {
		animeDayText = 'в Среду';
		return animeDayText;
	}
	else if (animeDayString.includes('Thu') === true) {
		animeDayText = 'в Четверг';
		return animeDayText;
	}
	else if (animeDayString.includes('Fri') === true) {
		animeDayText = 'в Пятницу';
		return animeDayText;
	}
	else if (animeDayString.includes('Sat') === true) {
		animeDayText = 'в Субботу';
		return animeDayText;
	}
	else if (animeDayString.includes('Sun') === true) {
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
