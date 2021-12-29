const mainVariablesSchema = require('../schemas/mainVariables');
const cooldownPeriod = 900000;
const avatarsPath = `${__dirname.replace('\\src\\utils', '')}\\assets\\avatars`;

async function getAvatarChangerData() {
    const documentData = await mainVariablesSchema.find({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
    return {
        'avatarNumber': documentData[0].avatarNumber,
        'avatarCooldown': documentData[0].avatarCooldown,
    };
}

async function updateCurrentAvatarNumber(oldAvatarNumber, newAvatarNumber) {
    const filter = { avatarNumber: oldAvatarNumber };
    const update = { avatarNumber: newAvatarNumber };
    await mainVariablesSchema.findOneAndUpdate(filter, update);
}

async function updateCurrentAvatarCooldown(oldAvatarCooldown, newAvatarCooldown) {
    const filter = { avatarCooldown: oldAvatarCooldown };
    const update = { avatarCooldown: newAvatarCooldown };
    await mainVariablesSchema.findOneAndUpdate(filter, update);
}

function checkAvatarCooldown(cooldownCheck) {
    console.log(cooldownCheck);
    if (cooldownCheck > 0) {
        return true;
    }
    return false;
}

async function getRandomAvatar() {
    const currentTime = Date.now();
    const changerData = await getAvatarChangerData();
    let newAvatarCooldown;

    if (changerData['avatarCooldown'] === -1) {
        newAvatarCooldown = currentTime + cooldownPeriod;
    }
    else {
        const cooldownCheck = checkAvatarCooldown(changerData['avatarCooldown'] - currentTime);
        if (cooldownCheck) return null;
        else newAvatarCooldown = currentTime + cooldownPeriod;
    }

    let randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
    if (changerData['avatarNumber'] !== -1) {
        while (randomAvatarNumber === changerData['avatarNumber']) {
            randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
        }
    }
    const choosenAvatar = randomAvatarNumber;

    await updateCurrentAvatarNumber(changerData['avatarNumber'], choosenAvatar);
    await updateCurrentAvatarCooldown(changerData['avatarCooldown'], newAvatarCooldown);
    return `${avatarsPath}\\Avatar_${choosenAvatar}.png`;
}

exports.getRandomAvatar = getRandomAvatar;
