'use strict';
const sharedVars = require('../data/variables');

function rspModeChooser(msg, args) {
	switch (args[0]) {
	case 'бот':
		rspGameBot(msg, args);
		break;
	default:
		break;
	}
}

function rspGameBot(msg, args) {
	const randomMove = sharedVars.vars.moveVariants[Math.floor(Math.random() * sharedVars.vars.moveVariants.length)];
	const userMove = args[1].toLowerCase();
	if (randomMove === userMove) {
		msg.channel.send(`${sharedVars.text.gameDraw1}**${randomMove}**${sharedVars.text.gameDraw2}`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'ножницы') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.userWinsS}**${randomMove}**`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'бумага') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.botWinsP}**${randomMove}**`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'бумага') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.userWinsP}**${randomMove}**`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'камень') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.botWinsR}**${randomMove}**`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'камень') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.userWinsR}**${randomMove}**`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'ножницы') {
		msg.channel.send(`${sharedVars.text.defaultPart}${msg.author}${sharedVars.text.botWinsS}**${randomMove}**`);
		return;
	}
	else {
		return;
	}
}

/* function rspVariantChooserUsers(msg, args) {
	const currentUser1 = msg.author.id;
	const collector = new Discord.MessageCollector(msg.channel, msg => msg.author.id === currentUser1, { time: waitTime });
	if (msg.author.id === currentUser1) {
		msg.channel.send(`${msg.author}, теперь нужно лишь дождаться кого-то, кто захочет с вами поиграть. Другой игрок может написать прямо сейчас слово *присоединиться*, чтобы начать играть`);
		collector.on('collect', msg => {
			if (msg.content.toLowerCase() === 'присоединиться' && msg.author.id !== currentUser1) {
				const currentUser2 = msg.author.id;
				console.log(currentUser1);
				console.log(currentUser2);
				collector.stop();
				return;
			}
			else {
				msg.channel.send('Похоже, что-то пошло не так, запустите игру ещё раз');
				collector.stop();
				return;
			}
		});
		return;
	}
}

function rspGameUsers(msg, args) {
	const randomMove = moveVariants[Math.floor(Math.random() * moveVariants.length)];
	const userMove = args[0].toLowerCase();
	if (randomMove === userMove) {
		msg.channel.send(`Так как у нас обоих **${randomMove}**, то у нас ничья!`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'ножницы') {
		msg.channel.send(`Эй, ${msg.author}. Ты победил, потому что у меня были **${randomMove}**`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'бумага') {
		msg.channel.send(`Эй, ${msg.author}. А я вот победил, потому что у меня была **${randomMove}**`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'бумага') {
		msg.channel.send(`Эй, ${msg.author}. Ты победил, потому что у меня была **${randomMove}**`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'камень') {
		msg.channel.send(`Эй, ${msg.author}. А я вот победил, потому что у меня был **${randomMove}**`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'камень') {
		msg.channel.send(`Эй, ${msg.author}. Ты победил, потому что у меня был **${randomMove}**`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'ножницы') {
		msg.channel.send(`Эй, ${msg.author}. А я вот победил, потому что у меня были **${randomMove}**`);
		return;
	}
	else {
		return;
	}
} */

module.exports = {
	name: 'rspGame',
	description: 'Module handles "Rock paper scissors" game',
	cooldown: 2,
	execute(msg, args) {
		rspModeChooser(msg, args);
	},
};
