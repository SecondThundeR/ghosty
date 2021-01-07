'use strict';
function meMessage(msg, args) {
	msg.delete();
	if (args[0] === 'анон' && args.length > 1) {
		args.shift();
		const textString = args.join(' ');
		msg.channel.send(textString);
		return;
	}
	else if (args[0] === 'анонттс' && args.length > 1) {
		args.shift();
		const textString = args.join(' ');
		msg.channel.send(textString, { tts: true });
		return;
	}
	else if (args[0] !== 'анон' && args.length > 0) {
		const textString = args.join(' ');
		msg.channel.send(`${msg.author} ${textString}`);
		return;
	}
}

module.exports = {
	name: 'meMessage',
	description: 'Module reproduces famous command /me',
	cooldown: 2,
	execute(msg, args) {
		meMessage(msg, args);
	},
};
