const { SlashCommandBuilder } = require('@discordjs/builders');

const magicBallAnswers = [
    'Бесспорно',
    'Предрешено',
    'Никаких сомнений',
    'Определённо да',
    'Можешь быть уверен в этом',
    'Мне кажется — «да»',
    'Вероятнее всего',
    'Хорошие перспективы',
    'Знаки говорят — «да»',
    'Да',
    'Пока не ясно, попробуй снова',
    'Спроси позже',
    'Лучше не рассказывать',
    'Сейчас нельзя предсказать',
    'Сконцентрируйся и спроси опять',
    'Даже не думай',
    'Мой ответ — «нет»',
    'По моим данным — «нет»',
    'Перспективы не очень хорошие',
    'Весьма сомнительно',
];

function returnMagicBallAnswer(userQuestion) {
    const magicBallAnswer = magicBallAnswers[Math.floor(Math.random() * magicBallAnswers.length)];
    const answerMsg = `Вопрос: **${userQuestion}**\nОтвет: **${magicBallAnswer}**`;
    return answerMsg;
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('шар')
        .setDescription('Спроси магический шар обо всём (И может он даже ответит правильно!)')
        .addStringOption(option => option
            .setName('вопрос')
            .setDescription('Вопрос, который задаётся магическому шару')
            .setRequired(true),
        )
        .addBooleanOption(option => option
            .setName('тихий-режим')
            .setDescription('Позволяет запустить команду в тихом режиме')
            .setRequired(false),
        ),
    async execute(interaction) {
        const magicBallQuestion = interaction.options.getString('вопрос');
        const quietMode = interaction.options.getBoolean('тихий-режим');
        const magicBallFinalAnswer = returnMagicBallAnswer(magicBallQuestion);
        if (quietMode === null || quietMode === false) {
            return interaction.reply({
                content: magicBallFinalAnswer,
            });
        }
        return interaction.reply({
            content: magicBallFinalAnswer,
            ephemeral: true,
        });
    },
};
