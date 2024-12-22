import { env } from '../../env.js';

const ConfigData = {
    API_URL: 'https://test-web.helixsense.com',
    CHATBOT_API_URL: env.CHAT_API_URL && env.MODE !== 'development' ? env.CHAT_API_URL : 'http://localhost:5001',
};
export default ConfigData; 