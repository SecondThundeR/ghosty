'use strict';
const sharedVars = require('../data/variables');

function resultsReset(msg, command) {
	if (command === 'шип') {
		if (sharedVars.vars.shipInActive === false) {
			sharedVars.vars.shipDate = '';
			sharedVars.vars.shipTextShort = '';
			sharedVars.vars.shipTextFull = '';
			sharedVars.vars.shipActivated = false;
			sendWarningMessage(msg, 0);
		}
	}
	else if (command === 'хуископ') {
		if (sharedVars.vars.goroInActive === false) {
			sharedVars.vars.goroDate = '';
			sharedVars.vars.goroTextShort = '';
			sharedVars.vars.goroTextFull = '';
			sharedVars.vars.goroActivated = false;
			sendWarningMessage(msg, 1);
		}
	}
	else if (command === 'гей') {
		if (sharedVars.vars.animeInActive === false) {
			sharedVars.vars.gayDate = '';
			sharedVars.vars.gayText = '';
			sharedVars.vars.gayActivated = false;
			sendWarningMessage(msg, 2);
		}
	}
	else if (command === 'аниме') {
		if (sharedVars.vars.animeInActive === false) {
			sharedVars.vars.animeDate = '';
			sharedVars.vars.animeText = '';
			sharedVars.vars.animeActivated = false;
			sendWarningMessage(msg, 3);
		}
	}
	else if (command === 'алина') {
		if (sharedVars.vars.alinaInActive === false) {
			sharedVars.vars.alinaDate = '';
			sharedVars.vars.alinaText = '';
			sharedVars.vars.alinaActivated = false;
			sendWarningMessage(msg, 4);
		}
	}
	else {
		return;
	}
}

function sendWarningMessage(msg, i) {
	msg.delete({ timeout: 3000 });
	msg.channel.send(sharedVars.text.infoMessages[i])
		.then(msg => {
			msg.delete({ timeout: 3000 });
		});
}

module.exports = {
	name: 'resultsReset',
	description: 'Resetting some function results',
	execute(msg, command) {
		resultsReset(msg, command);
	},
};
