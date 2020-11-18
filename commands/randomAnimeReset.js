'use strict';
const sharedVars = require('../data/variables');

function randomAnimeReset(msg) {
	if (sharedVars.vars.animeInActive === false) {
		sharedVars.vars.animeDate = '';
		sharedVars.vars.animeText = '';
		sharedVars.vars.animeActivated = false;
		msg.delete({ timeout: 3000 });
		msg.channel.send('Результаты анимешницы дня сброшены! *(И наверное сама анимешница тоже сброшена..., только тсс!)*')
			.then(msg => {
				msg.delete({ timeout: 3000 });
			});
	}
}

module.exports = {
	name: 'randomAnimeReset',
	description: 'Resetting anime girl of the day results',
	execute(msg) {
		randomAnimeReset(msg);
	},
};
