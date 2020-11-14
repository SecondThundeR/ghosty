/* eslint-disable no-shadow */
const sharedVars = require('../data/variables');

function goroscopeSkip(msg) {
	sharedVars.vars.goroDate = '';
	sharedVars.vars.goroTextShort = '';
	sharedVars.vars.goroTextFull = '';
	sharedVars.vars.goroActivated = false;
	msg.channel.send('Результаты гороскопа сброшены!')
		.then(msg => {
			msg.delete({ timeout: 5000 });
		});
}

module.exports = {
	name: 'goroscopeReset',
	description: 'Resetting goroscope results',
	execute(msg) {
		goroscopeSkip(msg);
	},
};
