function gayChecker(msg, args) {
	const gayPercent = Math.floor(Math.random() * 101);

	if (typeof args === 'boolean') {
		if (gayPercent === 0) {
			const msgText = `${msg.author} сегодня не гей`;
			msg.channel.send(msgText);
		}
		else if (gayPercent === 100) {
			const msgText = `${msg.author} тобой бы гордился ♂Dungeon Master♂!\nТы на ${gayPercent}% гей!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${msg.author} на ${gayPercent}% гей!`;
			msg.channel.send(msgText);
		}
	}
	else if (typeof args !== 'boolean') {
		if (gayPercent === 0) {
			const msgText = `${args[1]} сегодня не гей!`;
			msg.channel.send(msgText);
		}
		else if (gayPercent === 100) {
			const msgText = `${args[1]} тобой бы гордился ♂Dungeon Master♂!\nТы на ${gayPercent}% гей!`;
			msg.channel.send(msgText);
		}
		else {
			const msgText = `${args[1]} на ${gayPercent}% гей!`;
			msg.channel.send(msgText);
		}
	}
	else {
		return;
	}
}

module.exports = {
	name: 'gayChecker',
	description: 'Is user a gay?',
	cooldown: 3,
	execute(msg, args) {
		gayChecker(msg, args);
	},
};
