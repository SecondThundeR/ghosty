const botUsersModel = require('../schemas/botUsers');
const { getModelData } = require('./databaseUtils');

function fetchUsernameByID(currentGuild, rawUserID) {
    const userID = parseRawID(rawUserID);
    const guildUser = currentGuild.members.cache.get(userID);
    return guildUser.displayName;
}

function fetchRolenameByID(currentGuild, rawRoleID) {
    const roleID = parseRawID(rawRoleID);
    const roleName = currentGuild.roles.cache.get(roleID).name;
    return roleName;
}

function parseRawID(rawID) {
    return rawID.slice(3, -1);
}

async function getRandomUser(guild) {
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

exports.fetchUsernameByID = fetchUsernameByID;
exports.fetchRolenameByID = fetchRolenameByID;
exports.getRandomUser = getRandomUser;
