/*
	Imports

	Initializing modules, files and setting up variables for wakeUpDyno. Initializing Discord.Client()
*/

const Discord = require('discord.js');
const express = require('express');
const wakeUpDyno = require('./wakeDyno.js');
const config = require('./config.json');
const arrays = require('./arrays.js');
const constants = require('./constants.js');
const PORT = 3000;
const DYNO_URL = 'https://fuckin-slave.herokuapp.com';
const client = new Discord.Client();

// Importing token, arrays, variables (Constants)

const token = config.token;

const pizdec = arrays.pizdec;
const whoiscope = arrays.whoiscope;
const msgTime = arrays.msgTime;
const botIDs = arrays.botIDs;

const warningForSpam = constants.warningForSpam;
const goroCommand = constants.goroCommand;
const shipCommand = constants.shipCommand;

/*
	Prevent dyno from sleeping (Spends many free hours when idle)
*/

const app = express();
app.listen(PORT, () => {
	wakeUpDyno(DYNO_URL);
});

/*
	Variables

	Variables for noSpamWarning function
*/

// Stores ID of user, which is calling randomPizdec right now
let spammerID = 0;
// Stores the number of messages in a row from the user
let spammerCount = 0;

// Variables for randomGoroAndShipping function

// Stores the next day, after receiving the current one, at the time of the function call
let goroDate = '';
// Stores the generated goroscope text (without username)
let goroTextShort = '';
// Stores the goroscope ship text (with username)
let goroTextFull = '';
// Checking for an active horoscope
let goroActivated = false;
// Boolean for preventing calling second function
let goroInActive = false;

// Stores the next day, after receiving the current one, at the time of the function call
let shipDate = '';
// Stores the generated ship text (without shipname)
let shipTextShort = '';
// Stores the generated ship text (with shipname)
let shipTextFull = '';
// Checking for an active shipping
let shipActivated = false;
// Boolean for preventing calling second function
let shipInActive = false;

// Variables for shipping

let users = '';

let usersArray = '';

let firstRandomUser = '';
let secondRandomUser = '';

let firstRandomUserInfo = '';
let secondRandomUserInfo = '';

let firstUsername = '';
let secondUsername = '';

let firstShipnamePart = '';
let secondShipnamePart = '';

let finalShipname = '';

// Variables for shipping

let usersGoro = '';

let usersArrayGoro = '';

let randomUserGoro = '';

let randomUserInfoGoro = '';

let randomUsernameGoro = '';

/*
	Initializing randomPizdec function

	Choosing random word from 'pizdec' array and return 'text' variable for message (Also calling noSpamWarning for checking spam from user)

	(If user triggers noSpamWarning payload => returns different text)
*/

function randomPizdec(msg) {
	let warningText = noSpamWarning(msg);

	if (warningText === warningForSpam) {
		warningText = `${msg.author} ` + warningText;
		return warningText;
	}
	else {
		const randomWord = Math.floor(Math.random() * pizdec.length);
		const text = `${msg.author} ` + pizdec[randomWord];
		return text;
	}
}

/*
	Initializing noSpamWarning function

	Checking if user reaches the limit of sending multiple messages at row

	(After reaching the limit - returns a different text to send instead of the desired one in the randomPizdec function)
*/


function noSpamWarning(msg) {
	if (spammerCount >= 2 && spammerID === msg.author.id) {
		spammerCount = 0;
		return warningForSpam;
	}
	else if (spammerCount < 2 && spammerID === msg.author.id) {
		spammerCount++;
		return;
	}
	else {
		spammerID = msg.author.id;
		spammerCount = 1;
		return;
	}
}

/*
	Initializing randomGoroAndShipping function

	This function has two modes: subfunction for Goroscope command and subfunction for Shipping command

	------------------

	General function: Get current time and executed command

	------------------

	Goroscope: Get next day of currentDate => Changes mode of 'Goroscope Activated' to true => Get random name and word from 'names' array and 'whoiscope' array and merge them into 'goroText' variable => Call goroAndShippingFirstRun function


	(If 'Goroscope Activated' = true: Check for currentDate => If currentDate (in UNIX) less than goroDate, then return current goroText, otherwise set change mode of 'Goroscope Activated' to false and call randomGoroAndShipping again (Recursion))

	------------------

	Shipping: Get next day of currentDate => Changes mode of 'Shipping Activated' to true => Get two random users ID and their nicknames => Slicing first half of first username and second half of second username and merge them into one string => Setting two variables: 'shipTextShort' (For first shipping init) and 'shipTextFull' (For other shipping inits) => Call goroAndShippingFirstRun function

	(If 'Shipping Activated' = true: Check for currentDate => If currentDate (in UNIX) less than shipDate, then return current shipTextFull, otherwise set change mode of 'Shipping Activated' to false and call randomGoroAndShipping again (Recursion))
*/

