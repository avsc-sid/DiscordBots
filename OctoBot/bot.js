const data = require("./data.json");
const Discord = require("discord.js"); const MessageEmbed = require('discord.js');
const client = new Discord.Client();
let embedding = new Discord.MessageEmbed()


client.login("token");

client.on("ready", function() {
  console.log("Bot is ready");
});

client.on("message", async function (message) {
  if (!data[message.guild.id]) data[message.guild.id] = {};
  if (!data[message.guild.id].prefix) data[message.guild.id].prefix = "oc!";
  if (message.content[0]+message.content[1]+message.content[2] !== "oc!") return;
  else {
  if (message.author.bot || message.guild == undefined) return null;
  if (!message.content.toLowerCase(data[message.guild.id].prefix)) return null;



  const args = message.content.slice(data[message.guild.id].prefix.length).split(" ");


  const cmd = args.shift().toLowerCase();

  const command = (...aliases) => {return aliases.includes(cmd)}

  let eee = message.content.slice(data[message.guild.id].prefix.length).split("/");

  if (command("ping", "latency")) {
    let pingCmd = await message.channel.send(":ping_pong: Pong!");
    pingCmd.edit(`:ping_pong: Pong! \`${pingCmd.createdTimestamp - message.createdTimestamp}ms\``);
  }

  if (command("help", "commands")) {
    const helpthingy = new Discord.MessageEmbed()
    .setTitle("oc! is the prefix. Here is a list of commands:")
    .setDescription("Note: () = required, [] = not required")
    .addField("ping", "Checks latency of the bot. \nUsage: `oc!ping`/`oc!latency` \nNotes: None")
    .addField("gaw", "Pings giveaway ping along with additional information. \nUsage: `oc!gaw (Ping Donater) / [Additional Message]` \nNotes: If you are the donater then ping yourself otherwise this will not work as intended..")
    .addField("heist", "Pings heist ping along with additional information. \nUsage: `oc!heist (Ping Donater) / (Amount) / [Additional Message]` \nNotes: If you are the donater then ping yourself otherwise this will not work as intended.")
    .addField("flashgaw", "Pings flash giveaway ping along with additional information. \nUsage: `oc!flashgaw [Ping Donater] / [Additional Message]` \nNotes: If you are the donater then ping yourself otherwise this will not work as intended.")
    .addField("kick", "Kicks a user from this guild. \nUsage: `oc!kick (Ping User)` \nNotes: Must be a mod to use this command, You must ping a user without perms.")
    .addField("ban", "Bans a user from this guild. \nUsage: `oc!ban (Ping User) [Reason]` \nNotes: Must be a mod to use this command, You must ping a user without perms, the reason is what it will show in the audit logs.")
    message.channel.send(helpthingy)
  }

  if (command("gaw")) {
    if (!message.member.roles.cache.has("817769900994723840")) return message.channel.send("Uh oh. You need to be a giveaway manager for this to work.");
else {
    message.channel.send("<@&815469456012214312>")
    let userE = message.author
    if (message.mentions.users.size > 0) (userE = message.mentions.users.first())
    let Description = null
    let Mentioned = null
    if (message.mentions.users.size > 0) Mentioned = eee.slice(1)
    else (Mentioned = eee.slice(0))
    if (Mentioned.length > 0) Description = Mentioned
    else (Description = "None")
    const gawpingy = new Discord.MessageEmbed()
    .setTitle("Looks like a new giveaway has been hosted!")
    .setDescription(`Donater: ${userE}
                     Message: ${Description}
                     Make sure you thank ${userE} in <#815474098980913192>.`)
    message.channel.send(gawpingy)
    message.delete()
  }}

  if (command("heist")) {
    if (!message.member.roles.cache.has("817769900994723840")) return message.channel.send("Uh oh. You need to be a heist manager for this to work.");
else {
    message.channel.send("<@&815469401402376192>")
    let userH = message.author
    if (message.mentions.users.size > 0) (userH = message.mentions.users.first())
    let DescriptionH = null
    let Amount = null
    let msg = eee.slice(2)
    if (msg.length > 0) DescriptionH = msg
    else (DescriptionH = "None")
    if (eee.length > 0) Amount = eee[1]
    else (Amount = "No Amount Mentioned")
    const heistpingy = new Discord.MessageEmbed()
    .setTitle("Looks like a new heist has been hosted!")
    .setDescription(`Donater: ${userH}
                     Amount: ${Amount}
                     Message: ${DescriptionH}
                     Make sure you thank ${userH} in <#815474098980913192>.`)
    message.channel.send(heistpingy)
    message.delete()
  }}

  if (command("flashgaw")) {
    if (!message.member.roles.cache.has("817769900994723840")) return message.channel.send("Uh oh. You need to be a giveaway manager for this to work.");
else {
    message.channel.send("<@&815469500245082113>")
    let userFG = message.author
    if (message.mentions.users.size > 0) (userE = message.mentions.users.first())
    let DescriptionFG = null
    let MentionedFG = null
    if (message.mentions.users.size > 0) MentionedFG = eee.slice(1)
    else (MentionedFG = eee.slice(0))
    if (MentionedFG.length > 0) DescriptionFG = MentionedFG
    else (DescriptionFG = "None")
    const flashpingy = new Discord.MessageEmbed()
    .setTitle("Looks like a new giveaway has been hosted!")
    .setDescription(`Donater: ${userFG}
                     Message: ${DescriptionFG}
                     Make sure you thank ${userFG} in <#815474098980913192>.`)
    message.channel.send(flashpingy)
    message.delete()
  }}
  if (message.content.startsWith('oc!ban')) {
    if (!message.member.hasPermission("BAN_MEMBERS")) return message.channel.send("Imagine trying to ban without perms");
    else {
      if (!message.guild.me.hasPermission("BAN_MEMBERS")) return message.channel.send("I need something called `perms` idiot.");
      else{
    const userq = message.mentions.users.first();
   const msgee = args.slice(1)
    if (userq) {

      const memberq = message.guild.member(userq);

      if (memberq) {

        memberq.ban({time: eee[0], reason: eee[1]}).then(function () {

            message.reply(`Successfully beaned ${userq.tag} with reason: ${eee[1]}! We won't see them again.`);
          }).catch(function () {

            message.reply("Uh hello? I can't ban them. They prolly have admin or smth");
          });
      }

    } else {
      message.reply('Nothing to ban? Bruh...');
    }}}}

    if (message.content.startsWith('oc!kick')) {
      if (!message.member.hasPermission("KICK_MEMBERS")) return message.channel.send("Imagine trying to ban without perms");
      else {
        if (!message.guild.me.hasPermission("KICK_MEMBERS")) return message.channel.send("I need something called `perms` idiot.");
        else {
      const user = message.mentions.users.first();
      if (user) {
        const member = message.guild.member(user);

        if (member) {

          member.kick().then(function () {

              message.reply(`Successfully yeeted ${user.tag}! Hopefully we won't see them again.`);
            }).catch(function () {

                message.reply("Uh hello? I can't kick them. They prolly have admin or smth");
              });

            }

      } else {
        message.reply('Nothing to kick? Bruh...');
     }}}}
}})
console.log(816677218189049866)
