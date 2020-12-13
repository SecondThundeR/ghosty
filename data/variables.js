exports.vars = {
	// (createPoll.js) initPoll()
	pollLocked: false,

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

	// (getRandomThing.js) randomDed()
	dedDate: '',
	dedTextFull: '',
	dedTextShort: '',
	randomUserInfoDed: '',
	randomUsernameDed: '',
	dedActivated: false,
	dedInActive: false,
};

exports.ignorelist = {
	// Currenly, this section is empty, but you can add someone, which you want to ignore, when triggering command (Also, currenty there is no check for ignore, but this part is easy to add)
};

exports.text = {
	// (main.js) client.on('ready)
	activityName: 'Helltaker',

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

	// (getHelp.js) sendHelpMessage()
	helpMessage: 'Доступные команды бота:' +
	'\n\n**ху** - выбирает рандомного пользователя и показывает ему рандомное предложение из массива слов' +
	'\n**хуископ** - выдаёт ежедневный гороскоп, который выводит пользователя и даёт предсказание ему' +
	'\n **шип** - шипперит двух рандомных пользователей и скрепляет их с помощью спаренного имени' +
	'\n **рулетка** - запускает игру в русскую рулетку' +
	'\n**рандом** - получение рандомного числа' +
	'\n**йа** - аналог команды `/me`' +
	'\n**гей (тест | дня)** - выводит рандомного гея с процентами, также выводит гея дня' +
	'\n**аниме (тест | дня)** - выводит рандомную анимешницу с процентами, также выводит анимешницу дня' +
	'\n**алина (тест | дня)** - выводит рандомного пользователя с процентами, насколько пользователь Алина, также выводит Алину дня' +
	'\n**влад (тест | дня)** - выводит рандомного пользователя с процентами, насколько пользователь Влад, также выводит Влада дня' +
	'\n**дед (тест | дня)** - выводит рандомного пользователя с процентами, насколько пользователь дед, также выводит деда дня' +
	'\n**полл (время | текст *или* текст)** - создаёт простейшее голосование с выборами голосов "За" и "Против"' +
	'\n**хелп** - выводит информацию с командами *(то, что вы видите сейчас)*' +
	'\n**uptime** - выводит сколько бот проработал с последнего запуска на сервере' +
	'\n\n*Сообщение удалится автоматически через 20 секунд*',

	// (getRandomThing.js) randomNumber()
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

	// (getRandomThing.js) randomVlad()
	dedOnText: ' дед на ',
	dedNoneText: '%!\nМы не любим молодых, уходи! Дверь там!',
	dedFullText: '%!\nТы настоящий дед!!!',


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
	dedFirstRunArray: ['*А вы знаете?*', '*Что по статистике каждый студент является дедом!*', '*Однако, вы ведь хотите узнать кто дед среди нас?*', '*Сейчас я поведаю вам...*', '**Cегодня: **'],

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
	infoMessages: ['Результаты шиппинга сброшены! *(Вы разлучили, возможно, великолепную парочку!)*', 'Результаты гороскопа сброшены! *(Пора гадать снова?)*', 'Результаты гея дня сброшены! *(А что же случилось с геем?...)*', 'Результаты анимешницы дня сброшены! *(И наверное сама анимешница тоже сброшена..., только тсс!)*', 'Результаты Алины дня сброшены! *(Мы больше не узнаем, кто же у нас ещё Алина в мирном чатике...)*', 'Результаты Влада дня сброшены! **(МЫ ИМЕЕМ ПОТЕРИ, НУЖНЫ НОВЫЕ РЕКРУТЫ!!!)**', 'Результаты деда дня сброшены! *(Дед стоит и передо мной дрочит, я ему говорю, старина, съеби нахуй, а)*'],

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

	// (userChecker.js) dedChecker()
	noneDed: ' сегодня не дед :c',
	fullDed: ' кто бы мог подумать то!\nТы дед на ',
	dedPercent: '%!',
	dedDefaultPart: ' дед на ',
};
