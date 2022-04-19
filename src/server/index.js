const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const fs = require('fs');
const net = require('net');

const app = express();
const server = http.createServer(app);
const io = new Server(server);
const local = net.connect('/tmp/video');

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

local.on('data', _ => {
  const data = fs.readFileSync('../camera/image.jpeg');
  const buffer = Buffer.from(data).toString('base64');
  io.emit('image', buffer);
});

server.listen(3000, () => {
  console.log('>>> http://localhost:3000');
});
