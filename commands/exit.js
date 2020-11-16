/* eslint-disable no-shadow */
'use strict';
async function exitMessage(msg) {
	msg.delete({ timeout: 1500 });
	msg.channel.send('Завершаю процесс')
		.then(msg => {
			msg.delete({ timeout: 1500 });
		});
	await new Promise(r => setTimeout(r, 3000));
	exit();
}

function exit() {
	console.log('Exited!');
	process.exit(0);
}

module.exports = {
	name: 'exit',
	description: 'Exit process for update purpose',
	execute(msg) {
		exitMessage(msg);
	},
};
