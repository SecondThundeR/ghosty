class GuildUtils {
    static getChannel(interaction) {
        return interaction.client.channels.cache.get(interaction.channelId);
    }
}

exports.GuildUtils = GuildUtils;
