'use strict';
const sharedVars = require('../data/variables');

function spamChecker(msg) {
	switch (true) {
	case sharedVars.vars.spammerCount >= 3 && sharedVars.vars.spammerID === msg.author.id:
		return true;
	case sharedVars.vars.spammerCount < 3 && sharedVars.vars.spammerID === msg.author.id:
		sharedVars.vars.spammerCount++;
		return false;
	default:
		sharedVars.vars.spammerID = msg.author.id;
		sharedVars.vars.spammerCount = 1;
		return false;
	}
}

module.exports = spamChecker;
