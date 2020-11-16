/* eslint-disable no-shadow */
'use strict';
const sharedVars = require('../data/variables');

function shippingSkip(msg) {
	if (sharedVars.vars.shipInActive === false) {
		sharedVars.vars.shipDate = '';
		sharedVars.vars.shipTextShort = '';
		sharedVars.vars.shipTextFull = '';
		sharedVars.vars.shipActivated = false;
		msg.delete({ timeout: 3000 });
		msg.channel.send('Результаты шиппинга сброшены!')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'shippingReset',
	description: 'Resetting shipping results',
	execute(msg) {
		shippingSkip(msg);
	},
};
