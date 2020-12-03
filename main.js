'use strict';
const fs = require('fs');
const Discord = require('discord.js');
const express = require('express');
const JSONLib = require('./libs/JSONHandlerLib');
const sharedVars = require('./data/variables');
const { token } = require('./config.json');
const wakeUpDyno = require('./wakeDyno');

const PORT = 3000;
const DYNO_URL = 'https://appname.herokuapp.com';
const commandsAliases = JSONLib.getCommandsNames();

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
	case commandsAliases[0]:
		client.commands.get('getRandomWordFromArray').execute(msg, args);
		break;
	case commandsAliases[1]:
	case commandsAliases[2]:
		switch (args[0]) {
		case 'скип':
			client.commands.get('resultsReset').execute(msg, command);
			break;
		default:
			client.commands.get('getRandomThing').execute(msg, args, command);
			break;
		}
		break;
	case commandsAliases[3]:
		client.commands.get('russianRoulette').execute(msg, args);
		break;
	case commandsAliases[4]:
		client.commands.get('getRandomThing').execute(msg, args, command);
		break;
	case commandsAliases[5]:
		client.commands.get('meMessage').execute(msg, args);
		break;
	case commandsAliases[6]:
	case commandsAliases[7]:
	case commandsAliases[8]:
	case commandsAliases[9]:
		if (!args.length) {
			return;
		}
		else {
			switch(args[0]) {
			case 'тест':
				client.commands.get('userChecker').execute(msg, args, command);
				break;
			case 'дня':
				client.commands.get('getRandomThing').execute(msg, args, command);
				break;
			case 'скип':
				client.commands.get('resultsReset').execute(msg, command);
				break;
			}
		}
		break;
	case commandsAliases[10]:
		if (!args.length) {
			break;
		}
		else {
			client.commands.get('createPoll').execute(msg, args);
		}
		break;
	case commandsAliases[11]:
		client.commands.get('getHelp').execute(msg);
		break;
	case commandsAliases[12]:
		client.commands.get('getUptime').execute(msg);
		break;
	default:
		break;
	}
});

client.login(token);
