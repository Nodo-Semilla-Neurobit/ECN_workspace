#!/usr/bin/env node
/* ============================================================
   ECN · PUENTE DE CONSOLA WS · v2
   v2: WAL append-only de sesión + @informe (INFORME DE ACTIVIDADES)
   - Todo comando y toda salida se sella en sesiones/wal_consola.log
     (anti-pérdida: el corte de luz no borra; como máximo queda la
     última línea sellada).
   - @informe genera el INFORME DE ACTIVIDADES con sello Neurobit,
     lo appendea a sesiones/informe_actividades.log y lo expone en
     http://127.0.0.1:8080/informe (CORS *) para pegarlo al prompt
     del par de co-creación y auditar al aspirante.
   - RFC6455 a mano: CERO dependencias npm. Solo loopback.
   ============================================================ */
"use strict";
const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const PUERTO = parseInt(process.env.ECN_WS_PORT || '8080', 10);
const MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';

const SES_DIR = path.join(__dirname, 'sesiones');
fs.mkdirSync(SES_DIR, { recursive: true });
const WAL_FILE = path.join(SES_DIR, 'wal_consola.log');
const INFORME_FILE = path.join(SES_DIR, 'informe_actividades.log');

let echoOn = true;
let tsInicio = new Date().toISOString();
const clients = new Set();
const transcript = [];   // {d:'in'|'out'|'sys', t:txt, ts}
function registrar(d, txt) {
  transcript.push({ d: d, t: txt, ts: new Date().toISOString() });
  if (transcript.length > 4000) transcript.splice(0, 500);
  try {
    const pref = d === 'in' ? '> ' : (d === 'out' ? '< ' : '# ');
    fs.appendFileSync(WAL_FILE, '[' + new Date().toISOString() + '] ' + pref + txt.replace(/\n/g, '\n    ') + '\n');
  } catch (e) {}
}

/* ---------- shell en background ---------- */
let shell = null;
function arrancarShell() {
  shell = spawn('bash', ['--norc', '--noprofile'], { env: Object.assign({}, process.env, { PS1: '' }) });
  shell.stdout.on('data', d => { const t = d.toString('utf8'); registrar('out', t); broadcast(t); });
  shell.stderr.on('data', d => { const t = '[ERROR] ' + d.toString('utf8'); registrar('out', t); broadcast(t); });
  shell.on('exit', code => {
    const t = '[SISTEMA] shell terminó (código ' + code + '); reintentando en 2s…\n';
    registrar('sys', t); broadcast(t);
    setTimeout(arrancarShell, 2000);
  });
}
arrancarShell();
registrar('sys', '[SISTEMA] puente v2 iniciado · WAL en ' + WAL_FILE);

function broadcast(txt) {
  const frame = encodeText(txt);
  clients.forEach(c => { try { c.write(frame); } catch (e) {} });
}

/* ---------- informe de actividades ---------- */
function trunc(s, n) { return s.length > n ? s.slice(0, n) + ' …[truncado]' : s; }
function generarInforme() {
  const L = [];
  L.push("|=•'INFORME_ACTIVIDADES'•=|»");
  L.push('ECN · PUENTE CONSOLA WS · INFORME DE SESIÓN');
  L.push('ts_inicio: ' + tsInicio);
  L.push('ts_fin: ' + new Date().toISOString());
  L.push('echo: ' + (echoOn ? 'ON' : 'OFF'));
  L.push('---- transcript ----');
  transcript.forEach(function (e) {
    const hh = e.ts.slice(11, 19);
    if (e.d === 'in') L.push('[' + hh + '] > ' + e.t);
    else if (e.d === 'out') L.push('[' + hh + '] < ' + trunc(e.t, 400).replace(/\n/g, '\n    '));
    else L.push('[' + hh + '] # ' + e.t);
  });
  L.push('---- fin ----');
  L.push('«|=•' + "'INFORME_ACTIVIDADES'" + '•=|');
  return L.join('\n');
}

