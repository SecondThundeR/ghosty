const mainVariablesSchema = require('../schemas/mainVariables');
const avatarsPath = `${__dirname.replace('\\src\\utils', '')}\\assets\\avatars`;

async function getCurrentAvatarNumber() {
    const documentData = await mainVariablesSchema.find({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
    return documentData[0].avatarNumber;
}

async function updateCurrentAvatarNumber(oldAvatarNumber, newAvatarNumber) {
    const filter = { avatarNumber: oldAvatarNumber };
    const update = { avatarNumber: newAvatarNumber };
    await mainVariablesSchema.findOneAndUpdate(filter, update);
}

async function getRandomAvatar() {
    const oldAvatar = await getCurrentAvatarNumber();
    let randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
    if (oldAvatar !== -1) {
        while (randomAvatarNumber === oldAvatar) {
            randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
        }
    }
    const choosenAvatar = randomAvatarNumber;
    await updateCurrentAvatarNumber(oldAvatar, choosenAvatar);
    return `${avatarsPath}\\Avatar_${choosenAvatar}.png`;
}

exports.getRandomAvatar = getRandomAvatar;
