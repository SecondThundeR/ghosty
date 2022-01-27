const { SlashCommandBuilder } = require('@discordjs/builders');
const { getCommandsInfo } = require('../utils/helpUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('хелп')
        .setDescription('Показывает информацию о командах бота')
        .addStringOption(option => option
            .setName('команда')
            .setDescription('Возвращает информацию о конкретной команде'),
        ),
    async execute(interaction) {
        const commandName = interaction.options.getString('команда');

        return interaction.reply({
            content: getCommandsInfo(commandName),
            ephemeral: true,
        });
    },
};
