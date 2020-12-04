'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const botIDs = JSONLib.getBotIDsArray();
const goroscopeArray = JSONLib.getWordsArray();
const delayTime1 = 3000;
const delayTime2 = 10000;

function randomThingChooser(msg, args, command) {
	switch (command) {
	case 'шип':
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
	case 'хуископ':
		switch (args.length) {
		case 1:
			customGoroscope(msg, args);
			return;
		default:
			randomGoroscope(msg);
			return;
		}
	case 'рандом':
		randomNumber(msg, args);
		return;
	case 'гей':
		randomGay(msg);
		return;
	case 'аниме':
		randomAnime(msg);
		return;
	case 'алина':
		randomAlina(msg);
		return;
	case 'влад':
		randomVlad(msg);
		return;
	default:
		return;
	}
}

function randomNumber(msg, args) {
	let rangeNumber, randomNumberSingle, fromRangeNumber, toRangeNumber, randomNumberRange;
	switch (args.length) {
	case 1:
		rangeNumber = Number(args[0]);
		if (rangeNumber < 1) {
			msg.delete({ timeout: delayTime2 });
			msg.reply(sharedVars.text.noRangeNumberWarning)
				.then(msg => {
					msg.delete({ timeout: delayTime2 });
				});
			break;
		}
		else {
			randomNumberSingle = Math.floor(Math.random() * rangeNumber) + 1;
			msg.channel.send(`${sharedVars.text.randomNumberText} ${rangeNumber}: **${randomNumberSingle}**`);
			break;
		}
	case 2:
		fromRangeNumber = Number(args[0]);
		toRangeNumber = Number(args[1]);
		randomNumberRange = Math.round(Math.random() * (toRangeNumber - fromRangeNumber) + fromRangeNumber);
		msg.channel.send(`${sharedVars.text.randomNumberWithRangeTextPart1} ${fromRangeNumber} ${sharedVars.text.randomNumberWithRangeTextPart2} ${toRangeNumber}: **${randomNumberRange}**`);
		break;
	default:
		msg.delete({ timeout: delayTime2 });
		msg.reply(sharedVars.text.noRangeNumberWarning)
			.then(msg => {
				msg.delete({ timeout: delayTime2 });
			});
		break;
	}
}

async function randomGoroscope(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.goroActivated === false && sharedVars.vars.goroInActive === false) {
		sharedVars.vars.goroInActive = sharedVars.vars.goroActivated = true;
		sharedVars.vars.goroDate = getNextDayTime();
		const userInfo = await getUser(msg, 'typical');
		sharedVars.vars.randomUserInfoGoro = userInfo[0];
		sharedVars.vars.randomUsernameGoro = userInfo[1];
		const randomWord = Math.floor(Math.random() * goroscopeArray.length);
		sharedVars.vars.goroTextShort = `${sharedVars.vars.randomUserInfoGoro} - ${goroscopeArray[randomWord]}`;
		sharedVars.vars.goroTextFull = `${sharedVars.vars.randomUsernameGoro} - ${goroscopeArray[randomWord]}`;
		await firstRunMessages(msg, sharedVars.vars.goroTextShort, sharedVars.text.goroFirstRunArray);
		sharedVars.vars.goroInActive = false;
		return;
	}
	else if (sharedVars.vars.goroActivated === true && currentDate < sharedVars.vars.goroDate) {
		const nextDateStr = getNextDayString(sharedVars.vars.goroDate);
		msg.channel.send(`${sharedVars.text.goroSendPart1}${sharedVars.vars.goroTextFull}${sharedVars.text.goroSendPart2}${nextDateStr}`);
		return;
	}
	else if (sharedVars.vars.goroActivated === true && currentDate > sharedVars.vars.goroDate) {
		sharedVars.vars.goroActivated = false;
		await randomGoroscope(msg);
	}
	else if (sharedVars.vars.goroInActive === true) {
		return;
	}
}