async function randomGoroAndShipping(msg, command) {
	const currentDate = new Date();
	const commandText = command;

	if (commandText === goroCommand) {
		if (goroActivated === false && goroInActive === false) {
			goroInActive = true;
			goroActivated = true;
			goroDate = new Date();
			goroDate.setDate(goroDate.getDate() + 1);
			goroDate.setHours(0, 0, 0, 0);
			await goroGetUsers(msg);
			const randomWord = Math.floor(Math.random() * whoiscope.length);
			goroTextShort = `${randomUserInfoGoro}` + ' - ' + whoiscope[randomWord];
			goroTextFull = `${randomUsernameGoro}` + ' - ' + whoiscope[randomWord];
			await goroAndShippingFirstRun(msg, goroTextShort, commandText);
			goroInActive = false;
			return;
		}
		else if (goroInActive === true) {
			return;
		}
		else if (goroActivated === true && currentDate < goroDate) {
			msg.channel.send('**Гороскоп дня на сегодня: **' + goroTextFull + '\n\n*Следующее предсказание будет доступно ' + getGoroAndShipDay(command) + ' в 00:00*');
			return;
		}
		else if (goroActivated === true && currentDate > goroDate) {
			goroActivated = false;
			randomGoroAndShipping(msg, commandText);
		}
	}
	else if (commandText === shipCommand) {
		if (shipActivated === false && shipInActive === false) {
			shipInActive = true;
			shipActivated = true;
			shipDate = new Date();
			shipDate.setDate(shipDate.getDate() + 1);
			shipDate.setHours(0, 0, 0, 0);
			await shipGetUsers(msg);
			shipTextShort = `${firstRandomUserInfo}` + ' + ' + `${secondRandomUserInfo}`;
			shipTextFull = `${firstUsername}` + ' + ' + `${secondUsername}, #${finalShipname}`;
			await goroAndShippingFirstRun(msg, shipTextShort, commandText);
			shipInActive = false;
			return;
		}
		else if (shipInActive === true) {
			return;
		}
		else if (shipActivated === true && currentDate < shipDate) {
			msg.channel.send('**Парочка дня на сегодня: **' + shipTextFull + ' \:hearts:' + '\n\n*Следующий шиппинг будет доступен ' + getGoroAndShipDay(command) + ' в 00:00*');
			return;
		}
		else if (shipActivated === true && currentDate > shipDate) {
			shipActivated = false;
			randomGoroAndShipping(msg, commandText);
		}
	}
	else {
		return;
	}
}

async function goroGetUsers(msg) {
	usersGoro = await msg.guild.members.fetch({ force: true });

	usersArrayGoro = [ ...usersGoro.keys() ];

	shipDeleteBots();

	randomUserGoro = Math.floor(Math.random() * usersArrayGoro.length);

	randomUserInfoGoro = await msg.guild.members.fetch(usersArrayGoro[randomUserGoro]);

	randomUsernameGoro = randomUserInfoGoro.displayName;
}

async function shipGetUsers(msg) {
	users = await msg.guild.members.fetch({ force: true });

	usersArray = [ ...users.keys() ];

	goroDeleteBots();

	firstRandomUser = Math.floor(Math.random() * usersArray.length);
	secondRandomUser = Math.floor(Math.random() * usersArray.length);

	firstRandomUserInfo = await msg.guild.members.fetch(usersArray[firstRandomUser]);
	secondRandomUserInfo = await msg.guild.members.fetch(usersArray[secondRandomUser]);

	firstUsername = firstRandomUserInfo.displayName;
	secondUsername = secondRandomUserInfo.displayName;

	firstShipnamePart = firstUsername.slice(0, firstUsername.length / 2);
	secondShipnamePart = secondUsername.slice(secondUsername.length / 2, secondUsername.length);

	finalShipname = firstShipnamePart + secondShipnamePart;
}

function goroDeleteBots() {
	const botInArray1 = usersArrayGoro.indexOf(botIDs[0]);

	if (botInArray1 !== -1) {
		usersArrayGoro.splice(botInArray1, 1);
	}

	const botInArray2 = usersArrayGoro.indexOf(botIDs[1]);

	if (botInArray2 !== -1) {
		usersArrayGoro.splice(botInArray2, 1);
	}

	const botInArray3 = usersArrayGoro.indexOf(botIDs[2]);

	if (botInArray3 !== -1) {
		usersArrayGoro.splice(botInArray3, 1);
	}
}

function shipDeleteBots() {
	const botInArray1 = usersArray.indexOf(botIDs[0]);

	if (botInArray1 !== -1) {
		usersArray.splice(botInArray1, 1);
	}

	const botInArray2 = usersArray.indexOf(botIDs[1]);

	if (botInArray2 !== -1) {
		usersArray.splice(botInArray2, 1);
	}

	const botInArray3 = usersArray.indexOf(botIDs[2]);

	if (botInArray3 !== -1) {
		usersArray.splice(botInArray3, 1);
	}
}

/*
	Initializing goroSkip and shipSkip functions

	Resetting data in variables
*/

function goroSkip() {
	goroDate = '';
	goroTextShort = '';
	goroTextFull = '';
	goroActivated = false;
	return;
}

