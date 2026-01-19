const Discord = require('discord.js');
const client = new Discord.Client();
const {prefix, token, bot_age, words_array, bot_info} = require()
client.on('ready', () => {
	console.log('prefix');
	console.log(token);
	console.log(words_array[0]);
	console.log(words_array[1]);
	console.log(words_array[2]);
	console.log(bot_info.name);
	console.log(bot_info.version);
	console.log(prefix);
	console.log(prefix);
	console.log(prefix);
});

client.login('token');

client.on('message', (message) => {
	console.log(message.content);
	if (message.content === '!sb ping') {
		message.channel.send('YO I AM RUNNING RIGHT NOW');
	}


});
