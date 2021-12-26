const { SlashCommandBuilder } = require('@discordjs/builders');
const { getUserMention } = require('../utils/userUtils');

function sendMessageFromBot(interaction, textToSend, textMode) {
	const channel = interaction.client.channels.cache.get(interaction.channelId);
	const regularMessage = `${getUserMention(interaction.user.id)} сказал: `;

	switch (textMode) {
	case 'анонттс':
		return channel.send(textToSend, {
			tts: true,
		});
	case 'анон':
		return channel.send(textToSend);
	case 'ттс':
		return channel.send(regularMessage + textToSend, {
			tts: true,
		});
	case 'обычный':
		return channel.send(regularMessage + textToSend);
	}
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('йа')
		.setDescription('Аналог команды `/me`')
		.addSubcommand(subcommand => subcommand
			.setName('обычный')
			.setDescription('Управляет отправкой сообщения в обычном режиме')
			.addStringOption(option => option
				.setName('текст')
				.setDescription('Текст, который будет написан от лица бота')
				.setRequired(true),
			),
		)
		.addSubcommand(subcommand => subcommand
			.setName('анон')
			.setDescription('Управляет отправкой сообщения без упоминания автора')
			.addStringOption(option => option
				.setName('текст')
				.setDescription('Текст, который будет написан от лица бота')
				.setRequired(true),
			),
		)
		.addSubcommand(subcommand => subcommand
			.setName('ттс')
			.setDescription('Управляет отправкой сообщения в режиме TTS')
			.addStringOption(option => option
				.setName('текст')
				.setDescription('Текст, который будет написан от лица бота')
				.setRequired(true),
			),
		)
		.addSubcommand(subcommand => subcommand
			.setName('анонттс')
			.setDescription('Управляет отправкой сообщения без упоминания автора в режиме TTS')
			.addStringOption(option => option
				.setName('текст')
				.setDescription('Текст, который будет написан от лица бота')
				.setRequired(true),
			),
		),
	async execute(interaction) {
		const sendMode = interaction.options.getSubcommand();
		const textToSend = interaction.options.getString('текст');
		sendMessageFromBot(interaction, textToSend, sendMode);
		return interaction.reply({
			content: 'Текст отправлен!',
			ephemeral: true,
		});
	},
};
