const mongoose = require('mongoose');
const AvatarUtils = require('../utils/avatarUtils');
const DatabaseUtils = require('../utils/databaseUtils');

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        await mongoose.connect(process.env.MONGO_URI, {
            keepAlive: true,
        });
        client.user.setStatus('dnd');
        const randomAvatar = await AvatarUtils.getRandomAvatar();
        if (typeof randomAvatar !== 'number') {
            client.user.setAvatar(randomAvatar);
        }
        await DatabaseUtils.updateMemberList(client);
        console.log(`Выполнен вход как ${client.user.tag}`);
    },
};
