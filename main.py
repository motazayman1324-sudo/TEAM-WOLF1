const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates
    ]
});

// نخزن وقت دخول كل عضو
const voiceJoinTimes = new Map();

client.once('ready', () => {
    console.log(`Bot logged in as ${client.user.tag}`);
});

client.on('voiceStateUpdate', (oldState, newState) => {
    const member = newState.member;

    // دخول إلى روم صوتي
    if (!oldState.channelId && newState.channelId) {
        const joinTime = Date.now();
        voiceJoinTimes.set(member.id, joinTime);

        const joinDate = new Date(joinTime);
        const hours = joinDate.getHours().toString().padStart(2, '0');
        const minutes = joinDate.getMinutes().toString().padStart(2, '0');

        console.log(`${member.user.tag} joined voice at ${hours}:${minutes}`);
        member.send(`🎙️ Welcome ${member.user.username}! You joined voice at ${hours}:${minutes}`);
    }

    // خروج من روم صوتي
    if (oldState.channelId && !newState.channelId) {
        const joinTime = voiceJoinTimes.get(member.id);
        if (joinTime) {
            const durationMs = Date.now() - joinTime;
            const durationMinutes = Math.floor(durationMs / 60000);
            const durationSeconds = Math.floor((durationMs % 60000) / 1000);

            console.log(`${member.user.tag} left after ${durationMinutes}m ${durationSeconds}s`);
            member.send(`👋 ${member.user.username}, you stayed in voice for ${durationMinutes}m ${durationSeconds}s`);

            voiceJoinTimes.delete(member.id);
        }
    }
});

 bot.run(TOKEN)

