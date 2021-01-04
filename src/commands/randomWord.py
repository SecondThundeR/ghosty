import random
from src.libs.dataImport import dataImport
from src.libs.getRandomUser import getRandomUser
from src.libs.databaseHandler import getDataFromDatabase, editDataInDatabase
words_array = dataImport('src/data/words.txt')


async def randomWord(msg, args):
    currentUser = ''
    if len(args) == 0:
        currentUser = msg.author.mention
    elif args[0] == 'рандом':
        randomUser = await getRandomUser(msg)
        currentUser = randomUser.mention
    else:
        currentUser = args[0]
    isSpamTriggerEnabled = spamChecker(msg)
    if isSpamTriggerEnabled:
        return f'{msg.author.mention} куда спамиш?'
    return f'{currentUser} {random.choice(words_array)}'


def spamChecker(msg):
    currentStatus = getDataFromDatabase('variables', ['spammerID', 'spammerCount'])
    if currentStatus[0] == msg.author.id:
        if currentStatus[1] >= 3:
            editDataInDatabase('variables', ['spammerCount'], [0])
            return True
        editDataInDatabase('variables', ['spammerCount'], [currentStatus[1] + 1])
        return False
    editDataInDatabase('variables', ['spammerID', 'spammerCount'], [msg.author.id, 1])
    return False
