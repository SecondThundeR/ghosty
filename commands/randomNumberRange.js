function randomNumberRange(msg, args) {
	const numCountMin = Number(args[0]);
	const numCountMax = Number(args[1]);
	const randomNumber = Math.round(Math.random() * (numCountMax - numCountMin) + numCountMin);
	msg.channel.send(`Рандомное число от ${numCountMin} до ${numCountMax}: **${randomNumber}**`);
	return;
}

module.exports = {
	name: 'randomNumberRange',
	description: 'Returns random number from selected range',
	cooldown: 2,
	execute(msg, args) {
		randomNumberRange(msg, args);
	},
};
