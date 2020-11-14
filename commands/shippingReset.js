/* eslint-disable no-shadow */
const sharedVars = require('../data/variables');

function shippingSkip(msg) {
	sharedVars.vars.shipDate = '';
	sharedVars.vars.shipTextShort = '';
	sharedVars.vars.shipTextFull = '';
	sharedVars.vars.shipActivated = false;
	msg.channel.send('Результаты шиппинга сброшены!')
		.then(msg => {
			msg.delete({ timeout: 5000 });
		});
}

module.exports = {
	name: 'shippingReset',
	description: 'Resetting shipping results',
	execute(msg) {
		shippingSkip(msg);
	},
};
