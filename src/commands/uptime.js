const { SlashCommandBuilder } = require('@discordjs/builders');
const TimeUtils = require('../utils/timeUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('аптайм')
        .setDescription('Показывает текущее время работы бота'),
    async execute(interaction) {
        const uptimeMessage = `Я не сплю уже на протяжении ${TimeUtils.getFormattedTime(process.uptime())}`;

        return interaction.reply({
            content: uptimeMessage,
            ephemeral: true,
        });
    },
};
