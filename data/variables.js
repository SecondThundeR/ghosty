exports.vars = {
	// (getRandomWordFromArray.js) spamCheck()
	spammerID: '',
	spammerCount: 0,

	// (getRandomThing.js) randomGoroscope()
	goroDate: '',
	goroTextFull: '',
	goroTextShort: '',
	randomUserInfoGoro: '',
	randomUsernameGoro: '',
	goroActivated: false,
	goroInActive: false,

	// (getRandomThing.js) randomShipping()
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

	// (getRandomThing.js) randomGay()
	gayDate: '',
	gayTextFull: '',
	gayTextShort: '',
	randomUserInfoGay: '',
	randomUsernameGay: '',
	gayActivated: false,
	gayInActive: false,

	// (getRandomThing.js) randomAnime()
	animeDate: '',
	animeTextFull: '',
	animeTextShort: '',
	randomUserInfoAnime: '',
	randomUsernameAnime: '',
	animeActivated: false,
	animeInActive: false,

	// (getRandomThing.js) randomAlina()
	alinaDate: '',
	alinaTextFull: '',
	alinaTextShort: '',
	randomUserInfoAlina: '',
	randomUsernameAlina: '',
	alinaActivated: false,
	alinaInActive: false,

	// (getRandomThing.js) randomVlad()
	vladDate: '',
	vladTextFull: '',
	vladTextShort: '',
	randomUserInfoVlad: '',
	randomUsernameVlad: '',
	vladActivated: false,
	vladInActive: false,
};

exports.ignorelist = {
	// Currenly, this section is empty, but you can add someone, which you want to ignore, when triggering command (Also, currenty there is no check for ignore, but this part is easy to add)
};

