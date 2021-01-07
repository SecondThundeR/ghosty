'use strict';
const delayTime = 1500;

async function initRunMessages(msg, text, firstRunArray) {
	msg.channel.send(firstRunArray[0]);
	await new Promise(r => setTimeout(r, delayTime));
	msg.channel.send(firstRunArray[1]);
	await new Promise(r => setTimeout(r, delayTime));
	msg.channel.send(firstRunArray[2]);
	await new Promise(r => setTimeout(r, delayTime));
	msg.channel.send(firstRunArray[3]);
	await new Promise(r => setTimeout(r, delayTime));
	msg.channel.send(firstRunArray[4] + text);
	return;
}

module.exports = initRunMessages;