function shipSkip() {
	shipDate = '';
	shipTextShort = '';
	shipTextFull = '';
	shipActivated = false;
	return;
}

/*
	Initializing goroAndShippingFirstRun async function

	This function has two modes: subfunction for Goroscope command and subfunction for Shipping command

	------------------

	General function: Get current command and calculates four random timeout duration for the current function call

	------------------

	Goroscope: Sending messages and waiting for random timeout duration (Then sending last message with goroText)

	------------------

	Shipping: Sending messages and waiting for random timeout duration (Then sending last message with shipTextShort)
*/

async function goroAndShippingFirstRun(msg, text, command) {
	const commandText = command;
	const randomTime1 = Math.floor(Math.random() * msgTime.length);
	const randomTime2 = Math.floor(Math.random() * msgTime.length);
	const randomTime3 = Math.floor(Math.random() * msgTime.length);
	const randomTime4 = Math.floor(Math.random() * msgTime.length);
	const currTime1 = msgTime[randomTime1];
	const currTime2 = msgTime[randomTime2];
	const currTime3 = msgTime[randomTime3];
	const currTime4 = msgTime[randomTime4];

	if (commandText === goroCommand) {
		msg.channel.send('*Заглядываю в будущее...*');
		await new Promise(r => setTimeout(r, currTime1));
		msg.channel.send('*Анализирую прошлое...*');
		await new Promise(r => setTimeout(r, currTime2));
		msg.channel.send('*Живу настоящим...*');
		await new Promise(r => setTimeout(r, currTime3));
		msg.channel.send('*Что же мы получаем сегодня?*');
		await new Promise(r => setTimeout(r, currTime4));
		msg.channel.send('**Гороскоп дня на сегодня: **' + text);
		return;
	}
	else if (commandText === shipCommand) {
		msg.channel.send('**МОРЕ ВОЛНУЕТСЯ РАЗ**');
		await new Promise(r => setTimeout(r, currTime1));
		msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ДВА**');
		await new Promise(r => setTimeout(r, currTime2));
		msg.channel.send('**МОРЕ ВОЛНУЕТСЯ ТРИ**');
		await new Promise(r => setTimeout(r, currTime3));
		msg.channel.send('**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ **' + text + ' \:hearts:');
		return;
	}
	else {
		return;
	}
}

/*
	Initializing getGoroAndShipDay async function

	This function has two modes: subfunction for Goroscope command and subfunction for Shipping command

	------------------

	General function: Get current command

	------------------

	Goroscope: Converting current goroDate to string and initializing 'goroDayText' variable => Checking for the name of the day and writing it into a 'goroDayText' variable => returns 'goroDayText'

	------------------

	Shipping: Converting current shipDate to string and initializing 'shipDayText' variable => Checking for the name of the day and writing it into a 'shipDayText' variable => returns 'shipDayText'
*/

function getGoroAndShipDay(command) {
	const currentCommand = command;

	if (currentCommand === goroCommand) {
		const goroDayString = goroDate.toString();
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
		else {
			return;
		}
	}
	else if (currentCommand === shipCommand) {
		const shipDayString = shipDate.toString();
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
		else {
			return;
		}
	}
	else {
		return;
	}
}

/*
	Discord.js Workspace

	Ready State: Send log after successful login (Writing username of bot) => Setting 'Dungeon Master Simulator' as 'Playing...' for bot status

	------------------

	Messages State: This state has three modes: subfunction for Who command, subfunction for Goroscope command and subfunction for Shipping command

	Who: Calling randomPizdec function and pass the 'msg' argument => When function completes, sending message with recieved text from function

	Goroscope: Getting current command from message => Calling randomGoroAndShipping function and pass the 'msg' and 'commandText' argument (Triggering Goroscope subfunction)

	Shipping: Getting current command from message => Calling randomGoroAndShipping function and pass the 'msg' and 'commandText' argument (Triggering Shipping subfunction)

	------------------

	Main action after starting script: Triggering 'client.login' with token of bot for login
*/

client.on('ready', () => {
	console.log(`Logged in as ${client.user.tag}!`);
	client.user.setActivity('Dungeon Master Simulator');
});

client.on('message', msg => {
	if (msg.content.toLowerCase() === 'ху' || msg.content.toLowerCase() === 'who') {
		msg.channel.send(randomPizdec(msg));
	}
	else if (msg.content.toLowerCase() === 'whoiscope') {
		const commandText = msg.content.toLowerCase();
		randomGoroAndShipping(msg, commandText);
	}
	else if (msg.content.toLowerCase() === 'whoiscope skip') {
		goroSkip();
		msg.channel.send('Результаты гороскопа сброшены!');
	}
	else if (msg.content.toLowerCase() === 'шип') {
		const commandText = msg.content.toLowerCase();
		randomGoroAndShipping(msg, commandText);
	}
	else if (msg.content.toLowerCase() === 'шип скип') {
		shipSkip();
		msg.channel.send('Результаты шиппинга сброшены!');
	}
});

client.login(token);
