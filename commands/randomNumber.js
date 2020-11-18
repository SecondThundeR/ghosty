function randomNumber(msg, args) {
	const numCount = Number(args[0]);
	const randomNumber = Math.floor(Math.random() * numCount) + 1;
	msg.channel.send(`Рандомное число от 0 до ${numCount}: **${randomNumber}**`);
}

module.exports = {
	name: 'randomNumber',
	description: 'Returns random number',
	cooldown: 2,
	execute(msg, args) {
		randomNumber(msg, args);
	},
};
