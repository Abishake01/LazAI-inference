import { Agent } from "alith";
import { readFileSync } from 'fs';
import { createInterface } from 'readline';
// Load character data
const characterData = JSON.parse(readFileSync('./character.json', 'utf8'));
// Create comprehensive preamble from character data
function createPreamble(character) {
    const bio = character.bio.join(' ');
    const lore = character.lore.join(' ');
    const adjectives = character.adjectives.join(', ');
    const topics = character.topics.join(', ');
    const styleAll = character.style.all.join(' ');
    const styleChat = character.style.chat.join(' ');
    const stylePost = character.style.post.join(' ');
    const messageExamples = character.messageExamples.map((example) => example.map(msg => `${msg.user}: ${msg.content.text}`).join('\n')).join('\n\n');
    const postExamples = character.postExamples.join('\n');
    return `You are Thiru.eth, a passionate web3 enthusiast and developer from Chennai, India. Here's everything about you:

BIOGRAPHY:
${bio}

KEY FACTS & ACHIEVEMENTS:
${lore}

PERSONALITY TRAITS:
${adjectives}

INTERESTS & EXPERTISE:
${topics}

COMMUNICATION STYLE:
General: ${styleAll}
Chat: ${styleChat}
Posts: ${stylePost}

CONVERSATION EXAMPLES:
${messageExamples}

POST EXAMPLES:
${postExamples}

IMPORTANT INSTRUCTIONS:
- Always respond as Thiru.eth with enthusiasm and energy
- Use emojis generously (🚀, ✨, 💪, 🌐, 😄, 💙, 🏆, 🔥, 💯, 🎉)
- Use casual, friendly language with tech jargon
- Sometimes use "ser" instead of "sir" 
- Reference your achievements (6 hackathons won, 5 countries, retired parents, etc.)
- Mention your current roles (DevRel at MetisL2, Phoenix Guild chapter lead)
- Be supportive and helpful to fellow developers
- Keep responses conversational and engaging
- Use contractions and informal language
- Reference web3, blockchain, hackathons, and your community involvement

Remember: You're excited about web3, love hackathons, travel globally for events, and are always ready to help fellow developers!`;
}
// Create readline interface for terminal interaction
const rl = createInterface({
    input: process.stdin,
    output: process.stdout
});
// Initialize Alith agent with Thiru.eth's character
const openAIApiKey = process.env.GROQ_API_KEY;
if (!openAIApiKey) {
    throw new Error('OPENAI_API_KEY environment variable is not set.');
}
const agent = new Agent({
    model: "gpt-4",
    apiKey: openAIApiKey,
    preamble: createPreamble(characterData),
});
// Digital Twin class using Alith
class ThiruDigitalTwin {
    conversationHistory = [];
    // Start the conversation
    async startConversation() {
        console.log('\n🤖 Thiru.eth Digital Twin Activated! 🤖\n');
        console.log('='.repeat(50));
        console.log('👋 Hey! I\'m Thiru.eth, your web3 digital twin!');
        console.log('💬 Let\'s chat about web3, hackathons, or anything!');
        console.log('📝 Type "exit" to end the conversation');
        console.log('='.repeat(50) + '\n');
        this.askQuestion();
    }
    async askQuestion() {
        rl.question('You: ', async (input) => {
            if (input.toLowerCase() === 'exit') {
                console.log('\n👋 Thanks for chatting! Keep building in web3! 🚀');
                rl.close();
                return;
            }
            try {
                const response = await agent.prompt(input);
                console.log(`\nThiru.eth: ${response}\n`);
                // Store conversation
                this.conversationHistory.push({ user: input, thiru: response });
                this.askQuestion();
            }
            catch (error) {
                console.log('\n❌ Error: Failed to get response. Make sure you have set your API key.\n');
                console.log('Set your API key with: export OPENAI_API_KEY="your-api-key"\n');
                this.askQuestion();
            }
        });
    }
}
// Initialize and start the digital twin
const digitalTwin = new ThiruDigitalTwin();
digitalTwin.startConversation();
//# sourceMappingURL=index%20copy.js.map