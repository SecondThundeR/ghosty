const { MessageEmbed } = require('discord.js');
const { SlashCommandBuilder } = require('@discordjs/builders');
const { getRandomEmbedColor } = require('../utils/embedUtils');
const { getChannel } = require('../utils/guildUtils');

function createEmbedPoll(userName, pollText, pollTime) {
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

async function addVoteReactions(message) {
    try {
        await message.react('👍');
        await message.react('👎');
    }
    catch (error) {
        console.log('Произошла ошибка при добавлении реакций на голосование:', error);
    }
}

function parseCollected(collected) {
    const reactionsMap = {
        '👍': 0,
        '👎': 0,
    };
    collected.map(
        reaction => reactionsMap[reaction.emoji.name] = reaction.count - 1,
    );
    return reactionsMap;
}

function evaluateResults(pollData) {
    const likesCount = pollData['👍'];
    const dislikesCount = pollData['👎'];

    if (likesCount > dislikesCount) return `Сокрушительная победа! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
    if (likesCount < dislikesCount) return `Безжалостное поражение! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
    return `Возможно, победа дружбы! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
}

async function executePollMessage(interaction, pollText, pollTime) {
    const channel = getChannel(interaction);
    const userName = interaction.member.displayName;
    const pollMessageEmbed = createEmbedPoll(userName, pollText, pollTime);

    const message = await channel.send({ embeds: [pollMessageEmbed] });
    await addVoteReactions(message);

    const pollFilter = (reaction, user) => {
        return ['👍', '👎'].includes(reaction.emoji.name) && user.id !== message.author.id;
    };

    const collector = message.createReactionCollector({ pollFilter, time: pollTime * 1000 });

    collector.on('end', async (collected) => {
        const pollData = parseCollected(collected);
        const resultText = evaluateResults(pollData);
        const resultsEmbed = createResultsEmbed(userName, pollText, resultText);
        await message.delete();
        await channel.send({ embeds: [resultsEmbed] });
    });
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('полл')
        .setDescription('Создает голосования с реакциями')
        .addStringOption((option) =>
            option
                .setName('текст')
                .setDescription('Текст для голосования')
                .setRequired(true),
        )
        .addNumberOption((option) =>
            option
                .setName('время')
                .setDescription(
                    'Устанавливает время до конца голосования (По умолчанию - 60 секунд)',
                ),
        ),
    async execute(interaction) {
        const pollText = interaction.options.getString('текст');
        let pollTime = interaction.options.getNumber('время') || 60;
        let replyMessage = 'Голосование запущено!';

        if (pollTime < 60) {
            pollTime = 60;
            replyMessage = 'Голосование запущено! *(Время было изменено до 60 секунд)*';
        }

        await interaction.reply({
            content: replyMessage,
            ephemeral: true,
        });
        return await executePollMessage(interaction, pollText, pollTime);
    },
};
