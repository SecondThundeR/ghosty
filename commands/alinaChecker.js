'use strict';
const Discord = require('discord.js');
const alinaID = '312671116810518528';

function realAlinaChecker(msg, args) {
	const collector = new Discord.MessageCollector(msg.channel, msg => msg.author.id === alinaID, { time: 10000 });
	if (msg.author.id === alinaID) {
		msg.channel.send(`${msg.author} - ты же Алина...\nТы уверена что хочешь проверить саму себя? (Да / Нет)`);
		collector.on('collect', msg => {
			if (msg.content.toLowerCase() == 'да' && msg.author.id === alinaID) {
				collector.stop();
				alinaChecker(msg, args);
			}
			else if (msg.content.toLowerCase() == 'нет' && msg.author.id === alinaID) {
				msg.channel.send('Хорошо, проверять не будем');
				collector.stop();
				return;
			}
			else {
				msg.channel.send('Это слово я ещё не понимаю');
				collector.stop();
				return;
			}
		});
		return;
	}
	else {
		alinaChecker(msg, args);
	}
}

function alinaChecker(msg, args) {
	const alinaPercent = Math.floor(Math.random() * 101);

	if (typeof args === 'boolean') {
		if (alinaPercent === 0) {
			const msgText = `${msg.author} сегодня не Алина :c`;
			msg.channel.send(msgText);
		}
		else if (alinaPercent === 100) {
			const msgText = `${msg.author} разлогинься!\nТы Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${msg.author} Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
		}
	}
	else if (typeof args !== 'boolean') {
		if (alinaPercent === 0) {
			const msgText = `${args[1]} сегодня не Алина :c`;
			msg.channel.send(msgText);
		}
		else if (alinaPercent === 100) {
			const msgText = `${args[1]} разлогинься!\nТы Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${args[1]} Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
		}
	}
	else {
		return;
	}
}

module.exports = {
	name: 'alinaChecker',
	description: 'Is user a alina?',
	cooldown: 3,
	execute(msg, args) {
		realAlinaChecker(msg, args);
	},
};
