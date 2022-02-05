const { SlashCommandBuilder } = require('@discordjs/builders');
const SystemUtils = require('../utils/systemUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('система')
        .setDescription('Показывает информацию о системе, на которой запущен бот'),
    async execute(interaction) {
        const systemInfo = SystemUtils.getSystemDataMessage();

        return interaction.reply({
            content: systemInfo,
            ephemeral: true,
        });
    },
};
