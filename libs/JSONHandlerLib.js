/* eslint-disable no-undef */
'use strict';
const fs = require('fs');
const unparsedWordsArray = fs.readFileSync('./jsonArrays/array.json');
const unparsedBotIDsArray = fs.readFileSync('./jsonArrays/botIDs.json');
const unparsedWinWords = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsWin.json');
const unparsedLoseWords = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsLose.json');
const unparsedZeroWords = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsZero.json');
const unparsedMinusWords = fs.readFileSync('./jsonArrays/russianRouletteWords/rouletteWordsMinus.json');
const unparsedCommandsNames = fs.readFileSync('./jsonArrays/commandsNames.json');

function getWordsArray() {
	const parsedWordsArray = JSON.parse(unparsedWordsArray);
	return parsedWordsArray;
}

function getBotIDsArray() {
	const parsedBotIDs = JSON.parse(unparsedBotIDsArray);
	return parsedBotIDs;
}

function getRouletteArrays() {
	const parsedWinWords = JSON.parse(unparsedWinWords);
	const parsedLoseWords = JSON.parse(unparsedLoseWords);
	const parsedZeroWords = JSON.parse(unparsedZeroWords);
	const parsedMinusWords = JSON.parse(unparsedMinusWords);
	return [ parsedWinWords, parsedLoseWords, parsedZeroWords, parsedMinusWords ];
}

function getCommandsNames() {
	const parsedCommandsNames = JSON.parse(unparsedCommandsNames);
	return parsedCommandsNames;
}

function getAllArraysAndPaths() {
	const pathToMainWords = './jsonArrays/array.json';
	const pathToBotIDs = './jsonArrays/botIDs.json';
	const pathToWinWords = './jsonArrays/russianRouletteWords/rouletteWordsWin.json';
	const pathToLoseWords = './jsonArrays/russianRouletteWords/rouletteWordsLose.json';
	const pathToZeroWords = './jsonArrays/russianRouletteWords/rouletteWordsZero.json';
	const pathToMinusWords = './jsonArrays/russianRouletteWords/rouletteWordsMinus.json';
	const parsedWordsArray = JSON.parse(unparsedWordsArray);
	const parsedBotIDs = JSON.parse(unparsedBotIDsArray);
	const parsedWinWords = JSON.parse(unparsedWinWords);
	const parsedLoseWords = JSON.parse(unparsedLoseWords);
	const parsedZeroWords = JSON.parse(unparsedZeroWords);
	const parsedMinusWords = JSON.parse(unparsedMinusWords);
	return [ [ pathToMainWords, pathToBotIDs, pathToWinWords, pathToLoseWords, pathToZeroWords, pathToMinusWords ], [ parsedWordsArray, parsedBotIDs, parsedWinWords, parsedLoseWords, parsedZeroWords, parsedMinusWords ] ];
}

module.exports = { getWordsArray, getBotIDsArray, getRouletteArrays, getCommandsNames, getAllArraysAndPaths };
