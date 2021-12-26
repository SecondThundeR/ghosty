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

function getUserMention(userID) {
    return `<@${userID}>`;
}

exports.fetchUsernameByID = fetchUsernameByID;
exports.fetchRolenameByID = fetchRolenameByID;
exports.getUserMention = getUserMention;