async function randomShipping(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.shipActivated === false && sharedVars.vars.shipInActive === false) {
		sharedVars.vars.shipInActive = sharedVars.vars.shipActivated = true;
		sharedVars.vars.shipDate = getNextDayTime();
		const userInfo = await getUser(msg, 'shipping');
		sharedVars.vars.firstRandomUserInfo = userInfo[0];
		sharedVars.vars.secondRandomUserInfo = userInfo[1];
		sharedVars.vars.firstUsername = userInfo[2];
		sharedVars.vars.secondUsername = userInfo[3];
		sharedVars.vars.finalShipname = userInfo[4];
		sharedVars.vars.shipTextShort = `${sharedVars.vars.firstRandomUserInfo} + ${sharedVars.vars.secondRandomUserInfo}`;
		sharedVars.vars.shipTextFull = `${sharedVars.vars.firstUsername} + ${sharedVars.vars.secondUsername}, #${sharedVars.vars.finalShipname}`;
		await firstRunMessages(msg, sharedVars.vars.shipTextShort, sharedVars.text.shipFirstRunArray);
		sharedVars.vars.shipInActive = false;
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate < sharedVars.vars.shipDate) {
		const nextDateStr = getNextDayString(sharedVars.vars.shipDate);
		msg.channel.send(`${sharedVars.text.shipSendPart1}${sharedVars.vars.shipTextFull}${sharedVars.text.shipSendPart2}${nextDateStr}`);
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate > sharedVars.vars.shipDate) {
		sharedVars.vars.shipActivated = false;
		await randomShipping(msg);
	}
	else if (sharedVars.vars.shipInActive === true) {
		return;
	}
}

async function randomGay(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.gayActivated === false && sharedVars.vars.gayInActive === false) {
		sharedVars.vars.gayInActive = sharedVars.vars.gayActivated = true;
		sharedVars.vars.gayDate = getNextDayTime();
		const userInfo = await getUser(msg, 'typical');
		sharedVars.vars.randomUserInfoGay = userInfo[0];
		sharedVars.vars.randomUsernameGay = userInfo[1];
		const randomPercent = Math.floor(Math.random() * 101);
		switch (randomPercent) {
		case 0:
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.gayNoneText}`;
			break;
		case 100:
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.gayFullText}`;
			break;
		default:
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay}${sharedVars.text.gayOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			break;
		}
		await firstRunMessages(msg, sharedVars.vars.gayTextFull, sharedVars.text.gayFirstRunArray);
		sharedVars.vars.gayInActive = false;
		return;
	}
	else if (sharedVars.vars.gayActivated === true && currentDate < sharedVars.vars.gayDate) {
		const nextDayStr = getNextDayString(sharedVars.vars.gayDate);
		msg.channel.send(`${sharedVars.text.otherSendPart1}${sharedVars.vars.gayTextShort}${sharedVars.text.otherSendPart2}${nextDayStr}`);
		return;
	}
	else if (sharedVars.vars.gayActivated === true && currentDate > sharedVars.vars.gayDate) {
		sharedVars.vars.gayActivated = false;
		await randomGay(msg);
	}
	else if (sharedVars.vars.gayInActive === true) {
		return;
	}
}

