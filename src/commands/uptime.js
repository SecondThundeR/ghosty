const { SlashCommandBuilder } = require('@discordjs/builders');
const { formatTimeValue } = require('../utils/timeUtils');

function formatUptime(uptime) {
    const hours = formatTimeValue(Math.floor(uptime / (60 * 60)));
    const minutes = formatTimeValue(Math.floor(uptime % (60 * 60) / 60));
    const seconds = formatTimeValue(Math.floor(uptime % 60));
    return `Я не сплю уже на протяжении **${hours}:${minutes}:${seconds}**`;
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('аптайм')
        .setDescription('Показывает текущее время работы бота'),
    async execute(interaction) {
        const currUptime = process.uptime();
        const uptimeMessage = formatUptime(currUptime);

        return interaction.reply({
            content: uptimeMessage,
            ephemeral: true,
        });
    },
};