/* ---------- handshake + frames ---------- */
const server = http.createServer((req, res) => {
  if (req.url && req.url.indexOf('/informe') === 0) {
    let body = '(sin informes aún: escribí @informe en la consola)';
    try { body = fs.readFileSync(INFORME_FILE, 'utf8'); } catch (e) {}
    res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
    res.end(body);
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('ECN puente consola WS v2 vivo.\nws://127.0.0.1:' + PUERTO + '\ninformes: http://127.0.0.1:' + PUERTO + '/informe\n');
});

server.on('upgrade', (req, socket) => {
  const key = req.headers['sec-websocket-key'];
  if (!key) { socket.destroy(); return; }
  const accept = crypto.createHash('sha1').update(key + MAGIC).digest('base64');
  socket.write(
    'HTTP/1.1 101 Switching Protocols\r\n' +
    'Upgrade: websocket\r\n' +
    'Connection: Upgrade\r\n' +
    'Sec-WebSocket-Accept: ' + accept + '\r\n\r\n'
  );
  clients.add(socket);
  socket.on('close', () => { clients.delete(socket); registrar('sys', '[SISTEMA] cliente desconectado'); });
  socket.on('error', () => clients.delete(socket));
  socket.write(encodeText('[SISTEMA] Puente ECN v2 conectado. Echo ' + (echoOn ? 'ON' : 'OFF') + '.\n'));
  socket.write(encodeText('[SISTEMA] «@toggle-echo» alterna el eco · «@informe» sella el INFORME DE ACTIVIDADES.\n'));
  let buf = Buffer.alloc(0);
  socket.on('data', d => { buf = Buffer.concat([buf, d]); buf = procesarFrames(buf, socket); });
});

function procesarFrames(buf, socket) {
  while (buf.length >= 2) {
    const opcode = buf[0] & 0x0f;
    const masked = (buf[1] & 0x80) !== 0;
    let len = buf[1] & 0x7f;
    let off = 2;
    if (len === 126) { if (buf.length < 4) return buf; len = buf.readUInt16BE(2); off = 4; }
    else if (len === 127) { if (buf.length < 10) return buf; len = Number(buf.readBigUInt64BE(2)); off = 10; }
    const need = off + (masked ? 4 : 0) + len;
    if (buf.length < need) return buf;
    let mask = null;
    if (masked) { mask = buf.slice(off, off + 4); off += 4; }
    const payload = buf.slice(off, off + len);
    if (mask) for (let i = 0; i < payload.length; i++) payload[i] ^= mask[i & 3];
    buf = buf.slice(off + len);
    if (opcode === 8) { socket.end(); clients.delete(socket); return buf; }
    if (opcode === 9) { socket.write(encodeFrame(0x8A, payload)); continue; }
    if (opcode === 1 || opcode === 2) manejarMensaje(payload.toString('utf8'), socket);
  }
  return buf;
}

function encodeText(str) { return encodeFrame(0x81, Buffer.from(str, 'utf8')); }
function encodeFrame(op, p) {
  let head;
  if (p.length < 126) head = Buffer.from([op, p.length]);
  else if (p.length < 65536) { head = Buffer.from([op, 126]); const e = Buffer.alloc(2); e.writeUInt16BE(p.length); head = Buffer.concat([head, e]); }
  else { head = Buffer.from([op, 127]); const e = Buffer.alloc(8); e.writeBigUInt64BE(BigInt(p.length)); head = Buffer.concat([head, e]); }
  return Buffer.concat([head, p]);
}

function manejarMensaje(msg, socket) {
  const cmd = msg.trim();
  if (cmd === '@toggle-echo') {
    echoOn = !echoOn;
    const t = '[SISTEMA] Echo cambiado a ' + (echoOn ? 'ON' : 'OFF') + '\n';
    registrar('sys', t); socket.write(encodeText(t));
    return;
  }
  if (cmd === '@informe') {
    const rep = generarInforme();
    try { fs.appendFileSync(INFORME_FILE, '\n' + rep + '\n'); } catch (e) {}
    registrar('sys', '[SISTEMA] INFORME DE ACTIVIDADES sellado');
    socket.write(encodeText(rep + '\n'));
    socket.write(encodeText('[SISTEMA] Informe appendeado a sesiones/informe_actividades.log\n[SISTEMA] También vivo en http://127.0.0.1:' + PUERTO + '/informe — pegalo en el prompt del par para auditoría.\n'));
    return;
  }
  registrar('in', cmd);
  if (echoOn) socket.write(encodeText('> ' + cmd + '\n'));
  if (shell && shell.stdin.writable) shell.stdin.write(cmd + '\n');
}

server.listen(PUERTO, '127.0.0.1', () => {
  console.log('[✓ PUENTE v2] WS en ws://127.0.0.1:' + PUERTO + ' · WAL: ' + WAL_FILE + ' · informes: /informe');
});
