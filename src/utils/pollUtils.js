async function addVoteReactions(message) {
    try {
        await message.react('👍');
        await message.react('👎');
    }
    catch (error) {
        console.log('Произошла ошибка при добавлении реакций на голосование:', error);
    }
}

function parseCollected(collected) {
    const reactionsMap = {
        '👍': 0,
        '👎': 0,
    };
    collected.map(
        reaction => reactionsMap[reaction.emoji.name] = reaction.count - 1,
    );
    return reactionsMap;
}

function evaluateResults(collected) {
    const pollData = parseCollected(collected);
    const likesCount = pollData['👍'];
    const dislikesCount = pollData['👎'];

    if (likesCount > dislikesCount) return `Сокрушительная победа! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
    if (likesCount < dislikesCount) return `Безжалостное поражение! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
    return `Возможно, победа дружбы! - 👍: ${likesCount} / 👎: ${dislikesCount}`;
}

exports.addVoteReactions = addVoteReactions;
exports.evaluateResults = evaluateResults;
