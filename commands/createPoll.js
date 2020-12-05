'use strict';
const sharedVars = require('../data/variables');
let voteTime = 0;
let voter = '';

function getVoteResult(collectedArr, voteMsg) {
	let rArray, pArray, nArray, pObj, nObj, pValue, nValue;
	const collectedArray = Array.from(collectedArr.entries());
	if (collectedArray.length === 0) {
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.noVotesText}`;
	}
	else if (collectedArray.length === 1) {
		rArray = collectedArray[0];
		if (rArray[0] === '👍') {
			pObj = rArray[1];
			pValue = pObj.count - 1;
			nValue = 0;
		}
		else {
			nObj = rArray[1];
			pValue = 0;
			nValue = nObj.count - 1;
		}
	}
	else {
		pArray = collectedArray[0];
		nArray = collectedArray[1];
		pObj = pArray[1];
		nObj = nArray[1];
		pValue = pObj.count;
		nValue = nObj.count;
	}

	if (pValue > nValue) {
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.positiveResultText}`;
	}
	else if (pValue < nValue) {
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.negativeResultText}`;
	}
	else if (pValue === nValue) {
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.noWinnerText}`;
	}
}

function createPoll(msg, args) {
	if (isNaN(args[0])) {
		voteTime = 60000;
	}
	else {
		voteTime = Number(args[0]) * 1000;
		args.shift();
	}
	voter = msg.author;
	let voteMessage = args.join(' ');
	while (voteMessage.includes('*')) {
		voteMessage = voteMessage.replace(/\*/g, '');
	}
	const filter = (reaction, user) => {
		return ['👍', '👎'].includes(reaction.emoji.name) && user.id === msg.author.id;
	};
	msg.channel.send(`${sharedVars.text.pollText1}${voter}${sharedVars.text.pollText2}${voteMessage}${sharedVars.text.pollText3}${voteTime / 1000}${sharedVars.text.pollText4}`)
		.then(msg => {
			msg.react('👍');
			msg.react('👎');
			msg.awaitReactions(filter, { time: voteTime, errors: ['time'] })
				.catch(collected => {
					msg.reactions.removeAll();
					msg.edit(getVoteResult(collected, voteMessage));
				});
		});
}

module.exports = {
	name: 'createPoll',
	description: 'Module creates simple poll with two reaction buttons',
	cooldown: 5,
	execute(msg, args) {
		createPoll(msg, args);
	},
};
