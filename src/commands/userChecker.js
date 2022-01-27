const { SlashCommandBuilder } = require('@discordjs/builders');
const { getRandomNumber } = require('../utils/miscUtils');
const { getRandomUser } = require('../utils/userUtils');

function generateTestMessage(text, user, amount) {
    let testMessage = `Журнал тестирования **${user}**\n\n`;
    if (amount <= 1) {
        const randomPercent = getRandomNumber(0, 100);
        switch (randomPercent) {
        case 0:
            testMessage += `Пациент сегодня не **${text}** :c`;
            break;
        case 100:
            testMessage += `Кто бы мог подумать то!\nПациент **${text}** на ${randomPercent}%`;
            break;
        default:
            testMessage += `Пациент **${text}** на ${randomPercent}%`;
            break;
        }
        return testMessage;
    }
    for (let i = 0; i < amount; i++) {
        const randomPercent = getRandomNumber(0, 100);
        switch (randomPercent) {
        case 0:
            testMessage += `**Тест #${i + 1}.** Пациент сегодня не **${text}** :c\n`;
            break;
        case 100:
            testMessage += `**Тест #${i + 1}.** Кто бы мог подумать то!\nПациент **${text}** на ${randomPercent}%\n`;
            break;
        default:
            testMessage += `**Тест #${i + 1}.** Пациент **${text}** на ${randomPercent}%\n`;
            break;
        }
        if (testMessage.length > 2000) {
            return undefined;
        }
    }
    return testMessage;
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('тест')
        .setDescription('Активирует "тест" над пользователями')
        .addStringOption(option => option
            .setName('текст')
            .setDescription('Устанавливает текст теста')
            .setRequired(true))
        .addNumberOption(option => option
            .setName('число-тестов')
            .setDescription('Устанавливает количество тестирований'))
        .addUserOption(option => option
            .setName('пользователь')
            .setDescription('Задает пользователя для тестирования'))
        .addStringOption(option => option
            .setName('тестируемый')
            .setDescription('Устанавливает вместо тестирумого пользователя, текст'))
        .addBooleanOption(option => option
            .setName('рандом-выбор')
            .setDescription('Выбирает случайного пользователя для тестирования')),
    async execute(interaction) {
        const testText = interaction.options.getString('текст');
        const testAmount = interaction.options.getNumber('число-тестов') || 1;
        const textTestUser = interaction.options.getString('тестируемый') || null;
        const testUserObject = interaction.options.getUser('пользователь') || null;
        const randomUserBoolean = interaction.options.getBoolean('рандом-выбор') || false;
        let testUser;

        if (randomUserBoolean === true) {
            const randomUser = await getRandomUser(interaction.guild);
            testUser = `${randomUser}`;
        }
        else if (testUserObject !== null) {
            testUser = `${interaction.options.getUser('пользователь')}`;
        }
        else if (textTestUser !== null) {
            testUser = textTestUser;
        }
        else {
            testUser = `${interaction.user}`;
        }

        const testMessage = generateTestMessage(testText, testUser, testAmount);
        if (testMessage === undefined) {
            return interaction.reply({
                content: 'Вы превысили лимит Discord по длине сообщения!',
                ephemeral: true,
            });
        }
        return interaction.reply({
            content: testMessage,
        });
    },
};
