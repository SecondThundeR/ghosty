const { SlashCommandBuilder } = require('@discordjs/builders');
const MiscUtils = require('../utils/miscUtils');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('рандом')
        .setDescription('Показывает информацию о командах бота')
        .addSubcommand(subcommand => subcommand
            .setName('число')
            .setDescription('Получение рандомного числа от 1 до выбранного диапазона')
            .addNumberOption(option => option
                .setName('граница')
                .setDescription('Устанавливает правую границу диапазона для рандомного числа')
                .setRequired(true)))
        .addSubcommand(subcommand => subcommand
            .setName('числа')
            .setDescription('Получение рандомного числа для собственного диапазона')
            .addNumberOption(option => option
                .setName('граница-левая')
                .setDescription('Устанавливает левую границу диапазона')
                .setRequired(true))
            .addNumberOption(option => option
                .setName('граница-правая')
                .setDescription('ТУстанавливает правую границу диапазона')
                .setRequired(true))),
    async execute(interaction) {
        const randomMode = interaction.options.getSubcommand();
        let lowNum = 1;
        let highNum;

        if (randomMode === 'число') {
            highNum = interaction.options.getNumber('граница');
        }
        else {
            lowNum = interaction.options.getNumber('граница-левая');
            highNum = interaction.options.getNumber('граница-правая');
        }

        const randomNumber = MiscUtils.getRandomNumber(lowNum, highNum);
        if (randomNumber === null) {
            return interaction.reply({
                content: 'Неверный диапазон чисел или значения чисел!',
                ephemeral: true,
            });
        }

        const message = `Случайное число от ${lowNum} до ${highNum}: **${randomNumber}**`;
        return interaction.reply({
            content: message,
        });
    },
};
