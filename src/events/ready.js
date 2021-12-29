const mongoose = require('mongoose');
const { getRandomAvatar } = require('../utils/avatarUtils');

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        await mongoose.connect(process.env.MONGO_URI, {
            keepAlive: true,
        });
        client.user.setStatus('dnd');
        const randomAvatar = await getRandomAvatar();
        if (typeof randomAvatar !== 'number') {
            client.user.setAvatar(randomAvatar);
        }
        console.log(`Выполнен вход как ${client.user.tag}`);
    },
};
