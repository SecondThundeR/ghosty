const { SlashCommandBuilder } = require('@discordjs/builders');
const { createPollEmbed, createResultsEmbed } = require('../utils/embedUtils');
const { getChannel } = require('../utils/guildUtils');
const { addVoteReactions, parseCollected, evaluateResults } = require('../utils/pollUtils');

async function executePollMessage(interaction, pollText, pollTime) {
    const channel = getChannel(interaction);
    const userName = interaction.member.displayName;
    const pollMessageEmbed = createPollEmbed(userName, pollText, pollTime);

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
