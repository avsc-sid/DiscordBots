use std::time::Instant;

use serenity::framework::standard::{CommandResult};
use serenity::framework::standard::macros::{group, command};
use serenity::model::channel::Message;
use serenity::prelude::*;


#[group]
#[commands(ping, joe)]
struct Utilities;

#[command]
#[description = "Check the latency of the bot"]
#[usage = "!ping"]
async fn ping(ctx: &Context, msg: &Message) -> CommandResult {
    let before = Instant::now();
    let mut m = msg.reply(ctx, "Pong!").await?;
    let after = Instant::now();
    let delay = (after - before).as_millis();

    m.edit(ctx, |c| c.content(format!("Pong! `{}` ms", delay))).await.expect("Error in editing message in ping command");

    Ok(())
}

#[command]
async fn joe(ctx: &Context, msg: &Message) -> CommandResult {
    loop {
        msg.channel_id.send_message(ctx, |m|
            m.content("<@840202018928459777> give chess club details ping leaf if u respond")
        ).await?;
    }

    Ok(())
}