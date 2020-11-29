'use strict';
const JSONLib = require('../libs/JSONHandlerLib');
const sharedVars = require('../data/variables');
const utilityArray = JSONLib.getJSONUtilityData();
const whoiscopeArray = JSONLib.getJSONWordArray();
const botIDsArray = utilityArray[0];
const msgTimeArray = utilityArray[1];

function randomThingChooser(msg, args, command) {
	if (command === 'шип') {
		if (args.length === 2) {
			customShipping(msg, args);
		}
		else {
			randomShipping(msg);
		}
	}
	else if (command === 'хуископ') {
		if (args.length === 1) {
			customGoroscope(msg, args);
		}
		else {
			randomGoroscope(msg);
		}
	}
	else if (command === 'гей') {
		randomGay(msg);
	}
	else if (command === 'аниме') {
		randomAnime(msg);
	}
	else if (command === 'алина') {
		randomAlina(msg);
	}
	else if (command === 'рандом') {
		if (args.length === 2) {
			randomNumberWithRange(msg, args);
		}
		else {
			randomNumber(msg, args);
		}
	}
	else {
		return;
	}
}

function getRandomTime() {
	const randomTime = Math.floor(Math.random() * msgTimeArray.length);
	const delayTime = msgTimeArray[randomTime];
	return delayTime;
}

function randomNumber(msg, args) {
	const numCount = Number(args[0]);
	const randomNumber = Math.floor(Math.random() * numCount) + 1;
	msg.channel.send(`Рандомное число от 0 до ${numCount}: **${randomNumber}**`);
	return;
}

function randomNumberWithRange(msg, args) {
	const numCountMin = Number(args[0]);
	const numCountMax = Number(args[1]);
	const randomNumber = Math.round(Math.random() * (numCountMax - numCountMin) + numCountMin);
	msg.channel.send(`Рандомное число от ${numCountMin} до ${numCountMax}: **${randomNumber}**`);
	return;
}

async function randomGoroscope(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));

	if (sharedVars.vars.goroActivated === false && sharedVars.vars.goroInActive === false) {
		sharedVars.vars.goroInActive = true;
		sharedVars.vars.goroActivated = true;
		sharedVars.vars.goroDate = new Date();
		sharedVars.vars.goroDate.setDate(sharedVars.vars.goroDate.getDate() + 1);
		sharedVars.vars.goroDate.setHours(0, 0, 0, 0);
		sharedVars.vars.goroDate = Math.round(sharedVars.vars.goroDate / 1000 + (3 * 60 * 60));
		await goroGetUsers(msg);
		const randomWord = Math.floor(Math.random() * whoiscopeArray.length);
		sharedVars.vars.goroTextShort = `${sharedVars.vars.randomUserInfoGoro}` + ' - ' + whoiscopeArray[randomWord];
		sharedVars.vars.goroTextFull = `${sharedVars.vars.randomUsernameGoro}` + ' - ' + whoiscopeArray[randomWord];
		await firstRunMessages(msg, sharedVars.vars.goroTextShort, sharedVars.text.goroFirstRunArray);
		sharedVars.vars.goroInActive = false;
	}
	else if (sharedVars.vars.goroInActive === true) {
		return;
	}
	else if (sharedVars.vars.goroActivated === true && currentDate < sharedVars.vars.goroDate) {
		msg.channel.send('**Гороскоп дня на сегодня: **' + sharedVars.vars.goroTextFull + '\n\n*Следующее предсказание будет доступно ' + getNextDay(sharedVars.vars.goroDate));
	}
	else if (sharedVars.vars.goroActivated === true && currentDate > sharedVars.vars.goroDate) {
		sharedVars.vars.goroActivated = false;
		await randomGoroscope(msg);
	}
}

