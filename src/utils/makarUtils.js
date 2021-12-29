const userDataEnum = {
    'here/everyone': 1,
    'emoji': 2,
    'rolename': 3,
    'username': 4,
    'default': 5,
};
Object.freeze(userDataEnum);

function getUserDataType(userData) {
    if (userData === '@here' || userData === '@everyone') {
        return userDataEnum['here/everyone'];
    }
    if (userData.startsWith('<:')) {
        return userDataEnum['emoji'];
    }
    if (userData.startsWith('<@&')) {
        return userDataEnum['rolename'];
    }
    if (userData.startsWith('<@!')) {
        return userDataEnum['username'];
    }
    return userDataEnum['default'];
}

exports.userDataEnum = userDataEnum;
exports.getUserDataType = getUserDataType;
