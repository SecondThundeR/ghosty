const { msgTime, botIDs } = require('../data/arrays');
const sharedVars = require('../data/variables');

async function randomGay(msg) {
	const currentDate = new Date();

	if (sharedVars.vars.gayActivated === false && sharedVars.vars.gayInActive === false) {
		sharedVars.vars.gayInActive = true;
		sharedVars.vars.gayActivated = true;
		sharedVars.vars.gayDate = new Date();
		sharedVars.vars.gayDate.setDate(sharedVars.vars.gayDate.getDate() + 1);
		sharedVars.vars.gayDate.setHours(0, 0, 0, 0);
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
	const botInGayArray1 = sharedVars.vars.usersArrayGay.indexOf(botIDs[0]);
	if (botInGayArray1 !== -1) {
		sharedVars.vars.usersArrayGay.splice(botInGayArray1, 1);
	}
	const botInGayArray2 = sharedVars.vars.usersArrayGay.indexOf(botIDs[1]);
	if (botInGayArray2 !== -1) {
		sharedVars.vars.usersArrayGay.splice(botInGayArray2, 1);
	}
	const botInGayArray3 = sharedVars.vars.usersArrayGay.indexOf(botIDs[2]);
	if (botInGayArray3 !== -1) {
		sharedVars.vars.usersArrayGay.splice(botInGayArray3, 1);
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
	const gayDayString = sharedVars.vars.gayDate.toString();
	let gayDayText = '';

	if (gayDayString.includes('Mon') === true) {
		gayDayText = 'в Понедельник';
		return gayDayText;
	}
	else if (gayDayString.includes('Tue') === true) {
		gayDayText = 'во Вторник';
		return gayDayText;
	}
	else if (gayDayString.includes('Wed') === true) {
		gayDayText = 'в Среду';
		return gayDayText;
	}
	else if (gayDayString.includes('Thu') === true) {
		gayDayText = 'в Четверг';
		return gayDayText;
	}
	else if (gayDayString.includes('Fri') === true) {
		gayDayText = 'в Пятницу';
		return gayDayText;
	}
	else if (gayDayString.includes('Sat') === true) {
		gayDayText = 'в Субботу';
		return gayDayText;
	}
	else if (gayDayString.includes('Sun') === true) {
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