exports.text = {
	// (main.js) client.on('ready)
	activityName: 'Helltaker',

	// addWord.js + deleteWord.js
	notFoundFileRoulette: 'Я не нашёл такого файла у меня. Пожалуйста, проверьте правильность написания аргумента!',

	// addWord.js addWord()
	successAddWord: 'Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(',
	failAddWord: 'Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего',

	// addWord.js addBot()
	successAddBot: 'Я добавил этого бота в исключения! Теперь я буду его игнорировать',
	failAddBot: 'Данный бот уже есть у меня в исключениях!',

	// addWord.js addWordRoulette()
	successAddRouletteWord: 'Я добавил это в мой словарь! Спасибо, что делаешь меня тупее :(',
	failAddRouletteWord: 'Я бы ответил что-нибудь остроумное, но это слово у меня уже есть, мне добавлять нечего',

	// (createPoll.js) getVoteResult()
	noVotesText: '**ГОЛОСОВАНИЕ ОКОНЧЕНО!**\n\nК сожалению, я не получил никаких голосов, поэтому ничего сказать не могу(',
	hasResultText1: '**ГОЛОСОВАНИЕ ОКОНЧЕНО!**\n\nВопрос **',
	hasResultText2: '** от ',
	positiveResultText: ' был принят среди многих **положительно**!\n*Ну разве это не счастье?*',
	negativeResultText: ' был принят среди многих **отрицательно**!\n*Что ж, неудачам тоже свойственно быть*',
	noWinnerText: '**ГОЛОСОВАНИЕ ОКОНЧЕНО!**\n\nПоскольку у нас вышло одинаковое голосов, значит голосование является недействительным!\n*Победила дружба!*',

	// (createPoll.js) createPoll()
	pollText1: '**ВРЕМЯ ГОЛОСОВАНИЯ ОТ ',
	pollText2: '**\n\nВопрос: ',
	pollText3: '\n*На подумать - ',
	pollText4: ' секунд*',

	// deleteWord.js deleteWord()
	successDeleteWord: 'Я удалил это слово у себя. Неужели кто-то очищает меня от этого...',
	failDeleteWord: 'Прости, я не нашёл это слово у себя и мне нечего удалять',

	// deleteWord.js deleteBot()
	successDeleteBot: 'Я удалил этого бота у себя. Теперь я не буду его игнорировать!',
	failDeleteBot: 'Прости, я не нашёл этого бота у себя и мне некого убирать',

	// deleteWord.js deleteWordRoulette()
	successDeleteRouletteWord: 'Я удалил это слово у себя. Неужели кто-то очищает меня от этого...',
	failDeleteRouletteWord: 'Прости, я не нашёл это слово у себя и мне нечего удалять',

	/*
		Next variable is encoded in Base64 due to the inconvenience of typing a large text. For decryption, you need to use online base64 decoders

		(getHelp.js) sendHelpMessage()
	*/
	helpMessageBase64: '0JTQvtGB0YLRg9C/0L3Ri9C1INC60L7QvNCw0L3QtNGLINCx0L7RgtCwOgoKKirRhdGDKiogLSDQstGL0LHQuNGA0LDQtdGCINGA0LDQvdC00L7QvNC90L7Qs9C+INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjyDQuCDQv9C+0LrQsNC30YvQstCw0LXRgiDQtdC80YMg0YDQsNC90LTQvtC80L3QvtC1INC/0YDQtdC00LvQvtC20LXQvdC40LUg0LjQtyDQvNCw0YHRgdC40LLQsCDRgdC70L7QsgoqKtGF0YPQuNGB0LrQvtC/KiogLSDQstGL0LTQsNGR0YIg0LXQttC10LTQvdC10LLQvdGL0Lkg0LPQvtGA0L7RgdC60L7Qvywg0LrQvtGC0L7RgNGL0Lkg0LLRi9Cy0L7QtNC40YIg0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GPINC4INC00LDRkdGCINC/0YDQtdC00YHQutCw0LfQsNC90LjQtSDQtdC80YMgCioq0YjQuNC/KiogLSDRiNC40L/Qv9C10YDQuNGCINC00LLRg9GFINGA0LDQvdC00L7QvNC90YvRhSDQv9C+0LvRjNC30L7QstCw0YLQtdC70LXQuSDQuCDRgdC60YDQtdC/0LvRj9C10YIg0LjRhSDRgSDQv9C+0LzQvtGJ0YzRjiDRgdC/0LDRgNC10L3QvdC+0LPQviDQuNC80LXQvdC4Cioq0YDRg9C70LXRgtC60LAqKiAtINC30LDQv9GD0YHQutCw0LXRgiDQuNCz0YDRgyDQsiDRgNGD0YHRgdC60YPRjiDRgNGD0LvQtdGC0LrRgwoqKtGA0LDQvdC00L7QvCoqIC0g0L/QvtC70YPRh9C10L3QuNC1INGA0LDQvdC00L7QvNC90L7Qs9C+INGH0LjRgdC70LAKKirQudCwKiogLSDQsNC90LDQu9C+0LMg0LrQvtC80LDQvdC00YsgYC9tZWAKKirQs9C10LkgKNGC0LXRgdGCIHwg0LTQvdGPKSoqIC0g0LLRi9Cy0L7QtNC40YIg0YDQsNC90LTQvtC80L3QvtCz0L4g0LPQtdGPINGBINC/0YDQvtGG0LXQvdGC0LDQvNC4LCDRgtCw0LrQttC1INCy0YvQstC+0LTQuNGCINCz0LXRjyDQtNC90Y8KKirQsNC90LjQvNC1ICjRgtC10YHRgiB8INC00L3RjykqKiAtINCy0YvQstC+0LTQuNGCINGA0LDQvdC00L7QvNC90YPRjiDQsNC90LjQvNC10YjQvdC40YbRgyDRgSDQv9GA0L7RhtC10L3RgtCw0LzQuCwg0YLQsNC60LbQtSDQstGL0LLQvtC00LjRgiDQsNC90LjQvNC10YjQvdC40YbRgyDQtNC90Y8KKirQsNC70LjQvdCwICjRgtC10YHRgiB8INC00L3RjykqKiAtINCy0YvQstC+0LTQuNGCINGA0LDQvdC00L7QvNC90L7Qs9C+INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjyDRgSDQv9GA0L7RhtC10L3RgtCw0LzQuCwg0L3QsNGB0LrQvtC70YzQutC+INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjCDQkNC70LjQvdCwLCDRgtCw0LrQttC1INCy0YvQstC+0LTQuNGCINCQ0LvQuNC90YMg0LTQvdGPCioq0LLQu9Cw0LQgKNGC0LXRgdGCIHwg0LTQvdGPKSoqIC0g0LLRi9Cy0L7QtNC40YIg0YDQsNC90LTQvtC80L3QvtCz0L4g0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GPINGBINC/0YDQvtGG0LXQvdGC0LDQvNC4LCDQvdCw0YHQutC+0LvRjNC60L4g0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GMINCS0LvQsNC0LCDRgtCw0LrQttC1INCy0YvQstC+0LTQuNGCINCS0LvQsNC00LAg0LTQvdGPCioq0L/QvtC70LsgKNCy0YDQtdC80Y8gfCDRgtC10LrRgdGCICrQuNC70LgqINGC0LXQutGB0YIpKiogLSDRgdC+0LfQtNCw0ZHRgiDQv9GA0L7RgdGC0LXQudGI0LXQtSDQs9C+0LvQvtGB0L7QstCw0L3QuNC1INGBINCy0YvQsdC+0YDQsNC80Lgg0LPQvtC70L7RgdC+0LIgItCX0LAiINC4ICLQn9GA0L7RgtC40LIiCioq0YXQtdC70L8qKiAtINCy0YvQstC+0LTQuNGCINC40L3RhNC+0YDQvNCw0YbQuNGOINGBINC60L7QvNCw0L3QtNCw0LzQuCAqKNGC0L4sINGH0YLQviDQstGLINCy0LjQtNC40YLQtSDRgdC10LnRh9Cw0YEpKgoqKnVwdGltZSoqIC0g0LLRi9Cy0L7QtNC40YIg0YHQutC+0LvRjNC60L4g0LHQvtGCINC/0YDQvtGA0LDQsdC+0YLQsNC7INGBINC/0L7RgdC70LXQtNC90LXQs9C+INC30LDQv9GD0YHQutCwINC90LAg0YHQtdGA0LLQtdGA0LUKCirQodC+0L7QsdGJ0LXQvdC40LUg0YPQtNCw0LvQuNGC0YHRjyDQsNCy0YLQvtC80LDRgtC40YfQtdGB0LrQuCDRh9C10YDQtdC3IDIwINGB0LXQutGD0L3QtCo=',

	// (getRandomThing.js) randomNumber()
	randomNumberText: 'Рандомное число от 1 до',
	randomNumberWithRangeTextPart1: 'Рандомное число от',
	randomNumberWithRangeTextPart2: 'до',
	noRangeNumberWarning: 'чтобы я мог выдать тебе число, напиши, пожалуйста, после этой команды диапазон с какого по какое число я должен начать рандомить *(либо от 0 до любого другого)*',
	wrongRangeNumberWarning: '',

	// (getRandomThing.js) randomGoroscope()
	goroSendPart1: '**Гороскоп дня на сегодня: **',
	goroSendPart2: '\n\n*Следующее предсказание будет доступно ',

	// (getRandomThing.js) randomGoroscope()
	shipSendPart1: '**Парочка дня на сегодня: **',
	shipSendPart2: ' \:hearts:\n\n*Следующий шиппинг будет доступен ',

	// (getRandomThing.js) randomGay()
	gayOnText: ' гей на ',
	gayFullText: '%!\nГотов ли он служить ♂Dungeon Master\'у♂?',
	gayNoneText: '%!\nНеужели он не настоящий ♂Fucking Slave♂?',

	// (getRandomThing.js) randomAnime()
	animeOnText: ' анимешница на ',
	animeFullText: '%!\nТы настоящая кошкодевочка!',
	animeNoneText: '%!\nПохоже ты не смотрел SAO и Токийский гуль...',

	// (getRandomThing.js) randomAlina()
	alinaOnText: ' Алина на ',
	alinaFullText: '%!\nНе пора ли разлогинится?',
	alinaNoneText: '%!\nМогла бы постараться немного...',

	// (getRandomThing.js) randomVlad()
	vladOnText: ' Влад на ',
	vladNoneText: '%!\nПойман за руку как дешёвка!',
	vladFullText: '%!\nТеперь мы знаем кто один из нас!',

	// (getRandomThing.js) randomGay() + randomAnime() + randomAlina() + randomVlad()
	otherSendPart1: '**Cегодня: **',
	otherSendPart2: '\n\n*Следующяя проверка будет доступна ',
	otherDefaultText: '%!',

	// (getRandomThing.js) firstRunMessages()
	goroFirstRunArray: ['*Заглядываю в будущее...*', '*Анализирую прошлое...*', '*Живу настоящим...*', '*Что же мы получаем сегодня?*', '**Гороскоп дня на сегодня: **'],
	shipFirstRunArray: ['*чтож...*', '**МОРЕ ВОЛНУЕТСЯ РАЗ**', '**МОРЕ ВОЛНУЕТСЯ ДВА**', '**МОРЕ ВОЛНУЕТСЯ ТРИ**', '**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ **'],
	gayFirstRunArray: ['*Захожу в* ♂**Gay Party**♂', '*Ищу* ♂**Dungeon Master**♂', '*Зову нашего* ♂**Fucking Slave**♂', '*Говорю ему* ♂**Welcome to the club, buddy**♂', '**Cегодня: **'],
	animeFirstRunArray: ['*Ищу тесты на анимешницу...*', '*Вбиваю кого-то из нас...*', '*Получаю результаты...*', '*И вот что мы получаем сегодня...*', '**Cегодня: **'],
	alinaFirstRunArray: ['*Загадочность удивляет...*', '*Но что-то в ней точно есть...*', '*А что же в ней есть?...*', '*Сейчас я вам и поведаю...*', '**Cегодня: **'],
	vladFirstRunArray: ['*Кто бы что не говорил...*', '*Но мы то с вами знаем...*', '*Что никого лучше нет на свете, чем...*', '*Ладно, долой интригу!*', '**Cегодня: **'],

	// (getRandomThing.js) getNextDayString()
	mondayText: 'в Понедельник*',
	tuesdayText: 'во Вторник*',
	wednesdayText: 'в Среду*',
	thursdayText: 'в Четверг*',
	fridayText: 'в Пятницу*',
	saturdayText: 'в Субботу*',
	sundayText: 'в Воскресенье*',

	// (getRandomThing.js) customShipping()
	customShippingMessage: 'Данная парочка смело бы называлась -',
	customGoroscopeMessage: 'Гороскоп для',

	// (getRandomThing.js) customGoroscope()
	warnMessageGoro: 'Я конечно мог бы сделать гороскоп с таким именем или словом, но это выглядело бы не кошерно. Напиши тоже самое, но с упоминанием юзера',

	// (getRandomWordFromArray.js) spamChecker()
	warningForSpam: 'куда спамиш?',

	// (getUptime.js) getUptime()
	uptimeText: 'Я не спал уже на протяжении',

	// (resultsReset.js) firstRunMessages()
	infoMessages: ['Результаты шиппинга сброшены! *(Вы разлучили, возможно, великолепную парочку!)*', 'Результаты гороскопа сброшены! *(Пора гадать снова?)*', 'Результаты гея дня сброшены! *(А что же случилось с геем?...)*', 'Результаты анимешницы дня сброшены! *(И наверное сама анимешница тоже сброшена..., только тсс!)*', 'Результаты Алины дня сброшены! *(Мы больше не узнаем, кто же у нас ещё Алина в мирном чатике...)*', 'Результаты Влада дня сброшены! **(МЫ ИМЕЕМ ПОТЕРИ, НУЖНЫ НОВЫЕ РЕКРУТЫ!!!)**'],

	// russianRoulette.js
	rouletteWinWarning: '*мертвая тишина*',
	rouletteLoseWarning: '**БАХ**',
	rouletteSixAndMoreBulletsWarning: 'если вдруг ты не знаешь, то напомним!\nПо правилам русской рулетки, можно брать только до 6 патронов',
	rouletteSixBulletsWarning: 'поздравляем! теперь у нас на одного суицидника меньше. им был ты!!!',

	// (userChecker.js) gayChecker()
	noneGay: 'сегодня не гей!',
	fullGay: 'тобой бы гордился ♂Dungeon Master♂!\nТы на',
	gayPercent: '% гей!',
	gayDefaultPart: 'на',

	// (userChecker.js) animeChecker()
	noneAnime: 'сегодня не анимешница :c',
	fullAnime: 'может называть себя по праву кошкодевочкой и девочкой волшебницей!\nТы анимешница на',
	animePercent: '%!',
	animeDefaultPart: 'анимешница на',

	// (userChecker.js) alinaChecker()
	noneAlina: 'сегодня не Алина :c',
	fullAlina: 'разлогинься!\nТы Алина на',
	alinaPercent: '%!',
	alinaDefaultPart: 'Алина на',

	// (userChecker.js) vladChecker()
	noneVlad: ' сегодня не Влад :c',
	fullVlad: ' кто бы мог подумать то!\nТы Влад на ',
	vladPercent: '%!',
	vladDefaultPart: ' Влад на ',
};
