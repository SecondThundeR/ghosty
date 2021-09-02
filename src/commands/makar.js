const { SlashCommandBuilder } = require('@discordjs/builders');

function fetchUserByID(currentGuild, rawUserID) {
    const userID = parseRawID(rawUserID);
    const guildUser = currentGuild.members.cache.get(userID);
    return guildUser.displayName;
}

function fetchRolenameByID(currentGuild, rawRoleID) {
    const roleID = parseRawID(rawRoleID);
    const roleName = currentGuild.roles.cache.get(roleID).name;
    return roleName;
}

function reverseString(str) {
    return str.split("").reverse().join("");
}

function parseRawID(rawID) {
    return rawID.slice(3,-1);
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('макар')
        .setDescription('Отправляет предложение вида "Улыбок тебе дед ракаМ" (Макар наоборот)')
        .addStringOption(option =>
            option.setName('user')
                .setDescription('Кого подставить вместо Макара?')),
    async execute(interaction) {
        let makarData = interaction.options.getString('user');
        if (makarData) {
            if (makarData === "@here" || makarData === "@everyone") {
                return interaction.reply({
                    content: `Улыбок тебе дед ${reverseString(makarData.slice(1))}`
                });
            }
            if (makarData.startsWith("<:")) {
                return interaction.reply({
                    content: "Я не могу перевернуть эмодзи(",
                    ephemeral: true
                });
            }
            if (makarData.startsWith("<@&")) {
                makarData = fetchRolenameByID(interaction.guild, makarData);
            }
            else if (makarData.startsWith("<@!")) {
                makarData = fetchUserByID(interaction.guild, makarData);
            }
            return interaction.reply({
                content: `Улыбок тебе дед ${reverseString(makarData)}`
            });
        }
        return interaction.reply({
            content: `Улыбок тебе дед ${reverseString(interaction.member.displayName)}`
        });
    },
};
