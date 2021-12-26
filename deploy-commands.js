const fs = require('fs');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const dotenv = require('dotenv');

dotenv.config();

const commands = [];
const commandFiles = fs.readdirSync('./src/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`./src/commands/${file}`);
	commands.push(command.data.toJSON());
}

const rest = new REST({ version: '9' }).setToken(process.env.TOKEN);
const args = process.argv.slice(2);

(async () => {
	try {
		if (args[0] === 'global') {
			await rest.put(
				Routes.applicationCommands(process.env.CLIENT_ID),
			);
			console.log('Successfully registered global application commands.');
		}
		else {
			await rest.put(
				Routes.applicationGuildCommands(process.env.CLIENT_ID, process.env.GUILD_ID),
				{ body: commands },
			);
			console.log('Successfully registered guild application commands.');
		}
	}
	catch (error) {
		console.error(error);
	}
})();
