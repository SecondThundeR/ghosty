'use strict';
const sharedVars = require('../data/variables');

function getDayString(currentDate) {
	const currentDayString = new Date(currentDate * 1000);

	if (currentDayString.toUTCString().includes('Mon') === true) {
		return sharedVars.text.mondayText;
	}
	else if (currentDayString.toUTCString().includes('Tue') === true) {
		return sharedVars.text.tuesdayText;
	}
	else if (currentDayString.toUTCString().includes('Wed') === true) {
		return sharedVars.text.wednesdayText;
	}
	else if (currentDayString.toUTCString().includes('Thu') === true) {
		return sharedVars.text.thursdayText;
	}
	else if (currentDayString.toUTCString().includes('Fri') === true) {
		return sharedVars.text.fridayText;
	}
	else if (currentDayString.toUTCString().includes('Sat') === true) {
		return sharedVars.text.saturdayText;
	}
	else if (currentDayString.toUTCString().includes('Sun') === true) {
		return sharedVars.text.sundayText;
	}
	else {
		return;
	}
}

module.exports = getDayString;
