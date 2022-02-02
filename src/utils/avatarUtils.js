const mainVariablesModel = require('../schemas/mainVariables');
const {
    getModelData,
    updateAvatarData,
} = require('../utils/databaseUtils');

const cooldownPeriod = 900000;
const avatarsPath = `${__dirname.replace('\\src\\utils', '')}\\assets\\avatars`;

class AvatarUtils {
    static checkAvatarCooldown(cooldownCheck) {
        if (cooldownCheck > 0) {
            return true;
        }
        return false;
    }

    static async getRandomAvatar() {
        const currentTime = Date.now();
        const changerData = await getModelData(mainVariablesModel);
        const avatarCooldown = changerData[0].avatarCooldown;
        const avatarNumber = changerData[0].avatarNumber;
        let newAvatarCooldown;

        if (avatarCooldown === -1) {
            newAvatarCooldown = currentTime + cooldownPeriod;
        }
        else {
            const cooldownDiff = avatarCooldown - currentTime;
            const cooldownCheck = AvatarUtils.checkAvatarCooldown(cooldownDiff);
            if (cooldownCheck) return cooldownDiff;
            else newAvatarCooldown = currentTime + cooldownPeriod;
        }

        let randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
        if (avatarNumber !== -1) {
            while (randomAvatarNumber === avatarNumber) {
                randomAvatarNumber = Math.floor(Math.random() * 16) + 1;
            }
        }
        const choosenAvatar = randomAvatarNumber;

        await updateAvatarData({
            oldData: avatarNumber,
            newData: choosenAvatar,
            isAvatarCooldown: false,
        });
        await updateAvatarData({
            oldData: avatarCooldown,
            newData: newAvatarCooldown,
            isAvatarCooldown: true,
        });
        return `${avatarsPath}\\Avatar_${choosenAvatar}.png`;
    }
}

exports.AvatarUtils = AvatarUtils;
