const $ = sel => document.querySelector(sel);
const $$ = sel => Array.from(document.querySelectorAll(sel));

const messagesEl = $('#messages');
const inputEl = $('#input');
const sendBtn = $('#send');
const aiBtn = $('#ai');
const cardsBtn = $('#cards');
const flashModal = $('#flash-modal');
const flashList = $('#flash-list');
const closeFlash = $('#close-flash');

let history = [];

function appendMessage(text, who='bot'){
  const el = document.createElement('div');
  el.className = 'msg ' + (who==='user'?'user':'bot');
  el.innerHTML = `<div class="body">${escapeHtml(text)}</div>`;
  const meta = document.createElement('div'); meta.className='meta'; meta.textContent = new Date().toLocaleTimeString();
  el.appendChild(meta);
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setLoading(flag){
  if(flag){ sendBtn.textContent='Sending…'; sendBtn.disabled = true; }
  else { sendBtn.textContent='Send'; sendBtn.disabled = false; }
}

function escapeHtml(s){ return (s||'').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }

async function postAsk(q){
  const res = await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
  return await res.json();
}

async function postChat(m){
  const res = await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
  return await res.json();
}

async function loadFlash(){
  const res = await fetch('/flashcards');
  return await res.json();
}

async function send(useAI=false){
  const text = inputEl.value.trim(); if(!text) return;
  appendMessage(text,'user'); inputEl.value='';
  setLoading(true);
  try{
    let data;
    if(useAI) data = await postChat(text); else data = await postAsk(text);
    appendMessage(data.answer || 'No answer');
  }catch(err){
    appendMessage('Error: ' + String(err));
  }finally{ setLoading(false); }
}

sendBtn.addEventListener('click', ()=>send(false));
aiBtn.addEventListener('click', ()=>send(true));
inputEl.addEventListener('keydown', e=>{ if(e.key==='Enter'){ e.preventDefault(); send(false); } });

cardsBtn.addEventListener('click', async ()=>{
  flashList.innerHTML='Loading…'; flashModal.classList.remove('hidden');
  const data = await loadFlash();
  flashList.innerHTML='';
  data.forEach(f=>{
    const el = document.createElement('div'); el.className='flash-item';
    el.innerHTML = `<strong>Q:</strong> ${escapeHtml(f.question)}<br/><strong>A:</strong> ${escapeHtml(f.answer)}`;
    flashList.appendChild(el);
  });
});

closeFlash.addEventListener('click', ()=>{ flashModal.classList.add('hidden'); });

// small UX: show a welcome message
appendMessage('Hello! Ask me about matches (try examples on the right). I can answer from the dummy DB or use AI if enabled.');
