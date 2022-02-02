const botUsersModel = require('../schemas/botUsers');
const { getModelData } = require('./databaseUtils');

class UserUtils {
    static fetchUsernameByID(currentGuild, rawUserID) {
        const userID = UserUtils.parseRawID(rawUserID);
        const guildUser = currentGuild.members.cache.get(userID);
        return guildUser.displayName;
    }

    static fetchRolenameByID(currentGuild, rawRoleID) {
        const roleID = UserUtils.parseRawID(rawRoleID);
        const roleName = currentGuild.roles.cache.get(roleID).name;
        return roleName;
    }

    static parseRawID(rawID) {
        return rawID.slice(3, -1);
    }

    static async getRandomUser(guild) {
        let guildUsers;
        const botUsersData = await getModelData(botUsersModel);
        for (const item of botUsersData) {
            if (item.guildID == guild.id) {
                guildUsers = item.guildMembers;
                break;
            }
        }
        const randomUserID = guildUsers[Math.floor(Math.random() * guildUsers.length)];
        const guildUser = guild.members.cache.get(randomUserID);
        return guildUser;
    }
}

exports.UserUtils = UserUtils;
