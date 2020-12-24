const moveVariants = ['камень', 'ножницы', 'бумага'];

function rspGame(msg, args) {
	const randomMove = moveVariants[Math.floor(Math.random() * moveVariants.length)];
	const userMove = args[0];
	if (randomMove === userMove) {
		msg.channel.send(`Так как у нас обоих ${randomMove}, то у нас ничья!`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'ножницы') {
		msg.channel.send(`${msg.author}! Ты победил. У меня были ${randomMove}`);
		return;
	}
	else if (userMove === 'камень' && randomMove === 'бумага') {
		msg.channel.send(`${msg.author}! Я победил. У меня была ${randomMove}`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'бумага') {
		msg.channel.send(`${msg.author}! Ты победил. У меня была ${randomMove}`);
		return;
	}
	else if (userMove === 'ножницы' && randomMove === 'камень') {
		msg.channel.send(`${msg.author}! Я победил. У меня был ${randomMove}`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'камень') {
		msg.channel.send(`${msg.author}! Ты победил. У меня был ${randomMove}`);
		return;
	}
	else if (userMove === 'бумага' && randomMove === 'ножницы') {
		msg.channel.send(`${msg.author}! Я победил. У меня были ${randomMove}`);
		return;
	}
	else {
		return;
	}
}

module.exports = {
	name: 'rspGame',
	description: 'Module handles "Rock paper scissors" game',
	cooldown: 2,
	execute(msg, args) {
		rspGame(msg, args);
	},
};
