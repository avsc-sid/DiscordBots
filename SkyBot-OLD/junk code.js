// eslint-disable-next-line no-empty
if (message.content === '!sb poll') {
    if (message.content.length === 8) {
        return (message.channel.send('I need a poll query.'));
    } else {
        const text = message.content.split(' ').slice(2).join(' ');
        message.channel.send(`${message.author.username} asks: ${text}`);
    }


}
