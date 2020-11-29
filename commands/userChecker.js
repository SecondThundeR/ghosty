'use strict';
function checkerSelector(msg, args, command) {
	if (command === 'гей') {
		gayChecker(msg, args);
	}
	else if (command === 'аниме') {
		animeChecker(msg, args);
	}
	else if (command === 'алина') {
		alinaChecker(msg, args);
	}
	else {
		return;
	}
}

function gayChecker(msg, args) {
	const gayPercent = Math.floor(Math.random() * 101);

	if (args.length === 1) {
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
	else if (args.length === 2) {
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

function animeChecker(msg, args) {
	const animePercent = Math.floor(Math.random() * 101);

	if (args.length === 1) {
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
	else if (args.length === 2) {
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

function alinaChecker(msg, args) {
	const alinaPercent = Math.floor(Math.random() * 101);

	if (args.length === 1) {
		if (alinaPercent === 0) {
			const msgText = `${msg.author} сегодня не Алина :c`;
			msg.channel.send(msgText);
			return;
		}
		else if (alinaPercent === 100) {
			const msgText = `${msg.author} разлогинься!\nТы Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
			return;
		}
		else {
			const msgText = `${msg.author} Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
			return;
		}
	}
	else if (args.length === 2) {
		if (alinaPercent === 0) {
			const msgText = `${args[1]} сегодня не Алина :c`;
			msg.channel.send(msgText);
			return;
		}
		else if (alinaPercent === 100) {
			const msgText = `${args[1]} разлогинься!\nТы Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
			return;
		}
		else {
			const msgText = `${args[1]} Алина на ${alinaPercent}%!`;
			msg.channel.send(msgText);
			return;
		}
	}
	else {
		return;
	}
}

module.exports = {
	name: 'userChecker',
	description: 'Checking users for certain criteria',
	cooldown: 3,
	execute(msg, args, command) {
		checkerSelector(msg, args, command);
	},
};
