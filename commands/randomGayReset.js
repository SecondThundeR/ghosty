'use strict';
const sharedVars = require('../data/variables');

function randomGayReset(msg) {
	if (sharedVars.vars.animeInActive === false) {
		sharedVars.vars.gayDate = '';
		sharedVars.vars.gayText = '';
		sharedVars.vars.gayActivated = false;
		msg.delete({ timeout: 3000 });
		msg.channel.send('Результаты гея дня сброшены! *(А что же случилось с геем?...)*')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'randomGayReset',
	description: 'Resetting gay of the day results',
	execute(msg) {
		randomGayReset(msg);
	},
};
