'use strict';
function meAnalog(msg, args) {
	msg.delete();
	msg.channel.send(`${msg.author} ${args}`);
}

module.exports = {
	name: 'me',
	description: '/me ...',
	cooldown: 2,
	execute(msg, args) {
		meAnalog(msg, args);
	},
};
