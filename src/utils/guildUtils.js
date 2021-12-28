function getChannel(interaction) {
    return interaction.client.channels.cache.get(interaction.channelId);
}

exports.getChannel = getChannel;
