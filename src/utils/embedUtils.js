const { MessageEmbed } = require('discord.js');

const logoColors = [
    '#C9CBFF',
    '#7868E6',
    '#DEF4F0',
    '#DEF4F0',
    '#43658B',
    '#654062',
    '#132743',
    '#763857',
    '#ECA3F5',
    '#132C33',
    '#78C4D4',
    '#046582',
    '#822659',
    '#F1D1D0',
    '#1687A7',
    '#2A3D66',
];

function getRandomEmbedColor() {
    return logoColors[Math.floor(Math.random() * logoColors.length)];
}

function createPollEmbed(userName, pollText, pollTime) {
    const pollEmbed = new MessageEmbed()
        .setColor(getRandomEmbedColor())
        .setTitle(`Новое голосование от ${userName}`)
        .setDescription(pollText)
        .addFields(
            { name: 'Время для голосования', value: `${pollTime} секунд` },
        );
    return pollEmbed;
}

function createResultsEmbed(userName, pollText, pollResults) {
    const resultsEmbed = new MessageEmbed()
        .setColor(getRandomEmbedColor())
        .setTitle(`Результаты голосования "${pollText}" от ${userName}`)
        .setDescription(pollResults);
    return resultsEmbed;
}

exports.createPollEmbed = createPollEmbed;
exports.createResultsEmbed = createResultsEmbed;