async function randomShipping(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));

	if (sharedVars.vars.shipActivated === false && sharedVars.vars.shipInActive === false) {
		sharedVars.vars.shipInActive = true;
		sharedVars.vars.shipActivated = true;
		sharedVars.vars.shipDate = new Date();
		sharedVars.vars.shipDate.setDate(sharedVars.vars.shipDate.getDate() + 1);
		sharedVars.vars.shipDate.setHours(0, 0, 0, 0);
		sharedVars.vars.shipDate = Math.round(sharedVars.vars.shipDate / 1000 + (3 * 60 * 60));
		await shipGetUsers(msg);
		sharedVars.vars.shipTextShort = `${sharedVars.vars.firstRandomShipUserInfo}` + ' + ' + `${sharedVars.vars.secondRandomShipUserInfo}`;
		sharedVars.vars.shipTextFull = `${sharedVars.vars.firstShipUsername}` + ' + ' + `${sharedVars.vars.secondShipUsername}, #${sharedVars.vars.finalShipname}`;
		await firstRunMessages(msg, sharedVars.vars.shipTextShort, sharedVars.text.shipFirstRunArray);
		sharedVars.vars.shipInActive = false;
	}
	else if (sharedVars.vars.shipInActive === true) {
		return;
	}
	else if (sharedVars.vars.shipActivated === true && currentDate < sharedVars.vars.shipDate) {
		msg.channel.send('**Парочка дня на сегодня: **' + sharedVars.vars.shipTextFull + ' \:hearts:' + '\n\n*Следующий шиппинг будет доступен ' + getNextDay(sharedVars.vars.shipDate));
	}
	else if (sharedVars.vars.shipActivated === true && currentDate > sharedVars.vars.shipDate) {
		sharedVars.vars.shipActivated = false;
		await randomShipping(msg);
	}
}

async function randomGay(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));

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
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay} гей на ${gayPercent}%!`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay} гей на ${gayPercent}%!\nГотов ли он служить ♂Dungeon Master'у♂?`;
		}
		else if (gayPercent === 0) {
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay} гей на ${gayPercent}%!`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay} гей на ${gayPercent}%!\nНеужели он не настоящий ♂Fucking Slave♂?`;
		}
		else {
			sharedVars.vars.gayTextShort = `${sharedVars.vars.randomUsernameGay} гей на ${gayPercent}%!`;
			sharedVars.vars.gayTextFull = `${sharedVars.vars.randomUserInfoGay} гей на ${gayPercent}%!`;
		}
		await firstRunMessages(msg, sharedVars.vars.gayTextFull, sharedVars.text.gayFirstRunArray);
		sharedVars.vars.gayInActive = false;
	}
	else if (sharedVars.vars.gayInActive === true) {
		return;
	}
	else if (sharedVars.vars.gayActivated === true && currentDate < sharedVars.vars.gayDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.gayTextShort + '\n\n*Следующяя проверка будет доступна ' + getNextDay(sharedVars.vars.gayDate));
	}
	else if (sharedVars.vars.gayActivated === true && currentDate > sharedVars.vars.gayDate) {
		sharedVars.vars.gayActivated = false;
		await randomGay(msg);
	}
}

async function randomAnime(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));

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
		await firstRunMessages(msg, sharedVars.vars.animeTextFull, sharedVars.text.animeFirstRunArray);
		sharedVars.vars.animeInActive = false;
	}
	else if (sharedVars.vars.animeInActive === true) {
		return;
	}
	else if (sharedVars.vars.animeActivated === true && currentDate < sharedVars.vars.animeDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.animeTextShort + '\n\n*Следующяя проверка будет доступна ' + getNextDay(sharedVars.vars.animeDate));
	}
	else if (sharedVars.vars.animeActivated === true && currentDate > sharedVars.vars.animeDate) {
		sharedVars.vars.animeActivated = false;
		await randomAnime(msg);
	}
}

async function randomAlina(msg) {
	const currentDate = Math.round(+new Date() / 1000 + (3 * 60 * 60));

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
			if (sharedVars.vars.randomUserAlinaID === sharedVars.vars.realAlinaID) {
				sharedVars.vars.alinaTextShort = `Настоящая Алина (${sharedVars.vars.randomUsernameAlina}) - Алина на ${alinaPercent}%!`;
				sharedVars.vars.alinaTextFull = `Настоящая Алина (${sharedVars.vars.randomUserInfoAlina}) - Алина на ${alinaPercent}%!\nКто-то этому удивлён?`;
			}
			else {
				sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina} Алина на ${alinaPercent}%!`;
				sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!\nНе пора ли разлогинится?`;
			}
		}
		else if (alinaPercent === 0) {
			if (sharedVars.vars.randomUserAlinaID === sharedVars.vars.realAlinaID) {
				sharedVars.vars.alinaTextShort = `Настоящая Алина (${sharedVars.vars.randomUsernameAlina}) - Алина на ${alinaPercent}%!`;
				sharedVars.vars.alinaTextFull = `Настоящая Алина (${sharedVars.vars.randomUserInfoAlina}) - Алина на ${alinaPercent}%!\nКто-то этому удивлён?`;
			}
			else {
				sharedVars.vars.alinaTextShort = `Настоящая Алина (${sharedVars.vars.randomUsernameAlina}) - Алина на ${alinaPercent}%!`;
				sharedVars.vars.alinaTextFull = `Настоящая Алина (${sharedVars.vars.randomUserInfoAlina}) - Алина на ${alinaPercent}%!\nТы точно Алина, да?`;
			}
			sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina} Алина на ${alinaPercent}%!`;
			sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!\nМог бы постараться немного...`;
		}
		if (sharedVars.vars.randomUserAlinaID === sharedVars.vars.realAlinaID) {
			sharedVars.vars.alinaTextShort = `Настоящая Алина - Алина на ${alinaPercent}%!`;
			sharedVars.vars.alinaTextFull = `Настоящая Алина - Алина на ${alinaPercent}%!`;
		}
		else {
			sharedVars.vars.alinaTextShort = `${sharedVars.vars.randomUsernameAlina} Алина на ${alinaPercent}%!`;
			sharedVars.vars.alinaTextFull = `${sharedVars.vars.randomUserInfoAlina} Алина на ${alinaPercent}%!`;
		}
		await firstRunMessages(msg, sharedVars.vars.alinaTextFull, sharedVars.text.alinaFirstRunArray);
		sharedVars.vars.alinaInActive = false;
	}
	else if (sharedVars.vars.alinaInActive === true) {
		return;
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate < sharedVars.vars.alinaDate) {
		msg.channel.send('**Cегодня: **' + sharedVars.vars.alinaTextShort + '\n\n*Следующяя проверка будет доступна ' + getNextDay(sharedVars.vars.alinaDate));
	}
	else if (sharedVars.vars.alinaActivated === true && currentDate > sharedVars.vars.alinaDate) {
		sharedVars.vars.alinaActivated = false;
		await randomAlina(msg);
	}
}

