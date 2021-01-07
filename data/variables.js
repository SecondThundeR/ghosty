exports.vars = {
	// (createPoll.js) initPoll()
	pollLocked: false,

	// (randomShip.js) randomShipping()
	shipDate: '',
	shipTextFull: '',
	shipTextShort: '',
	firstRandomUserInfo: '',
	secondRandomUserInfo: '',
	firstUsername: '',
	secondUsername: '',
	finalShipname: '',
	shipActivated: false,
	shipInActive: false,

	// (rspGame.js) rspGameBot()
	moveVariants: ['камень', 'ножницы', 'бумага'],

	// (spamChecker.js) spamChecker()
	spammerID: '',
	spammerCount: 0,
};

exports.ignorelist = {
	// Currently, this section is empty, but you can add someone, which you want to ignore, when triggering command
	// (Also, there is no check for ignore, but this part is easy to add)
};

exports.text = {
	// (main.js) client.on('ready)
	activityName: 'Helltaker',

	// addWord.js + deleteWord.js
	notFoundFileRoulette: 'Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!',

	// (addWord.js) addWord()
	successAddWord: 'Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(',
	failAddWord: 'Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего',

	// (addWord.js) addBot()
	successAddBot: 'Я добавил этого бота в исключения! Теперь я буду его игнорировать',
	failAddBot: 'Данный бот уже есть у меня в исключениях!',

	// (addWord.js) addWordRoulette()
	successAddRouletteWord: 'Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(',
	failAddRouletteWord: 'Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего',

	// (createPoll.js) pollInit()
	pollIsActiveWarn: 'К сожалению, у вас сейчас имеется одно активное голование в чате.' +
		'\nВы сможете запустить новое только по окончанию старого',

	// (createPoll.js) getVoteResult()
	endPollText1: '**ГОЛОСОВАНИЕ ОКОНЧЕНО!**\nВопрос **',
	endPollText2: '** от ',
	noVotesText: ' не получил никаких голосов, поэтому данное голосование объявляется **несостоявшимся!**',
	positiveResultText: ' был принят среди многих **положительно**!\n*Ну разве это не счастье?*',
	negativeResultText: ' был принят среди многих **отрицательно**!\n*Что ж, неудачам тоже свойственно быть*',
	noWinnerText: ' набрал одинаковое голосов, а значит данное голосование объявляется **несостоявшимся!**',

	// (createPoll.js) createPoll()
	pollText1: '**ВРЕМЯ ГОЛОСОВАНИЯ ОТ ',
	pollText2: '**\nВопрос: ',
	pollText3: '\n*На подумать - ',
	pollText4: ' секунд*',

	// (dedMakar.js) dedMakar()
	makarErrorParsing: 'К сожалению, я не могу обработать это, так как могу выдасть ошибку. Попробуйте что-то другое',
	makarErrorEmoji: 'Дядя, что ты мне дал? Какой блин переворот эмодзи...',
	makarDefaultText: 'Улыбок тебе дед ',

	// (deleteWord.js) deleteWord()
	successDeleteWord: 'Я удалил это слово у себя. Неужели кто-то очищает меня от этого...',
	failDeleteWord: 'Прости, я не нашёл это слово у себя и мне нечего удалять',

	// (deleteWord.js) deleteBot()
	successDeleteBot: 'Я удалил этого бота у себя. Теперь я не буду его игнорировать!',
	failDeleteBot: 'Прости, я не нашёл этого бота у себя и мне некого убирать',

	// (deleteWord.js) deleteWordRoulette()
	successDeleteRouletteWord: 'Я удалил это слово у себя. Неужели кто-то очищает меня от этого...',
	failDeleteRouletteWord: 'Прости, я не нашёл это слово у себя и мне нечего удалять',

	// (getHelp.js) sendHelpMessage()
	helpMessage: 'Доступные команды бота:' +
	'\n\n**ху** - выбирает рандомного пользователя и показывает ему рандомное предложение из массива слов' +
	'\n **шип** - шипперит двух рандомных пользователей и скрепляет их с помощью спаренного имени' +
	'\n *макар* - возвращает предложение "Улыбок тебе дед [перевёрнутое предложение]"' +
	'\n **рулетка** - запускает игру в русскую рулетку' +
	'\n**рандом** - получение рандомного числа' +
	'\n**йа** - аналог команды `/me`' +
	'\n**цуефа** - игра в "Камень Ножницы Бумага"' +
	'\n**полл** - создаёт простейшее голосование с выборами голосов "За" и "Против"' +
	'\n**хелп** - выводит информацию с командами *(то, что вы видите сейчас)*' +
	'\n**uptime** - выводит сколько бот проработал с последнего запуска на сервере' +
	'\n\n*Сообщение удалится автоматически через 20 секунд*',

	// (getRandomWord.js) getRandomWord()
	warningForSpam: 'куда спамиш?',

	// (getUptime.js) getUptime()
	uptimeText: 'Я не спал уже на протяжении',

	// (randomNumber.js) randomNumber()
	randomNumberText: 'Рандомное число от 1 до',
	randomNumberWithRangeTextPart1: 'Рандомное число от',
	randomNumberWithRangeTextPart2: 'до',
	noRangeWarning: 'к сожалению, я не получил аргументов для вывода рандома. повторите, ещё раз',
	wrongSingleRangeNumberWarning: 'я не могу выдать рандомное число от 1 до ',
	equalSingleRangeNumberWarning: 'в каком месте рандом от 1 до 1 является рандомом?',
	wrongRangeNumberWarning1: 'я не могу выдать рандомное число от ',
	wrongRangeNumberWarning2: ' до ',
	equalRangeNumberWarning1: 'в каком месте рандом от ',
	equalRangeNumberWarning2: ' до ',
	equalRangeNumberWarning3: ' является рандомом?',
	wrongArgumentWarning: 'один или более аргументов введены неправильно *(Пример вызова команды: рандом 6 или рандом 43 88)*',

	// (randomShip.js) randomShipping()
	shipSendPart1: '**Парочка дня на сегодня: **',
	shipSendPart2: ' \:two_hearts:\n\n*Следующий шиппинг будет доступен ',

	// (randomShip.js) customShipping()
	customShippingMessage: 'Данная парочка смело бы называлась -',
	warnBotShipping: 'Я бы не стал использовать ботов в шиппинге *(И вам не стоит)*',

	// (randomShip.js) shipSkip()
	shipInfoMessage: 'Результаты шиппинга сброшены! *(Вы разлучили, возможно, великолепную парочку!)*',

	// (rspGame.js) rspGameBot()
	gameDraw1: 'Так как у нас обоих ',
	gameDraw2: ', то у нас ничья!',
	defaultPart: 'Эй, ',
	userWinsR: '. Ты победил, потому что у меня был ',
	userWinsP: '. Ты победил, потому что у меня была ',
	userWinsS: '. Ты победил, потому что у меня были ',
	botWinsR: '. А я вот победил, потому что у меня был ',
	botWinsP: '. А я вот победил, потому что у меня была ',
	botWinsS: '. А я вот победил, потому что у меня были ',

	// russianRoulette.js
	rouletteWinWarning: '*мертвая тишина*',
	rouletteLoseWarning: '**БАХ**',
	rouletteSixAndMoreBulletsWarning: 'если вдруг ты не знаешь, то напомним!\nПо правилам русской рулетки, можно брать только до 6 патронов',
	rouletteSixBulletsWarning: 'поздравляем! теперь у нас на одного суицидника меньше. им был ты!!!',

	// (userChecker.js) userChecker()
	noneSomeone1: ' сегодня не ',
	noneSomeone2: ' :c',
	fullSomeone1: ' кто бы мог подумать то!\nТы ',
	fullSomeone2: ' на ',
	someonePercent: '%!',
	someoneDefaultPart: ' на ',

	// (getDayString.js) getDayString()
	mondayText: 'в Понедельник*',
	tuesdayText: 'во Вторник*',
	wednesdayText: 'в Среду*',
	thursdayText: 'в Четверг*',
	fridayText: 'в Пятницу*',
	saturdayText: 'в Субботу*',
	sundayText: 'в Воскресенье*',

	// (initRunMessages.js) initRunMessages()
	shipFirstRunArray: ['*чтож...*', '**МОРЕ ВОЛНУЕТСЯ РАЗ**', '**МОРЕ ВОЛНУЕТСЯ ДВА**', '**МОРЕ ВОЛНУЕТСЯ ТРИ**', '**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ **'],
};
