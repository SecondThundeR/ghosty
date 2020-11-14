'use strict';
const fs = require('fs');
const Discord = require('discord.js');
const express = require('express');
const wakeUpDyno = require('./wakeDyno');
const { token } = require('./config.json');
const PORT = 3000;
const DYNO_URL = 'https://fuckin-slave.herokuapp.com';
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
	console.log(`Logged in as ${client.user.tag}!`);
	client.user.setActivity('Dungeon Master Simulator')
		.then(() => console.log('Activity has been set successfully'));
});

client.on('message', msg => {
	if (msg.author.bot) {
		return;
	}

	const args = msg.content.trim().split(/ +/);
	const command = args.shift().toLowerCase();

	if (command === 'ху' || command === 'who') {
		client.commands.get('randomCringe').execute(msg);
	}
	else if (command === 'whoiscope') {
		if (!args.length) {
			client.commands.get('randomGoroscope').execute(msg);
		}
		else if (args[0] === 'reset') {
			client.commands.get('goroscopeReset').execute(msg);
		}
	}
	else if (command === 'шип') {
		if (!args.length) {
			client.commands.get('randomShipping').execute(msg);
		}
		else if (args[0] === 'сброс') {
			client.commands.get('shippingReset').execute(msg);
		}
	}
	else if (command === 'add') {
		if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length) {
			const textString = args.join(' ');
			client.commands.get('addWord').execute(msg, textString);
		}
	}
	else if (command === 'delete') {
		if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length) {
			const textString = args.join(' ');
			client.commands.get('deleteWord').execute(msg, textString);
		}
	}
	else if (command === 'рулетка') {
		if (!args.length) {
			const bulletCount = 1;
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
		else if (args.length) {
			const bulletCount = args[0];
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
	}
});

client.login(token).then(() => console.log);