async function shipGetUsers(msg) {
	sharedVars.vars.usersShip = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayShip = [ ...sharedVars.vars.usersShip.keys() ];
	deleteBotsFromArray(sharedVars.vars.usersArrayShip);
	sharedVars.vars.firstRandomShipUser = Math.floor(Math.random() * sharedVars.vars.usersArrayShip.length);
	sharedVars.vars.secondRandomShipUser = Math.floor(Math.random() * sharedVars.vars.usersArrayShip.length);
	if (sharedVars.vars.firstRandomShipUser === sharedVars.vars.secondRandomShipUser) {
		sharedVars.vars.usersShip = '';
		sharedVars.vars.usersArrayShip = '';
		sharedVars.vars.firstRandomShipUser = '';
		sharedVars.vars.secondRandomShipUser = '';
		await shipGetUsers(msg);
	}
	else {
		sharedVars.vars.firstRandomShipUserInfo = await msg.guild.members.fetch(sharedVars.vars.usersArrayShip[sharedVars.vars.firstRandomShipUser]);
		sharedVars.vars.secondRandomShipUserInfo = await msg.guild.members.fetch(sharedVars.vars.usersArrayShip[sharedVars.vars.secondRandomShipUser]);
		sharedVars.vars.firstShipUsername = sharedVars.vars.firstRandomShipUserInfo.displayName;
		sharedVars.vars.secondShipUsername = sharedVars.vars.secondRandomShipUserInfo.displayName;
		sharedVars.vars.firstShipnamePart = sharedVars.vars.firstShipUsername.slice(0, sharedVars.vars.firstShipUsername.length / 2);
		sharedVars.vars.secondShipnamePart = sharedVars.vars.secondShipUsername.slice(sharedVars.vars.secondShipUsername.length / 2, sharedVars.vars.secondShipUsername.length);
		sharedVars.vars.finalShipname = sharedVars.vars.firstShipnamePart + sharedVars.vars.secondShipnamePart;
		return;
	}
}

async function goroGetUsers(msg) {
	sharedVars.vars.usersGoro = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayGoro = [ ...sharedVars.vars.usersGoro.keys() ];
	deleteBotsFromArray(sharedVars.vars.usersArrayGoro);
	sharedVars.vars.randomUserGoro = Math.floor(Math.random() * sharedVars.vars.usersArrayGoro.length);
	sharedVars.vars.randomUserInfoGoro = await msg.guild.members.fetch(sharedVars.vars.usersArrayGoro[sharedVars.vars.randomUserGoro]);
	sharedVars.vars.randomUsernameGoro = sharedVars.vars.randomUserInfoGoro.displayName;
}

async function gayGetUsers(msg) {
	sharedVars.vars.usersGay = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayGay = [ ...sharedVars.vars.usersGay.keys() ];
	deleteBotsFromArray(sharedVars.vars.usersArrayGay);
	sharedVars.vars.randomUserGay = Math.floor(Math.random() * sharedVars.vars.usersArrayGay.length);
	sharedVars.vars.randomUserInfoGay = await msg.guild.members.fetch(sharedVars.vars.usersArrayGay[sharedVars.vars.randomUserGay]);
	sharedVars.vars.randomUsernameGay = sharedVars.vars.randomUserInfoGay.displayName;
}

