const data = require("./data.json");
const Discord = require("discord.js");
const MessageEmbed = require('discord.js');
const client = new Discord.Client();

client.login("token");


client.on("ready", () => {
    console.log("Bot is ready");
  });

client.on("message", async function(message) {
  if (message.content.startsWith("sb!")) {
  if (message.channel.type === "dm") return;
  if (!data[message.guild.id]) data[message.guild.id] = {};
  if (!data[message.guild.id].prefix) data[message.guild.id].prefix = "sb!";
  if (!data[message.author.id]) data[message.author.id] = {};
  if (!data[message.author.id].tags) {
  data[message.author.id].tags = [];
  global.tagContent = []
}
  if (message.content[0]+message.content[1]+message.content[2] !== "sb!") return;
  else {
  if (message.author.bot || message.guild == undefined) return null;
  if (!message.content.toLowerCase(data[message.guild.id].prefix)) return null;

  let args = message.content.slice(data[message.guild.id].prefix.length).split(" ");

  let cmd = args.shift().toLowerCase();

  let command = (...aliases) => {return aliases.includes(cmd)}

  const colors = ["#5d8aa8", "#f0f8ff", "#e32636", "#efdecd", "#e52b50", "#ffbf00", "#ff033e", "#9966cc", "#a4c639", "#f2f3f4", "#cd9575", "#915c83"];
  const randomColors = colors[Math.floor(Math.random() * colors.length)]


  if (command("ping", "latency")) {

    let msg = await message.channel.send(":ping_pong: Pong!");
    msg.edit(`:ping_pong: Pong! \`${msg.createdTimestamp - message.createdTimestamp}ms\``);
  }

  if (command("summon")) {

     if (args[0]  === "Spikestar") message.channel.send("<@732627312805412884>, you have been summoned!")
     if (args[0]  === "Bushbush") message.channel.send("<@609769118211637270>, you have been summoned!")
     if (args[0]  === "Leafshade") message.channel.send("<@667760867483582492>, you have been summoned")
  }

  if (command("poll", "vote")) {

    if (args.length < 1)
    return message.reply("I actually need something to poll idiot");
    let text = message.content.split(' ').slice(1).join(' ');
    const voteThingy = new Discord.MessageEmbed()
    .setTitle(`${message.author.username} Asks:`)
    .setColor(randomColors)
    .setDescription(text);
    let Voting = await message.channel.send(voteThingy);
    Voting.react("✅"); Voting.react("❎");
  }

  if (command("profile")) {

    message.channel.send("Error:CommandNotFunctional");
  }

  if (command("echo", "say")) {

    if (args.length < 1)
    return message.reply("I actually need something to echo stupid.");
    let text = message.content.split(' ').slice(1).join(' ');
   message.channel.send(text);
  message.delete();
  }

  if (command("gift")) {

    message.channel.send("Try `sb!gift(50)(Spikestar)`");
  }

  if (command("help", "commands")) {
    const commandThingy = new Discord.MessageEmbed()
    .setTitle("Here is a list of commands:")
    .setColor(randomColors)
    .addField("ping", "Checks the latency of the bot.")
    .addField("help", "This :neutral_face:")
    .addField("echo", "Skybot will say whatever you want!")
    .addField("avatar", "Shows your discord avatar.")
    .addField("kick", "Kicks whoever you desire! (You need perms)")
    .addField("ban", "Bans whoever you desire! (You need perms)")
    .addField("poll", "Make a poll and have people vote!")
    .setFooter("Why would u want the commands if ur blacklisted???")
    message.channel.send(commandThingy)
    };
  }
  if (command("addtag", "addtags")) {
    if (!args[0]) return message.reply("Please provide an argument.");
    if (!args[1]) return message.reply("You cannot add an empty tag!")
    if (data[message.author.id].tags.includes(args[0])) return message.reply("You already have this tag in your list.");
    data[message.author.id].tags.push(args[0]);
    tagContent.push(args[0] + args.slice(1))
    message.reply(`Successfully added tag **${args[0]}**`);
  }

  if (command("tag", "tags")) {
    if (data[message.author.id].tags.length === 0) return message.reply("You do not have any tags.");
    message.channel.send(data[message.author.id].tags.join(", "));

  }

  if (command("removetag", "removetags")) {
    if (!data[message.author.id].tags.includes(args[0])) return message.reply("You do not have this tag.");
    else {
    for (let removeTagLoop = 0; data[message.author.id].tags[removeTagLoop] === args[0]; removeTagLoop++) {
    data[message.author.id].tags.splice(removeTagLoop, 1)
    tagContent.splice(removeTagLoop, 1)
    message.channel.reply(`Successfully removed tag **${args[0]}**`)
  }}};

  if (command("cleartag", "cleartags")) {
    message.channel.send("Are you sure you want to clear all of your tags? Respond with `yes` if you do.")
    if (message.content === "yes") {
      message.channel.send("Cleared all of your tags.")
      data[message.author.id].tags.splice(0, data[message.author.id].tags.length)
      tagContent.splice(0, tagContent.length)
    } else if (message.content === "no") message.channel.send("Did not clear all of your tags.")
  }

  if (command("displaytag", "displaytags")) {
    if (!args[0]) return message.channel.send("Please provide a valid argument.")
    if (!data[message.author.id].tags.includes(args[0])) return message.channel.send("You do not have this tag.")
    for (let displayTagLoop = 0; data[message.author.id].tags[displayTagLoop] !== tagContent[displayTagLoop].content[data[message.author.id].tags[displayTagLoop].length]; displayTagLoop++) {
    message.channel.send(tagContent[displayTagLoop])
  }}

  if (command("dm", "send")) {

    let smth = message.content.slice(data[message.guild.id].prefix.length).split("/");
    if (message.mentions.users.size === 0) return message.channel.send("I need someone to dm boi");
    else {
    if (smth[1] === 0) return message.channel.send("What do I dm them?");
    else {
      message.mentions.users.first().send(smth[1]).catch(() => message.channel.send(`Bruh ${message.mentions.users.first()} blocked me.`))
      message.delete()
    }
  }}
  if (command("kick")) {

    if (!message.member.hasPermission("KICK_MEMBERS")) return message.channel.send("Imagine trying to ban without perms");
      else {
        if (!message.guild.me.hasPermission("KICK_MEMBERS")) return (await message.channel.send("I need something called `perms` idiot.")).delete(5000);
        else {
      const user = message.mentions.users.first();
      if (user) {
        const member = message.guild.member(user);

        if (member) {

          member.kick().then(function () {

              message.reply(`Successfully yeeted ${user.tag}! Hopefully we won't see them again.`);
            }).catch(function () {

                message.reply("Uh hello? I can't kick them. They prolly have admin or smth").delete(5000);
              });

            }

      } else {
        (await message.reply('Nothing to kick? Bruh...')).delete(5000);
     }}}}

  if (command("ban")) {

    if (!message.member.hasPermission("BAN_MEMBERS")) return message.channel.send("Imagine trying to ban without perms");
    else {
      if (!message.guild.me.hasPermission("BAN_MEMBERS")) return message.channel.send("I need something called `perms` idiot.");
      else{
    const userq = message.mentions.users.first();
    const text = message.content.slice(data[message.guild.id].prefix.length).split(" ");
   const msgee = text.slice(1)
    if (userq) {

      const memberq = message.guild.member(userq);

      if (memberq === message.author) {
     message.reply("U wanna ban urself?");
      }
      else if (memberq) {
        memberq.ban({reason: msgee}).then(function () {

            message.reply(`Successfully beaned ${userq.tag} with reason: ${msgee}! We won't see them again.`);
          }).catch(function () {

            message.reply("Uh hello? I can't ban them. They prolly have admin or smth");
          });
      }

    } else {
      message.reply('Nothing to ban? Bruh...');
    }}}

  if (command("avatar")) {

    let userE = message.author
    if (message.mentions.users.size > 0) (userE = message.mentions.users.first());
      const avatarThingy = new Discord.MessageEmbed()
        // Set the title of the field
       .setTitle("Their avatar:")
        // Set the color of the embed
        .setColor(randomColors)
        // Set the main content of the embed
        .setImage(userE.avatarURL());
      // Send the embed to the same channel as the message
      message.channel.send(avatarThingy);
      }
    }}});
