/* eslint-disable no-shadow */
const sharedVars = require('../data/variables');

function goroscopeSkip(msg) {
	if (sharedVars.vars.goroInActive === false) {
		sharedVars.vars.goroDate = '';
		sharedVars.vars.goroTextShort = '';
		sharedVars.vars.goroTextFull = '';
		sharedVars.vars.goroActivated = false;
		msg.delete({ timeout: 3000 });
		msg.channel.send('Результаты гороскопа сброшены!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'goroscopeReset',
	description: 'Resetting goroscope results',
	execute(msg) {
		goroscopeSkip(msg);
	},
};
