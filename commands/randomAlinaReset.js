'use strict';
const sharedVars = require('../data/variables');

function randomAlinaReset(msg) {
	if (sharedVars.vars.alinaInActive === false) {
		sharedVars.vars.alinaDate = '';
		sharedVars.vars.alinaText = '';
		sharedVars.vars.alinaActivated = false;
		msg.delete({ timeout: 3000 });
		msg.channel.send('Результаты Алины дня сброшены!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'randomAlinaReset',
	description: 'Resetting Alina of the day results',
	execute(msg) {
		randomAlinaReset(msg);
	},
};
