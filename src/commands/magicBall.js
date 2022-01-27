const { SlashCommandBuilder } = require('@discordjs/builders');
const { returnMagicBallAnswer } = require('../utils/magicBallUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('шар')
        .setDescription('Спроси магический шар обо всём (И может он даже ответит правильно!)')
        .addStringOption(option => option
            .setName('вопрос')
            .setDescription('Вопрос, который задаётся магическому шару')
            .setRequired(true))
        .addBooleanOption(option => option
            .setName('тихий-режим')
            .setDescription('Позволяет запустить команду в тихом режиме')
            .setRequired(false)),
    async execute(interaction) {
        const magicBallQuestion = interaction.options.getString('вопрос');
        const magicBallFinalAnswer = returnMagicBallAnswer(magicBallQuestion);
        let quietMode = interaction.options.getBoolean('тихий-режим');

        if (quietMode === null) {
            quietMode = false;
        }

        return interaction.reply({
            content: magicBallFinalAnswer,
            ephemeral: quietMode,
        });
    },
};
