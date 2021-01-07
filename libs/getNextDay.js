'use strict';
function getNextDay() {
	const newDate = new Date();
	newDate.setDate(newDate.getDate() + 1);
	newDate.setHours(0, 0, 0, 0);
	return Math.round(newDate / 1000 + (3 * 60 * 60));
}

module.exports = getNextDay;
