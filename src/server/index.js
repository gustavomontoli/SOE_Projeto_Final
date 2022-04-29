const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const fs = require('fs');
const net = require('net');
const ip = require('ip');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

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
  socket.on('data', _ => {
    const data = fs.readFileSync('../camera/image.jpeg');
    const buffer = Buffer.from(data).toString('base64');
    io.emit('image', buffer);
  });
});

local.listen('/tmp/video');

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
