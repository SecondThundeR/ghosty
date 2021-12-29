const mongoose = require('mongoose');
const { getRandomAvatar } = require('../utils/avatarUtils');

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        await mongoose.connect(process.env.MONGO_URI, {
            keepAlive: true,
        });
        const randomAvatar = await getRandomAvatar();
        client.user.setStatus('dnd');
        if (randomAvatar !== null) {
            client.user.setAvatar(randomAvatar);
        }
        console.log(`Выполнен вход как ${client.user.tag}`);
    },
};
