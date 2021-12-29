const fs = require('fs');
const cron = require('node-cron');
const { Client, Collection, Intents } = require('discord.js');
const dotenv = require('dotenv');
const { getRandomAvatar } = require('./src/utils/avatarUtils');

dotenv.config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS] });

const eventFiles = fs.readdirSync('./src/events').filter(file => file.endsWith('.js'));

client.commands = new Collection();
const commandFiles = fs.readdirSync('./src/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./src/commands/${file}`);
    client.commands.set(command.data.name, command);
}

cron.schedule('0 */3 * * *', async () => {
    const randomAvatar = await getRandomAvatar();
    if (randomAvatar !== null) {
        client.user.setAvatar(randomAvatar);
    }
});

for (const file of eventFiles) {
    const event = require(`./src/events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
    }
    else {
        client.on(event.name, (...args) => event.execute(...args));
    }
}

client.login(process.env.TOKEN);
