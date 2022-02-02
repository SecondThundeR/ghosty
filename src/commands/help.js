const { SlashCommandBuilder } = require('@discordjs/builders');
const HelpUtils = require('../utils/helpUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('хелп')
        .setDescription('Показывает информацию о командах бота')
        .addStringOption(option => option
            .setName('команда')
            .setDescription('Возвращает информацию о конкретной команде')),
    async execute(interaction) {
        const commandName = interaction.options.getString('команда');
        let helpMsg;

        if (commandName === null) {
            helpMsg = HelpUtils.getAllCommandsInfo();
        }
        helpMsg = HelpUtils.getCertainCommandInfo(commandName);

        return interaction.reply({
            content: helpMsg,
            ephemeral: true,
        });
    },
};
