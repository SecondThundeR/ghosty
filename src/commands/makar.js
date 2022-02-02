const { SlashCommandBuilder } = require('@discordjs/builders');
const UserUtils = require('../utils/userUtils');
const StringUtils = require('../utils/stringUtils');
const { userDataEnum, MakarUtils } = require('../utils/makarUtils');

async function executeMakarInteraction(interaction, userData) {
    let stringToReverse;
    const userDataType = MakarUtils.getUserDataType(userData);

    if (!userData) {
        return interaction.reply({
            content: `Улыбок тебе дед ${StringUtils.reverseString(interaction.member.displayName)}`,
        });
    }

    switch (userDataType) {
    case userDataEnum['emoji']:
        return interaction.reply({
            content: 'Я не могу перевернуть эмодзи(',
            ephemeral: true,
        });
    case userDataEnum['here/everyone']:
        stringToReverse = userData.slice(1);
        break;
    case userDataEnum['rolename']:
        stringToReverse = UserUtils.fetchRolenameByID(interaction.guild, userData);
        break;
    case userDataEnum['username']:
        stringToReverse = UserUtils.fetchUsernameByID(interaction.guild, userData);
        break;
    case userDataEnum['default']:
        stringToReverse = userData;
        break;
    }

    return interaction.reply({
        content: `Улыбок тебе дед ${StringUtils.reverseString(stringToReverse)}`,
    });
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('макар')
        .setDescription('Отправляет предложение вида "Улыбок тебе дед ракаМ" (Макар наоборот)')
        .addStringOption(option => option
            .setName('юзер')
            .setDescription('Кого подставить вместо Макара?')),
    async execute(interaction) {
        const userData = interaction.options.getString('юзер');
        await executeMakarInteraction(interaction, userData);
    },
};
