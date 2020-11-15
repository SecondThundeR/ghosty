const fs = require('fs');
const { msgTime, botIDs } = require('../data/arrays');
const sharedVars = require('../data/variables');

async function getJSONContents() {
	const data = fs.readFileSync('./jsonArrays/array.json');
	const convertedData = JSON.parse(data);
	return convertedData;
}

async function randomGoroscope(msg) {
	const currentDate = new Date();

	if (sharedVars.vars.goroActivated === false && sharedVars.vars.goroInActive === false) {
		sharedVars.vars.goroInActive = true;
		sharedVars.vars.goroActivated = true;
		sharedVars.vars.goroDate = new Date();
		sharedVars.vars.goroDate.setDate(sharedVars.vars.goroDate.getDate() + 1);
		sharedVars.vars.goroDate.setHours(0, 0, 0, 0);
		await goroGetUsers(msg);
		const whoiscopeArray = await getJSONContents();
		const randomWord = Math.floor(Math.random() * whoiscopeArray.length);
		sharedVars.vars.goroTextShort = `${sharedVars.vars.randomUserInfoGoro}` + ' - ' + whoiscopeArray[randomWord];
		sharedVars.vars.goroTextFull = `${sharedVars.vars.randomUsernameGoro}` + ' - ' + whoiscopeArray[randomWord];
		await goroscopeFirstRun(msg, sharedVars.vars.goroTextShort);
		sharedVars.vars.goroInActive = false;
	}
	else if (sharedVars.vars.goroInActive === true) {
		return;
	}
	else if (sharedVars.vars.goroActivated === true && currentDate < sharedVars.vars.goroDate) {
		msg.channel.send('**Гороскоп дня на сегодня: **' + sharedVars.vars.goroTextFull + '\n\n*Следующее предсказание будет доступно ' + goroscopeNextDay() + ' в 00:00*');
	}
	else if (sharedVars.vars.goroActivated === true && currentDate > sharedVars.vars.goroDate) {
		sharedVars.vars.goroActivated = false;
		await randomGoroscope(msg);
	}
}

async function goroGetUsers(msg) {
	sharedVars.vars.usersGoro = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayGoro = [ ...sharedVars.vars.usersGoro.keys() ];
	goroDeleteBots();
	sharedVars.vars.randomUserGoro = Math.floor(Math.random() * sharedVars.vars.usersArrayGoro.length);
	sharedVars.vars.randomUserInfoGoro = await msg.guild.members.fetch(sharedVars.vars.usersArrayGoro[sharedVars.vars.randomUserGoro]);
	sharedVars.vars.randomUsernameGoro = sharedVars.vars.randomUserInfoGoro.displayName;
}

function goroDeleteBots() {
	const botInGoroArray1 = sharedVars.vars.usersArrayGoro.indexOf(botIDs[0]);
	if (botInGoroArray1 !== -1) {
		sharedVars.vars.usersArrayGoro.splice(botInGoroArray1, 1);
	}
	const botInGoroArray2 = sharedVars.vars.usersArrayGoro.indexOf(botIDs[1]);
	if (botInGoroArray2 !== -1) {
		sharedVars.vars.usersArrayGoro.splice(botInGoroArray2, 1);
	}
	const botInGoroArray3 = sharedVars.vars.usersArrayGoro.indexOf(botIDs[2]);
	if (botInGoroArray3 !== -1) {
		sharedVars.vars.usersArrayGoro.splice(botInGoroArray3, 1);
	}
}

async function goroscopeFirstRun(msg, text) {
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const randomTime4 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];
	const currTime4 = msgTime[randomTime4];

	msg.channel.send('*Заглядываю в будущее...*');
	await new Promise(r => setTimeout(r, currTime1));
	msg.channel.send('*Анализирую прошлое...*');
	await new Promise(r => setTimeout(r, currTime2));
	msg.channel.send('*Живу настоящим...*');
	await new Promise(r => setTimeout(r, currTime3));
	msg.channel.send('*Что же мы получаем сегодня?*');
	await new Promise(r => setTimeout(r, currTime4));
	msg.channel.send('**Гороскоп дня на сегодня: **' + text);
}

function goroscopeNextDay() {
	const goroDayString = sharedVars.vars.goroDate.toString();
	let goroDayText = '';

	if (goroDayString.includes('Mon') === true) {
		goroDayText = 'в Понедельник';
		return goroDayText;
	}
	else if (goroDayString.includes('Tue') === true) {
		goroDayText = 'во Вторник';
		return goroDayText;
	}
	else if (goroDayString.includes('Wed') === true) {
		goroDayText = 'в Среду';
		return goroDayText;
	}
	else if (goroDayString.includes('Thu') === true) {
		goroDayText = 'в Четверг';
		return goroDayText;
	}
	else if (goroDayString.includes('Fri') === true) {
		goroDayText = 'в Пятницу';
		return goroDayText;
	}
	else if (goroDayString.includes('Sat') === true) {
		goroDayText = 'в Субботу';
		return goroDayText;
	}
	else if (goroDayString.includes('Sun') === true) {
		goroDayText = 'в Воскресенье';
		return goroDayText;
	}
}

module.exports = {
	name: 'randomGoroscope',
	description: 'Returns random user and random word from whoiscope array',
	execute(msg) {
		randomGoroscope(msg).then(() => console.log);
	},
};
