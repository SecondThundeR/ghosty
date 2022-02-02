const magicBallAnswers = [
    'Бесспорно',
    'Предрешено',
    'Никаких сомнений',
    'Определённо да',
    'Можешь быть уверен в этом',
    'Мне кажется — «да»',
    'Вероятнее всего',
    'Хорошие перспективы',
    'Знаки говорят — «да»',
    'Да',
    'Пока не ясно, попробуй снова',
    'Спроси позже',
    'Лучше не рассказывать',
    'Сейчас нельзя предсказать',
    'Сконцентрируйся и спроси опять',
    'Даже не думай',
    'Мой ответ — «нет»',
    'По моим данным — «нет»',
    'Перспективы не очень хорошие',
    'Весьма сомнительно',
];

class MagicBallUtils {
    static returnMagicBallAnswer(userQuestion) {
        const magicBallAnswer = magicBallAnswers[Math.floor(Math.random() * magicBallAnswers.length)];
        const answerMsg = `Вопрос: **${userQuestion}**\nОтвет: **${magicBallAnswer}**`;
        return answerMsg;
    }
}

exports.MagicBallUtils = MagicBallUtils;
