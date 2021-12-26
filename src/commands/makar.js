const { SlashCommandBuilder } = require('@discordjs/builders');
const { fetchRolenameByID, fetchUsernameByID } = require('../utils/userUtils');
const { reverseString } = require('../utils/stringUtils');

const userDataEnum = {
    'here/everyone': 1,
    'emoji': 2,
    'rolename': 3,
    'username': 4,
    'default': 5,
};
Object.freeze(userDataEnum);

function getUserDataType(userData) {
    if (userData === '@here' || userData === '@everyone') {
        return userDataEnum['here/everyone'];
    }
    if (userData.startsWith('<:')) {
        return userDataEnum['emoji'];
    }
    if (userData.startsWith('<@&')) {
        return userDataEnum['rolename'];
    }
    if (userData.startsWith('<@!')) {
        return userDataEnum['username'];
    }
    return userDataEnum['default'];
}

async function executeMakarInteraction(interaction, userData) {
    if (!userData) {
        return interaction.reply({
            content: `Улыбок тебе дед ${reverseString(interaction.member.displayName)}`,
        });
    }

    let stringToReverse;
    const userDataType = getUserDataType(userData);

    switch (userDataType) {
    case userDataEnum['here/everyone']:
        return interaction.reply({
            content: `Улыбок тебе дед ${reverseString(userData.slice(1))}`,
        });
    case userDataEnum['emoji']:
        return interaction.reply({
            content: 'Я не могу перевернуть эмодзи(',
            ephemeral: true,
        });
    case userDataEnum['rolename']:
        stringToReverse = fetchRolenameByID(interaction.guild, userData);
        break;
    case userDataEnum['username']:
        stringToReverse = fetchUsernameByID(interaction.guild, userData);
        break;
    case userDataEnum['default']:
        stringToReverse = userData;
        break;
    }

    return interaction.reply({
        content: `Улыбок тебе дед ${reverseString(stringToReverse)}`,
    });
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('макар')
        .setDescription('Отправляет предложение вида "Улыбок тебе дед ракаМ" (Макар наоборот)')
        .addStringOption(option => option
            .setName('юзер')
            .setDescription('Кого подставить вместо Макара?'),
        ),
    async execute(interaction) {
        const userData = interaction.options.getString('юзер');
        await executeMakarInteraction(interaction, userData);
    },
};
