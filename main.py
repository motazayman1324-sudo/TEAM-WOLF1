const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates
    ]
});

// تخزين وقت دخول كل عضو
const voiceJoinTimes = new Map();

client.once('ready', () => {
    console.log(`✅ تم تسجيل الدخول كبوت: ${client.user.tag}`);
});

client.on('voiceStateUpdate', (oldState, newState) => {
    const member = newState.member;

    // حالة الدخول إلى روم صوتي
    if (!oldState.channelId && newState.channelId) {
        const joinTime = Date.now();
        voiceJoinTimes.set(member.id, joinTime);

        const joinDate = new Date(joinTime);
        const hours = joinDate.getHours().toString().padStart(2, '0');
        const minutes = joinDate.getMinutes().toString().padStart(2, '0');

        console.log(`${member.user.tag} دخل الروم الصوتي الساعة ${hours}:${minutes}`);
        member.send(`🎙️ أهلاً ${member.user.username}! دخلت الروم الصوتي الساعة ${hours}:${minutes}`);
    }

    // حالة الخروج من روم صوتي
    if (oldState.channelId && !newState.channelId) {
        const joinTime = voiceJoinTimes.get(member.id);
        if (joinTime) {
            const durationMs = Date.now() - joinTime;
            const durationMinutes = Math.floor(durationMs / 60000);
            const durationSeconds = Math.floor((durationMs % 60000) / 1000);

            console.log(`${member.user.tag} خرج بعد ${durationMinutes} دقيقة و ${durationSeconds} ثانية`);
            member.send(`👋 ${member.user.username}، جلست في الروم الصوتي لمدة ${durationMinutes} دقيقة و ${durationSeconds} ثانية`);

            voiceJoinTimes.delete(member.id);
        }
    }
});

bot.run(TOKEN)
