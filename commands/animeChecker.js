function animeChecker(msg, args) {
	const animePercent = Math.floor(Math.random() * 101);

	if (typeof args === 'boolean') {
		if (animePercent === 0) {
			const msgText = `${msg.author} сегодня не анимешница :c`;
			msg.channel.send(msgText);
		}
		else if (animePercent === 100) {
			const msgText = `${msg.author} может называть себя по праву кошкодевочкой и девочкой волшебницей!\nТы анимешница на ${animePercent}%!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${msg.author} анимешница на ${animePercent}%!`;
			msg.channel.send(msgText);
		}
	}
	else if (typeof args !== 'boolean') {
		if (animePercent === 0) {
			const msgText = `${args[1]} сегодня не анимешница :c`;
			msg.channel.send(msgText);
		}
		else if (animePercent === 100) {
			const msgText = `${args[1]} может называть себя по праву кошкодевочкой и девочкой волшебницей!\nТы анимешница на ${animePercent}%!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${args[1]} анимешница на ${animePercent}%!`;
			msg.channel.send(msgText);
		}
	}
	else {
		return;
	}
}

module.exports = {
	name: 'animeChecker',
	description: 'Is user a anime?',
	cooldown: 3,
	execute(msg, args) {
		animeChecker(msg, args);
	},
};
