'use strict';
const fs = require('fs');
const Discord = require('discord.js');
const { token } = require('./config.json');
const client = new Discord.Client();
client.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	client.commands.set(command.name, command);
}

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

	switch (command) {
	case 'ху':
	case 'who':
		if (msg.author.id === '663283391365644309') {
			return;
		}
		else {
			client.commands.get('randomCringe').execute(msg);
		}
		break;
	case 'whoiscope':
		if (!args.length) {
			client.commands.get('randomGoroscope').execute(msg);
		}
		else if (args[0] === 'reset' && msg.author.id !== '663283391365644309') {
			client.commands.get('goroscopeReset').execute(msg);
		}
		break;
	case 'шип':
		if (!args.length) {
			const isCustom = false;
			client.commands.get('randomShipping').execute(msg, args, isCustom);
		}
		else if (args[0] === 'скип' && msg.author.id !== '663283391365644309') {
			client.commands.get('shippingReset').execute(msg);
		}
		else if (args[0] !== 'скип' && args.length === 2) {
			const isCustom = true;
			client.commands.get('randomShipping').execute(msg, args, isCustom);
		}
		else if (args.length === 1) {
			return;
		}
		break;
	case 'add':
		if (msg.author.id === '663283391365644309') {
			return;
		}
		else if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length) {
			const textString = args.join(' ');
			client.commands.get('addWord').execute(msg, textString);
		}
		break;
	case 'delete':
		if (msg.author.id === '663283391365644309') {
			return;
		}
		else if (!args.length) {
			return msg.channel.send(`${msg.author} чел... введи может что-нибудь`);
		}
		else if (args.length) {
			const textString = args.join(' ');
			client.commands.get('deleteWord').execute(msg, textString);
		}
		break;
	case 'рулетка':
		if (!args.length) {
			const bulletCount = 1;
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
		else if (args.length) {
			const bulletCount = args[0];
			client.commands.get('russianRoulette').execute(msg, bulletCount);
		}
		break;
	case 'uptime':
		client.commands.get('uptime').execute(msg);
		break;
	case 'йа':
		if (!args.length) {
			return;
		}
		else {
			const textString = args.join(' ');
			client.commands.get('me').execute(msg, textString);
		}
		break;
	case 'хелп':
		client.commands.get('help').execute(msg);
		break;
	case 'гей':
		if (!args.length) {
			return;
		}
		else if (args.length === 1 && args[0] === 'тест') {
			const selftest = true;
			client.commands.get('gayChecker').execute(msg, selftest);
		}
		else if (args.length === 2 && args[0] === 'тест' && typeof args[1] === 'string') {
			client.commands.get('gayChecker').execute(msg, args);
		}
		else if (args.length === 1 && args[0] === 'дня') {
			client.commands.get('randomGay').execute(msg);
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
			const selftest = true;
			client.commands.get('animeChecker').execute(msg, selftest);
		}
		else if (args.length === 2 && args[0] === 'тест' && typeof args[1] === 'string') {
			client.commands.get('animeChecker').execute(msg, args);
		}
		else {
			return;
		}
		break;
	case 'анимешница':
		if (!args.length) {
			return;
		}
		else if (args.length === 1 && args[0] === 'дня') {
			client.commands.get('randomAnime').execute(msg);
		}
		else {
			return;
		}
		break;
	case 'exit':
		client.commands.get('exit').execute(msg);
		break;
	default:
		break;
	}
});

client.login(token).then(() => console.log);
