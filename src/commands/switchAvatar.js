const { SlashCommandBuilder } = require('@discordjs/builders');
const AvatarUtils = require('../utils/avatarUtils');
const TimeUtils = require('../utils/timeUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('аватарка')
        .setDescription('Форсирует смену аватара'),
    async execute(interaction) {
        const randomAvatar = await AvatarUtils.getRandomAvatar();
        if (typeof randomAvatar !== 'number') {
            await interaction.client.user.setAvatar(randomAvatar);
            return interaction.reply({
                content: 'Аватарка успешно изменена!',
                ephemeral: true,
            });
        }

        const changerTime = TimeUtils.getFormattedTime(randomAvatar / 1000);
        return interaction.reply({
            content: `Пока что нельзя сменить аватарку. Попробуйте через ${changerTime}!`,
            ephemeral: true,
        });
    },
};
