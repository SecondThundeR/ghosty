const fs = require('fs');
const { Client, Collection, Intents } = require('discord.js');
const dotenv = require('dotenv');

// Gets all ENV variables from .env file
dotenv.config();

const client = new Client({
    intents: [
        Intents.FLAGS.GUILDS,
    ]
});

client.commands = new Collection();
const commandFiles = fs.readdirSync('./src/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./src/commands/${file}`);
    client.commands.set(command.data.name, command);
}

client.once('ready', () => {
    console.log(`Bot is ready! Logged in as ${client.user.tag}`);
})

client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    const command = client.commands.get(interaction.commandName);

    if (!command) return;

    try {
        await command.execute(interaction);
    }
    catch (error) {
        console.error(error);
        return interaction.reply({
            content: 'There was an error while executing this command!',
            ephemeral: true
        });
    }
});

client.login(process.env.TOKEN);
