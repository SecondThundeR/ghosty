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

	/*
		Next variable is encoded in Base64 due to the inconvenience of typing a large text. For decryption, you need to use online base64 decoders

		(getHelp.js) sendHelpMessage()
	*/
	helpMessageBase64: '0JTQvtGB0YLRg9C/0L3Ri9C1INC60L7QvNCw0L3QtNGLINCx0L7RgtCwOgoKKirRhdGDICh3aG8pKiogLSDQstGL0LLQvtC00LjRgiDRgtC10LMg0YDQsNC90LTQvtC80L3QvtCz0L4g0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GPINGBINGA0LDQvdC00L7QvNC90YvQvCDRgdC70L7QstC+0Lwg0LjQtyDQvNCw0YHRgdC40LLQsAoqKtGF0YPQuNGB0LrQvtC/KiogLSDQtdC20LXQtNC90LXQstC90YvQuSDQs9C+0YDQvtGB0LrQvtC/LCDQstGL0LLQvtC00LjRgiDQv9C+0LvRjNC30L7QstCw0YLQtdC70Y8g0Lgg0L/RgNC10LTRgdC60LDQt9Cw0L3QuNC1INC10LzRgyAKKirRiNC40L8qKiAtINGI0LjQv9C/0LXRgNC40YIg0LTQstGD0YUg0YDQsNC90LTQvtC80L3Ri9GFINC/0L7Qu9GM0LfQvtCy0LDRgtC10LvQtdC5INC4INGB0LrRgNC10L/Qu9GP0LXRgiDQuNGFINGBINC/0L7QvNC+0YnRjNGOINGB0L/QsNGA0LXQvdC90L7Qs9C+INC40LzQtdC90LgKKirRgNGD0LvQtdGC0LrQsCoqIC0g0YHRi9Cz0YDQsNC10Lwg0LIg0YDRg9GB0YHQutGD0Y4g0YDRg9C70LXRgtC60YM/ICoo0J/QviDRg9C80L7Qu9GH0LDQvdC40Y4g0LjQs9GA0LAg0LjQtNGR0YIg0L3QsCDQvtC00L3RgyDQt9Cw0YDRj9C20LXQvdC90YPRjiDQv9GD0LvRjiwg0YPRgdGC0LDQvdC+0LLQuNGC0Ywg0LTRgNGD0LPQvtC1INGH0LjRgdC70L4g0L/Rg9C70Ywg0LzQvtC20L3QviDRgSDQv9C+0LzQvtGJ0YzRjiDQsNGA0LPRg9C80LXQvdGC0LAsINCz0LTQtSDRh9C40YHQu9C+IC0g0LrQvtC70LjRh9C10YHRgtCy0L4g0L/Rg9C70YwpKgoqKtC50LAqKiAtINCw0L3QsNC70L7QsyDQutC+0LzQsNC90LTRiyBgL21lYCAqKNCf0YDQuNC80LXRgDogYNC50LAg0YHQtdC7YCAtPiBgQFNlY29uZFRodW5kZVIg0YHQtdC7YCkqCioq0LPQtdC5ICjRgtC10YHRgiB8INC00L3RjykqKiAtINCy0YvQstC+0LTQuNGCINGA0LDQvdC00L7QvNC90L7Qs9C+INCz0LXRjyDRgSDQv9GA0L7RhtC10L3RgtCw0LzQuCwg0YLQsNC60LbQtSDQstGL0LLQvtC00LjRgiDQs9C10Y8g0LTQvdGPCioq0LDQvdC40LzQtSAo0YLQtdGB0YIgfCDQtNC90Y8pKiogLSDQstGL0LLQvtC00LjRgiDRgNCw0L3QtNC+0LzQvdGD0Y4g0LDQvdC40LzQtdGI0L3QuNGG0YMg0YEg0L/RgNC+0YbQtdC90YLQsNC80LgsINGC0LDQutC20LUg0LLRi9Cy0L7QtNC40YIg0LDQvdC40LzQtdGI0L3QuNGG0YMg0LTQvdGPCioq0LDQu9C40L3QsCAo0YLQtdGB0YIgfCDQtNC90Y8pKiogLSDQstGL0LLQvtC00LjRgiDRgNCw0L3QtNC+0LzQvdC+0LPQviDQv9C+0LvRjNC30L7QstCw0YLQtdC70Y8g0YEg0L/RgNC+0YbQtdC90YLQsNC80LgsINC90LDRgdC60L7Qu9GM0LrQviDQvtC9KC3QsCkg0JDQu9C40L3QsCwg0YLQsNC60LbQtSDQstGL0LLQvtC00LjRgiDQkNC70LjQvdGDINC00L3RjwoqKtGF0LXQu9C/KiogLSDQstGL0LLQvtC00LjRgiDQuNC90YTQvtGA0LzQsNGG0LjRjiDRgSDQutC+0LzQsNC90LTQsNC80LggKijRgtC+LCDRh9GC0L4g0LLRiyDQstC40LTQuNGC0LUg0YHQtdC50YfQsNGBKSoKKip1cHRpbWUqKiAtINCy0YvQstC+0LTQuNGCINGB0LrQvtC70YzQutC+INCx0L7RgiDQv9GA0L7RgNCw0LHQvtGC0LDQuyDRgSDQv9C+0YHQu9C10LTQvdC10LPQviDQt9Cw0L/Rg9GB0LrQsCDQvdCwINGB0LXRgNCy0LXRgNC1Cgoq0KHQvtC+0LHRidC10L3QuNC1INGD0LTQsNC70LjRgtGB0Y8g0LDQstGC0L7QvNCw0YLQuNGH0LXRgdC60Lgg0YfQtdGA0LXQtyAxMCDRgdC10LrRg9C90LQq',

	// (getRandomThing.js) randomNumber()
	randomNumberText: 'Рандомное число от 0 до',
	randomNumberWithRangeTextPart1: 'Рандомное число от',
	randomNumberWithRangeTextPart2: 'до',
	noRangeNumberWarning: 'чтобы я мог выдать тебе число, напиши, пожалуйста, после этой команды диапазон с какого по какое число я должен начать рандомить *(либо от 0 до любого другого)*',

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
