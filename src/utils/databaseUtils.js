const mainVariablesModel = require('../schemas/mainVariables');
const botUsersModel = require('../schemas/botUsers');
const ignoredUsersModel = require('../schemas/ignoredUsers');
const otherBotsModel = require('../schemas/otherBots');

const usersData = {
    guildID: null,
    guildMembers: null,
};
const botsData = {
    guildID: null,
    guildBots: null,
};

async function addModelData(model, data) {
    await new model(data)
        .save().catch((err) => console.error(err));
}

async function getModelData(model) {
    return await model.find({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
}

async function updateAvatarData(options) {
    let filter, update;
    if (options.isAvatarCooldown) {
        filter = { avatarCooldown: options.oldData };
        update = { avatarCooldown: options.newData };
    }
    else {
        filter = { avatarNumber: options.oldData };
        update = { avatarNumber: options.newData };
    }
    await mainVariablesModel.findOneAndUpdate(filter, update);
}

async function updateMemberList(client) {
    await clearModelData(botUsersModel);
    await clearModelData(otherBotsModel);
    const ignoredUsersData = await getModelData(ignoredUsersModel);
    const ignoredUsersID = getIgnoredUsersID(ignoredUsersData);

    for (const guild of client.guilds.cache) {
        const guildID = guild[0];
        usersData['guildID'] = guildID;
        botsData['guildID'] = guildID;
        usersData['guildMembers'] = [];
        botsData['guildBots'] = [];

        const users = await guild[1].members.fetch({ force: true });

        for (const user of users) {
            const memberID = user[0];
            if (ignoredUsersID.includes(memberID)) continue;

            if (user[1].user.bot === false) {
                usersData['guildMembers'].push(memberID);
            }
            else {
                botsData['guildBots'].push(memberID);
            }
        }

        await addModelData(botUsersModel, usersData);
        await addModelData(otherBotsModel, botsData);
    }
}

function getIgnoredUsersID(ignoredUsersData) {
    const usersID = [];
    for (const item of ignoredUsersData) {
        usersID.push(item.userID);
    }
    return usersID;
}

async function clearModelData(model) {
    await model.deleteMany({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
}

exports.addModelData = addModelData;
exports.getModelData = getModelData;
exports.updateMemberList = updateMemberList;
exports.updateAvatarData = updateAvatarData;
exports.clearModelData = clearModelData;
