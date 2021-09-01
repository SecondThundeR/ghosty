const fs = require('fs');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const dotenv = require('dotenv');

// Gets all ENV variables from .env file
dotenv.config();

const commands = [];
const commandFiles = fs.readdirSync('./src/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./src/commands/${file}`);
    commands.push(command.data.toJSON());
}

const rest = new REST({ version: '9' }).setToken(process.env.TOKEN);

(async () => {
    try {
        await rest.put(
            // Line below is using global commands, instead of guild commands for dev purposes
            // Routes.applicationCommands(process.env.CLIENT_ID),

            // Line below is using guild commands to quickly check and test commands without waiting
            // for updating global commands
            Routes.applicationGuildCommands(process.env.CLIENT_ID, process.env.GUILD_ID),
            { body: commands },
        );
        console.log('Successfully registered application commands.');
    } catch (error) {
        console.error(error);
    }
})();
