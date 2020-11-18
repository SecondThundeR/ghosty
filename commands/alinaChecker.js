'use strict';
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
		alinaChecker(msg, args);
	},
};