async function randomAnime(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.animeActivated === false && sharedVars.vars.animeInActive === false) {
		sharedVars.vars.animeInActive = sharedVars.vars.animeActivated = true;
		sharedVars.vars.animeDate = getNextDayTime();
		const userInfo = await getUser(msg, 'typical');
		sharedVars.vars.randomUserInfoAnime = userInfo[0];
		sharedVars.vars.randomUsernameAnime = userInfo[1];
		const randomPercent = Math.floor(Math.random() * 101);
		switch (randomPercent) {
		case 0:
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime}${sharedVars.text.animeOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime}${sharedVars.text.animeOnText}${randomPercent}${sharedVars.text.animeNoneText}`;
			break;
		case 100:
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime}${sharedVars.text.animeOnText}${randomPercent}`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime}${sharedVars.text.animeOnText}${randomPercent}${sharedVars.text.animeFullText}`;
			break;
		default:
			sharedVars.vars.animeTextShort = `${sharedVars.vars.randomUsernameAnime}${sharedVars.text.animeOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.animeTextFull = `${sharedVars.vars.randomUserInfoAnime}${sharedVars.text.animeOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			break;
		}
		await firstRunMessages(msg, sharedVars.vars.animeTextFull, sharedVars.text.animeFirstRunArray);
		sharedVars.vars.animeInActive = false;
		return;
	}
	else if (sharedVars.vars.animeActivated === true && currentDate < sharedVars.vars.animeDate) {
		const nextDayStr = getNextDayString(sharedVars.vars.animeDate);
		msg.channel.send(`${sharedVars.text.otherSendPart1}${sharedVars.vars.animeTextShort}${sharedVars.text.otherSendPart2}${nextDayStr}`);
		return;
	}
	else if (sharedVars.vars.animeActivated === true && currentDate > sharedVars.vars.animeDate) {
		sharedVars.vars.animeActivated = false;
		await randomAnime(msg);
	}
	else if (sharedVars.vars.animeInActive === true) {
		return;
	}
}

async function randomAlina(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.alinaActivated === false && sharedVars.vars.alinaInActive === false) {
		sharedVars.vars.alinaInActive = sharedVars.vars.alinaActivated = true;
		sharedVars.vars.alinaDate = getNextDayTime();
		const userInfo = await getUser(msg, 'typical');
		sharedVars.vars.randomUserInfoAlina = userInfo[0];
		sharedVars.vars.randomUsernameAlina = userInfo[1];
		const randomPercent = Math.floor(Math.random() * 101);
		switch (randomPercent) {
		case 0:
			sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.alinaNoneText}`;
			break;
		case 100:
			sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.alinaFullText}`;
			break;
		default:
			sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina}${sharedVars.text.alinaOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			break;
		}
		await firstRunMessages(msg, sharedVars.vars.alinaTextFull, sharedVars.text.alinaFirstRunArray);
		sharedVars.vars.alinaInActive = false;
		return;
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate < sharedVars.vars.alinaDate) {
		const nextDayStr = getNextDayString(sharedVars.vars.alinaDate);
		msg.channel.send(`${sharedVars.text.otherSendPart1}${sharedVars.vars.alinaTextShort}${sharedVars.text.otherSendPart2}${nextDayStr}`);
		return;
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate > sharedVars.vars.alinaDate) {
		sharedVars.vars.alinaActivated = false;
		await randomAlina(msg);
	}
	else if (sharedVars.vars.alinaInActive === true) {
		return;
	}
}

async function randomVlad(msg) {
	const currentDate = Math.round(new Date() / 1000 + (3 * 60 * 60));
	if (sharedVars.vars.vladActivated === false && sharedVars.vars.vladInActive === false) {
		sharedVars.vars.vladInActive = sharedVars.vars.vladActivated = true;
		sharedVars.vars.vladDate = getNextDayTime();
		const userInfo = await getUser(msg, 'typical');
		sharedVars.vars.randomUserInfoVlad = userInfo[0];
		sharedVars.vars.randomUsernameVlad = userInfo[1];
		const randomPercent = Math.floor(Math.random() * 101);
		switch (randomPercent) {
		case 0:
			sharedVars.vars.vladTextShort = `${sharedVars.vars.randomUsernameVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.vladTextFull = `${sharedVars.vars.randomUserInfoVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.vladNoneText}`;
			break;
		case 100:
			sharedVars.vars.vladTextShort = `${sharedVars.vars.randomUsernameVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.vladTextFull = `${sharedVars.vars.randomUserInfoVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.vladFullText}`;
			break;
		default:
			sharedVars.vars.vladTextShort = `${sharedVars.vars.randomUsernameVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			sharedVars.vars.vladTextFull = `${sharedVars.vars.randomUserInfoVlad}${sharedVars.text.vladOnText}${randomPercent}${sharedVars.text.otherDefaultText}`;
			break;
		}
		await firstRunMessages(msg, sharedVars.vars.vladTextFull, sharedVars.text.vladFirstRunArray);
		sharedVars.vars.vladInActive = false;
		return;
	}
	else if (sharedVars.vars.vladActivated === true && currentDate < sharedVars.vars.vladDate) {
		const nextDayStr = getNextDayString(sharedVars.vars.vladDate);
		msg.channel.send(`${sharedVars.text.otherSendPart1}${sharedVars.vars.vladTextShort}${sharedVars.text.otherSendPart2}${nextDayStr}`);
		return;
	}
	else if (sharedVars.vars.vladActivated === true && currentDate > sharedVars.vars.vladDate) {
		sharedVars.vars.vladActivated = false;
		await randomVlad(msg);
	}
	else if (sharedVars.vars.vladInActive === true) {
		return;
	}
}

