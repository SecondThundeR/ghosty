'use strict';
const sharedVars = require('../data/variables');

function resultsReset(msg, command) {
	if (command === 'шип') {
		if (sharedVars.vars.shipInActive === false) {
			sharedVars.vars.shipDate = '';
			sharedVars.vars.shipTextShort = '';
			sharedVars.vars.shipTextFull = '';
			sharedVars.randomUserInfoGoro = '',
			sharedVars.randomUsernameGoro = '',
			sharedVars.vars.shipActivated = false;
			sendWarningMessage(msg, 0);
		}
	}
	else if (command === 'хуископ') {
		if (sharedVars.vars.goroInActive === false) {
			sharedVars.vars.goroDate = '';
			sharedVars.vars.goroTextShort = '';
			sharedVars.vars.goroTextFull = '';
			sharedVars.vars.firstRandomUserInfo = '',
			sharedVars.vars.secondRandomUserInfo = '',
			sharedVars.vars.firstUsername = '',
			sharedVars.vars.secondUsername = '',
			sharedVars.vars.finalShipname = '',
			sharedVars.vars.goroActivated = false;
			sendWarningMessage(msg, 1);
		}
	}
	else if (command === 'гей') {
		if (sharedVars.vars.animeInActive === false) {
			sharedVars.vars.gayDate = '';
			sharedVars.vars.gayTextShort = '';
			sharedVars.vars.gayTextFull = '';
			sharedVars.randomUserInfoGay = '',
			sharedVars.randomUsernameGay = '',
			sharedVars.vars.gayActivated = false;
			sendWarningMessage(msg, 2);
		}
	}
	else if (command === 'аниме') {
		if (sharedVars.vars.animeInActive === false) {
			sharedVars.vars.animeDate = '';
			sharedVars.vars.animeTextFull = '';
			sharedVars.vars.animeTextShort = '';
			sharedVars.randomUserInfoAnime = '',
			sharedVars.randomUsernameAnime = '',
			sharedVars.vars.animeActivated = false;
			sendWarningMessage(msg, 3);
		}
	}
	else if (command === 'алина') {
		if (sharedVars.vars.alinaInActive === false) {
			sharedVars.vars.alinaDate = '';
			sharedVars.vars.alinaTextShort = '';
			sharedVars.vars.alinaTextFull = '';
			sharedVars.randomUserInfoAlina = '',
			sharedVars.randomUsernameAlina = '',
			sharedVars.vars.alinaActivated = false;
			sendWarningMessage(msg, 4);
		}
	}
	else if (command === 'влад') {
		if (sharedVars.vars.vladInActive === false) {
			sharedVars.vars.vladDate = '';
			sharedVars.vars.vladTextShort = '';
			sharedVars.vars.vladTextFull = '';
			sharedVars.randomUserInfoVlad = '',
			sharedVars.randomUsernameVlad = '',
			sharedVars.vars.vladActivated = false;
			sendWarningMessage(msg, 5);
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
	description: 'Module resets the results of the function that the user has selected',
	execute(msg, command) {
		resultsReset(msg, command);
	},
};
