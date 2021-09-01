const { SlashCommandBuilder } = require('@discordjs/builders');

const commandsInfo = {
    "хелп": "выводит эту информацию с командами",
    "шар": "симулятор шара с ответами",
    "макар": 'генерирует предложение "Улыбок тебе дед ..."',
    "ген": "генерирует предложение с помощью цепей Маркова",
    "йа": "аналог команды `/me`",
    "полл": "запускает простое голосование",
    "рандом": "получение рандомного числа",
    "шип": "шипперит двух рандомных пользователей",
    "ху": "рандомный пользователь + предложение",
    "цуефа": 'игра в "Камень-Ножницы-Бумага"',
    "рулетка": "запускает игру в русскую рулетку",
    "аватарка": "запускает смену текущей аватарки",
    "система": "показывает данные о системе",
    "аптайм": "выводит время работы бота",
    "тест": "запускает динамическое тестирование",
    "поиск": '*поиск "кого-то" активирован...*',
    "очки": "управление аккаунтом с очками",
}
const faqLink = "https://github.com/SecondThundeR/ghosty/wiki/Commands-Description"

function returnAllCommands() {
    let commandsSummary = "Доступные команды бота:\n"
    for (const [key, value] of Object.entries(commandsInfo)) {
        commandsSummary += `\n**${key}**: ${value}`;
    }
    commandsSummary += `\n\nПолучить подробную информацию о командах можно здесь - <${faqLink}>`
    return commandsSummary;
}

function returnCertainCommand(commandName) {
    const commandInfo = commandsInfo[commandName];
    const commandAnswer = `Короткая информация о \`${commandName}\` - ${commandInfo}\n\n` +
                          `Получить больше информации можно здесь - <${faqLink}#${commandName}>`;
    return commandAnswer;
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('help')
        .setDescription('Показывает все доступные команды бота')
        .addStringOption(option => option.setName('name').setDescription('Возвращает информацию о введённой команде')),
    async execute(interaction) {
        const commandName = interaction.options.getString('name');
        if (commandName) {
            return interaction.reply(returnCertainCommand(commandName));
        };
        return interaction.reply(returnAllCommands());
    },
};
