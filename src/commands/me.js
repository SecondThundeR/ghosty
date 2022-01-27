const { SlashCommandBuilder } = require('@discordjs/builders');
const { getChannel } = require('../utils/guildUtils');

function sendMessageFromBot(interaction, userText, textMode) {
    const channel = getChannel(interaction);
    const messagePrefix = `${interaction.user} сказал: `;
    let messageBody = userText;
    let ttsMode = false;

    switch (textMode) {
    case 'анонттс':
        ttsMode = true;
        break;
    case 'ттс':
        messageBody = messagePrefix + userText;
        ttsMode = true;
        break;
    case 'обычный':
        messageBody = messagePrefix + userText;
        break;
    }

    return channel.send(messageBody, {
        tts: ttsMode,
    });
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('йа')
        .setDescription('Аналог команды `/me`')
        .addSubcommand((subcommand) => subcommand
            .setName('обычный')
            .setDescription('Управляет отправкой сообщения в обычном режиме')
            .addStringOption((option) => option
                .setName('текст')
                .setDescription('Текст, который будет написан от лица бота')
                .setRequired(true)))
        .addSubcommand((subcommand) => subcommand
            .setName('анон')
            .setDescription('Управляет отправкой сообщения без упоминания автора')
            .addStringOption((option) => option
                .setName('текст')
                .setDescription('Текст, который будет написан от лица бота')
                .setRequired(true)))
        .addSubcommand((subcommand) => subcommand
            .setName('ттс')
            .setDescription('Управляет отправкой сообщения в режиме TTS')
            .addStringOption((option) => option
                .setName('текст')
                .setDescription('Текст, который будет написан от лица бота')
                .setRequired(true)))
        .addSubcommand((subcommand) => subcommand
            .setName('анонттс')
            .setDescription('Управляет отправкой сообщения без упоминания автора в режиме TTS')
            .addStringOption((option) => option
                .setName('текст')
                .setDescription('Текст, который будет написан от лица бота')
                .setRequired(true))),
    async execute(interaction) {
        const sendMode = interaction.options.getSubcommand();
        const userText = interaction.options.getString('текст');
        sendMessageFromBot(interaction, userText, sendMode);

        return interaction.reply({
            content: 'Текст отправлен!',
            ephemeral: true,
        });
    },
};
