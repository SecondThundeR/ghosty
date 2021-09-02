const { SlashCommandBuilder } = require('@discordjs/builders');

const magicBallAnswers = [
    "Бесспорно",
    "Предрешено",
    "Никаких сомнений",
    "Определённо да",
    "Можешь быть уверен в этом",
    "Мне кажется — «да»",
    "Вероятнее всего",
    "Хорошие перспективы",
    "Знаки говорят — «да»",
    "Да",
    "Пока не ясно, попробуй снова",
    "Спроси позже",
    "Лучше не рассказывать",
    "Сейчас нельзя предсказать",
    "Сконцентрируйся и спроси опять",
    "Даже не думай",
    "Мой ответ — «нет»",
    "По моим данным — «нет»",
    "Перспективы не очень хорошие",
    "Весьма сомнительно",
]

function returnMagicBallAnswer(userQuestion) {
    const magicBallAnswer = magicBallAnswers[Math.floor(Math.random() * magicBallAnswers.length)];
    const answerMsg = `Вопрос: **${userQuestion}**\nОтвет: **${magicBallAnswer}**`;
    return answerMsg;
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('шар')
        .setDescription('Спроси магический шар обо всём (И может он даже ответит правильно!)')
        .addStringOption(option =>
            option.setName('question')
                .setDescription('Вопрос, который задаётся магическому шару')
                .setRequired(true)),
    async execute(interaction) {
        const magicBallQuestion = interaction.options.getString('question');
        const magicBallFinalAnswer = returnMagicBallAnswer(magicBallQuestion);
        return interaction.reply({
            content: magicBallFinalAnswer
        });
    },
};
