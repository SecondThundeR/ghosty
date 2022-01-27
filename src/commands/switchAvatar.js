const { SlashCommandBuilder } = require('@discordjs/builders');
const { getRandomAvatar } = require('../utils/avatarUtils');
const { getFormattedTime } = require('../utils/timeUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('аватарка')
        .setDescription('Форсирует смену аватара'),
    async execute(interaction) {
        const randomAvatar = await getRandomAvatar();
        if (typeof randomAvatar !== 'number') {
            interaction.client.user.setAvatar(randomAvatar);
            return interaction.reply({
                content: 'Аватарка успешно изменена!',
                ephemeral: true,
            });
        }

        const changerTime = getFormattedTime(randomAvatar / 1000);
        return interaction.reply({
            content: `Пока что нельзя сменить аватарку. Попробуйте через ${changerTime}!`,
            ephemeral: true,
        });
    },
};