function getNextDayTime() {
	const newDate = new Date();
	newDate.setDate(newDate.getDate() + 1);
	newDate.setHours(0, 0, 0, 0);
	return Math.round(newDate / 1000 + (3 * 60 * 60));
}

async function getUser(msg, mode) {
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

async function firstRunMessages(msg, text, firstRunArray) {
	msg.channel.send(firstRunArray[0]);
	await new Promise(r => setTimeout(r, delayTime1));
	msg.channel.send(firstRunArray[1]);
	await new Promise(r => setTimeout(r, delayTime1));
	msg.channel.send(firstRunArray[2]);
	await new Promise(r => setTimeout(r, delayTime1));
	msg.channel.send(firstRunArray[3]);
	await new Promise(r => setTimeout(r, delayTime1));
	msg.channel.send(firstRunArray[4] + text);
	return;
}

function getNextDayString(currentDate) {
	const currentDayString = new Date(currentDate * 1000);

	if (currentDayString.toUTCString().includes('Mon') === true) {
		return sharedVars.text.mondayText;
	}
	else if (currentDayString.toUTCString().includes('Tue') === true) {
		return sharedVars.text.tuesdayText;
	}
	else if (currentDayString.toUTCString().includes('Wed') === true) {
		return sharedVars.text.wednesdayText;
	}
	else if (currentDayString.toUTCString().includes('Thu') === true) {
		return sharedVars.text.thursdayText;
	}
	else if (currentDayString.toUTCString().includes('Fri') === true) {
		return sharedVars.text.fridayText;
	}
	else if (currentDayString.toUTCString().includes('Sat') === true) {
		return sharedVars.text.saturdayText;
	}
	else if (currentDayString.toUTCString().includes('Sun') === true) {
		return sharedVars.text.sundayText;
	}
	else {
		return;
	}
}

function customShipping(msg, args) {
	const firstUser = args[0];
	const secondUser = args[1];
	const firstUsernamePart = firstUser.slice(0, firstUser.length / 2);
	const secondUsernamePart = secondUser.slice(secondUser.length / 2, secondUser.length);
	const finalName = firstUsernamePart + secondUsernamePart;
	msg.channel.send(`${sharedVars.text.customShippingMessage} **${finalName}!**`);
	return;
}

function customGoroscope(msg, args) {
	const goroUser = args[0];
	if (!goroUser.startsWith('<@!')) {
		msg.delete({ timeout: 2500 });
		msg.channel.send(sharedVars.text.warnMessageGoro)
			.then(msg => {
				msg.delete({ timeout: 2500 });
			});
		return;
	}
	else {
		const randomWord = Math.floor(Math.random() * goroscopeArray.length);
		msg.channel.send(`${sharedVars.text.customGoroscopeMessage} ${goroUser} - **${goroscopeArray[randomWord]}**!`);
		return;
	}
}

module.exports = {
	name: 'getRandomThing',
	description: 'Module handles multiple commands, which depends on random (Getting random users, words, etc.)',
	execute(msg, args, command) {
		randomThingChooser(msg, args, command);
	},
};
