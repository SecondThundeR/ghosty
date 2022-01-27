const commandsInfo = {
    'хелп': 'показывает данное сообщение с информацией',
    'шар': 'симулятор шара с ответами',
    'макар': 'генерирует предложение "Улыбок тебе дед ..."',
    'ген': 'генерирует предложение с помощью цепей Маркова',
    'йа': 'аналог команды `/me`',
    'полл': 'запускает простое голосование',
    'рандом': 'получение рандомного числа',
    'шип': 'шипперит двух рандомных пользователей',
    'ху': 'рандомный пользователь + предложение',
    'цуефа': 'игра в "Камень-Ножницы-Бумага"',
    'рулетка': 'запускает игру в русскую рулетку',
    'аватарка': 'запускает смену текущей аватарки',
    'система': 'показывает данные о системе',
    'аптайм': 'выводит время работы бота',
    'тест': 'запускает динамическое тестирование',
    'поиск': 'поиск *"кого-то"* активирован...',
    'очки': 'управление аккаунтом с очками',
};
const faqLink = 'https://github.com/SecondThundeR/ghosty/wiki/Commands-Description';
const commandsSummaryHeader = 'Доступные команды бота:\n';
const commandInfoHelp = `\n\nПолучить подробную информацию о командах можно здесь - <${faqLink}>`;
const undefinedCommandName = 'Похоже, вы ввели несуществующую команду :c';

function getAllCommandsInfo() {
    let commandsSummary = commandsSummaryHeader;
    for (const [key, value] of Object.entries(commandsInfo)) {
        commandsSummary += `\n**${key}**: ${value}`;
    }
    commandsSummary += commandInfoHelp;
    return commandsSummary;
}

function getCertainCommandInfo(commandName) {
    const commandEntry = commandsInfo[commandName];
    if (commandEntry === undefined) {
        return undefinedCommandName;
    }

    const commandAnswer = `Короткая информация о \`${commandName}\` - ${commandEntry}\n\n` +
        `Получить больше информации можно здесь - <${faqLink}#${commandName}>`;
    return commandAnswer;
}

function getCommandsInfo(commandName) {
    if (commandName === null) {
        return getAllCommandsInfo();
    }
    return getCertainCommandInfo(commandName);
}

exports.getCommandsInfo = getCommandsInfo;
