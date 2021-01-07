'use strict';
const sharedVars = require('../data/variables');
const delayTime = 10000;
let voteTime = 60000;
let voter;

function pollInit(msg, args) {
	if (!args.length) {
		return;
	}
	else if (args.length !== 0 && sharedVars.vars.pollLocked !== true) {
		msg.delete();
		createPoll(msg, args);
	}
	else {
		msg.delete({ timeout: delayTime });
		msg.channel.send(sharedVars.text.pollIsActiveWarn)
			.then(msg => {
				msg.delete({ timeout: delayTime });
			});
	}
}

function getVoteResult(collectedArr, voteMsg) {
	const collectedArray = Array.from(collectedArr.entries());
	let pValue, nValue = 0;

	if (collectedArray.length === 0) {
		sharedVars.vars.pollLocked = false;
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.noVotesText}`;
	}
	else if (collectedArray.length === 1) {
		const rArray = collectedArray[0];

		if (rArray[0] === '👍') {
			const pObj = rArray[1];
			pValue = pObj.count - 1;
		}
		else {
			const nObj = rArray[1];
			nValue = nObj.count - 1;
		}
	}
	else {
		const pArray = collectedArray[0];
		const nArray = collectedArray[1];
		const pObj = pArray[1];
		const nObj = nArray[1];
		pValue = pObj.count - 1;
		nValue = nObj.count - 1;
	}

	if (pValue > nValue) {
		sharedVars.vars.pollLocked = false;
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.positiveResultText}`;
	}
	else if (pValue < nValue) {
		sharedVars.vars.pollLocked = false;
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.negativeResultText}`;
	}
	else if (pValue === nValue) {
		sharedVars.vars.pollLocked = false;
		return `${sharedVars.text.endPollText1}${voteMsg}${sharedVars.text.endPollText2}${voter}${sharedVars.text.noWinnerText}`;
	}
}

function createPoll(msg, args) {
	sharedVars.vars.pollLocked = true;
	let voteMessage = args.join(' ');
	voter = msg.author;

	if (!isNaN(args[0])) {
		voteTime = Number(args[0]) * 1000;
		args.shift();
	}

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
	execute(msg, args) {
		pollInit(msg, args);
	},
};