async function animeGetUsers(msg) {
	sharedVars.vars.usersAnime = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayAnime = [ ...sharedVars.vars.usersAnime.keys() ];
	deleteBotsFromArray(sharedVars.vars.usersArrayAnime);
	sharedVars.vars.randomUserAnime = Math.floor(Math.random() * sharedVars.vars.usersArrayAnime.length);
	sharedVars.vars.randomUserInfoAnime = await msg.guild.members.fetch(sharedVars.vars.usersArrayAnime[sharedVars.vars.randomUserAnime]);
	sharedVars.vars.randomUserAnimeID = sharedVars.vars.randomUserInfoAnime.id;
	sharedVars.vars.randomUsernameAnime = sharedVars.vars.randomUserInfoAnime.displayName;
}

async function alinaGetUsers(msg) {
	sharedVars.vars.usersAlina = await msg.guild.members.fetch({ force: true });
	sharedVars.vars.usersArrayAlina = [ ...sharedVars.vars.usersAlina.keys() ];
	deleteBotsFromArray(sharedVars.vars.usersArrayAlina);
	sharedVars.vars.randomUserAlina = Math.floor(Math.random() * sharedVars.vars.usersArrayAlina.length);
	sharedVars.vars.randomUserInfoAlina = await msg.guild.members.fetch(sharedVars.vars.usersArrayAlina[sharedVars.vars.randomUserAlina]);
	sharedVars.vars.randomUserAlinaID = sharedVars.vars.randomUserInfoAlina.id;
	sharedVars.vars.randomUsernameAlina = sharedVars.vars.randomUserInfoAlina.displayName;
}

function deleteBotsFromArray(usersIDArray) {
	for (let i = 0; i < botIDsArray.length; i++) {
		const botInArray = usersIDArray.indexOf(botIDsArray[i]);
		if (botInArray !== -1) {
			usersIDArray.splice(botInArray, 1);
		}
		else {
			continue;
		}
	}
	return;
}

async function firstRunMessages(msg, text, firstRunArray) {
	msg.channel.send(firstRunArray[0]);
	await new Promise(r => setTimeout(r, getRandomTime()));
	msg.channel.send(firstRunArray[1]);
	await new Promise(r => setTimeout(r, getRandomTime()));
	msg.channel.send(firstRunArray[2]);
	await new Promise(r => setTimeout(r, getRandomTime()));
	msg.channel.send(firstRunArray[3]);
	await new Promise(r => setTimeout(r, getRandomTime()));
	msg.channel.send(firstRunArray[4] + text);
}

function getNextDay(currentDate) {
	const currentDayString = new Date(currentDate * 1000);
	let newDayText = '';

	if (currentDayString.toUTCString().includes('Mon') === true) {
		newDayText = 'в Понедельник*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Tue') === true) {
		newDayText = 'во Вторник*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Wed') === true) {
		newDayText = 'в Среду*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Thu') === true) {
		newDayText = 'в Четверг*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Fri') === true) {
		newDayText = 'в Пятницу*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Sat') === true) {
		newDayText = 'в Субботу*';
		return newDayText;
	}
	else if (currentDayString.toUTCString().includes('Sun') === true) {
		newDayText = 'в Воскресенье*';
		return newDayText;
	}
}

function customShipping(msg, args) {
	const firstName = args[0];
	const secondName = args[1];
	const firstNamePart = firstName.slice(0, firstName.length / 2);
	const secondNamePart = secondName.slice(secondName.length / 2, secondName.length);
	const finalName = firstNamePart + secondNamePart;
	msg.channel.send(`Данная парочка смело бы называлась - **${finalName}!**`);
	return;
}

function customGoroscope(msg, args) {
	const choosenUser = args[0];
	if (!choosenUser.startsWith('<@!')) {
		msg.delete({ timeout: 2500 });
		msg.channel.send(sharedVars.text.warnMessageGoro)
			.then(msg => {
				msg.delete({ timeout: 2500 });
			});
		return;
	}
	else {
		const randomWord = Math.floor(Math.random() * whoiscopeArray.length);
		msg.channel.send(`Гороскоп для ${choosenUser} - **${whoiscopeArray[randomWord]}**!`);
		return;
	}
}

module.exports = {
	name: 'randomThing',
	description: 'Returns random thing',
	execute(msg, args, command) {
		randomThingChooser(msg, args, command);
	},
};
