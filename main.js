'use strict';
const fs = require('fs');
const Discord = require('discord.js');
const express = require('express');
const wakeUpDyno = require('./wakeDyno');
const PORT = 3000;
const DYNO_URL = 'https://slavebot-ds.herokuapp.com';
const sharedVars = require('./data/variables');
const { token } = require('./config.json');

const client = new Discord.Client();
client.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	client.commands.set(command.name, command);
}

const app = express();
app.listen(PORT, () => {
	wakeUpDyno(DYNO_URL);
});

client.on('ready', () => {
	client.user.setActivity(sharedVars.text.activityName);
	console.log(`Logged in as '${client.user.tag}' and set '${sharedVars.text.activityName}' as an activity`);
});

client.on('message', msg => {
	if (msg.author.bot) {
		return;
	}

	const args = msg.content.trim().split(/ +/);
	const command = args.shift().toLowerCase();

	switch (command) {
	case 'ху':
	case 'who':
		if (!args.length) {
			client.commands.get('getRandomWord').execute(msg, args);
		}
		else if (args[0] != '' && args.length === 1) {
			client.commands.get('getRandomWord').execute(msg, args);
		}
		else {
			return;
		}
		break;
	case 'хуископ':
		if (args[0] !== 'скип') {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args[0] === 'скип') {
			client.commands.get('resultsReset').execute(msg, command);
		}
		else {
			return;
		}
		break;
	case 'шип':
		if (!args.length) {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args[0] === 'скип' && args.length === 1) {
			client.commands.get('resultsReset').execute(msg, command);
		}
		else if (args[0] !== 'скип' && args.length === 2) {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else {
			return;
		}
		break;
	case 'add':
		if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length === 1) {
			client.commands.get('addWord').execute(msg, args);
			return;
		}
		else if (args.length >= 2 && args[0] === 'bot') {
			client.commands.get('addWord').execute(msg, args);
			return;
		}
		else if (args.length >= 3 && args[0] === 'roulette') {
			client.commands.get('addWord').execute(msg, args);
			return;
		}
		break;
	case 'delete':
		if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length === 1) {
			client.commands.get('deleteWord').execute(msg, args);
			return;
		}
		else if (args.length >= 2 && args[0] === 'bot') {
			client.commands.get('deleteWord').execute(msg, args);
			return;
		}
		else if (args.length >= 3 && args[0] === 'roulette') {
			client.commands.get('deleteWord').execute(msg, args);
			return;
		}
		break;
	case 'рулетка':
		if (!args.length) {
			const bulletCount = 1;
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
		else if (args.length === 1 && args[0] !== 'ттс') {
			const bulletCount = args[0];
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
		else if (args.length === 1 && args[0] === 'ттс') {
			client.commands.get('russianRoulette').execute(msg, args);
		}
		else {
			return;
		}
		break;
	case 'йа':
		if (!args.length) {
			msg.delete({ timeout: 1000 });
			return;
		}
		else {
			const textString = args.join(' ');
			client.commands.get('me').execute(msg, textString);
		}
		break;
	case 'рандом':
		if (!args.length) {
			return;
		}
		else if (args.length === 1) {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args.length === 2) {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else {
			return;
		}
		break;
	case 'гей':
		if (!args.length) {
			return;
		}
		else if (args.length === 1 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 2 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'дня') {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'скип') {
			client.commands.get('resultsReset').execute(msg, command);
		}
		else {
			return;
		}
		break;
	case 'аниме':
		if (!args.length) {
			return;
		}
		else if (args.length === 1 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 2 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'дня') {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'скип') {
			client.commands.get('resultsReset').execute(msg, command);
		}
		else {
			return;
		}
		break;
	case 'алина':
		if (!args.length) {
			return;
		}
		else if (args.length === 1 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 2 && args[0] === 'тест') {
			client.commands.get('userChecker').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'дня') {
			client.commands.get('randomThing').execute(msg, args, command);
		}
		else if (args.length === 1 && args[0] === 'скип') {
			client.commands.get('resultsReset').execute(msg, command);
		}
		else {
			return;
		}
		break;
	case 'хелп':
		client.commands.get('help').execute(msg);
		break;
	case 'uptime':
		client.commands.get('uptime').execute(msg);
		break;
	default:
		break;
	}
});

client.login(token);
