const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const fs = require('fs');
const net = require('net');
const ip = require('ip');
const nodemailer = require('nodemailer');
const inlineBase64 = require('nodemailer-plugin-inline-base64');

require('dotenv').config()

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const MAIL_TO = 'pereirapas123@gmail.com';
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.USERMAIL,
    pass: process.env.PASSWORD
  }
});
transporter.use('compile', inlineBase64());

function sendMail(base64_img) {
  transporter.sendMail({
    from: process.env.USERMAIL,
    to: MAIL_TO,
    subject: 'Alerta na câmera de segurança',
    html: `<h1>Pessoa detectada!</h1><img src="data:image/png;base64,${base64_img}">`,
  }, function(error, info){
    if (error) {
      console.log(`Erro enviando o email: ${error}`);
    } else {
      console.log('Email enviado: ' + info.response);
    }
  });
}

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

let sockets = [];

io.on('connection', (socket) => {
  sockets.push(socket);
  console.log('User connected');

  socket.on('disconnect', () => {
    sockets = sockets.filter(s => s !== socket);
    console.log('User disconnected');
  });
});

const local = net.createServer((socket) => {
  socket.on('data', event => {
    event = event.toString();

    const data = fs.readFileSync('./image.jpeg');
    const buffer = Buffer.from(data).toString('base64');
    io.emit('image', buffer);

    if(event == 'mail') {
      sendMail(buffer);
    }
  });
}).listen('/tmp/video');

server.listen(3000, () => {
  console.log(`Acesse em http://${ip.address()}:3000`);
});

process.on('SIGINT', () => {
  console.log('Encerrando o servidor...');

  local.close();
  io.close();
  server.close();

  process.exit(0);
});
