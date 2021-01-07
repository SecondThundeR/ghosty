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

function executeCommand(msg) {
	const args = msg.content.trim().split(/ +/);
	const customCommand = args.shift();
	const command = customCommand.toLowerCase();

	switch (command) {
	case commandsAliases[0]:
		client.commands.get('getRandomWord').execute(msg, args);
		break;
	case commandsAliases[1]:
		client.commands.get('randomShip').execute(msg, args);
		break;
	case commandsAliases[2]:
		client.commands.get('addWord').execute(msg, args);
		break;
	case commandsAliases[3]:
		client.commands.get('deleteWord').execute(msg, args);
		break;
	case commandsAliases[4]:
		client.commands.get('dedMakar').execute(msg, args, command);
		break;
	case commandsAliases[5]:
		client.commands.get('russianRoulette').execute(msg, args);
		break;
	case commandsAliases[6]:
		client.commands.get('randomNumber').execute(msg, args);
		break;
	case commandsAliases[7]:
		client.commands.get('meMessage').execute(msg, args);
		break;
	case commandsAliases[8]:
		client.commands.get('rspGame').execute(msg, args);
		break;
	case commandsAliases[9]:
		client.commands.get('createPoll').execute(msg, args);
		break;
	case commandsAliases[10]:
		client.commands.get('getHelp').execute(msg);
		break;
	case commandsAliases[11]:
		client.commands.get('getUptime').execute(msg);
		break;
	default:
		switch (args[0]) {
		case 'тест':
		case 'рандом':
			client.commands.get('userChecker').execute(msg, args, customCommand);
			break;
		default:
			break;
		}
		break;
	}
}

client.on('ready', () => {
	client.user.setActivity(sharedVars.text.activityName);
	console.log(`Successfully logged in as '${client.user.tag}'!\nSet '${sharedVars.text.activityName}' as an activity`);
});

client.on('message', msg => {
	if (msg.author.bot) {
		return;
	}
	executeCommand(msg);
});

client.login(token);
