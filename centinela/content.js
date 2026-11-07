/* Centinela de Composición · MutationObserver → WS → inbox/
   Sella solo en quiescencia (respuesta terminada) para no saturar. */
(function(){
  "use strict";
  var WS_URL="ws://127.0.0.1:8080";
  var QUIESCENCIA=1500;           // ms sin mutar = terminada
  var ws=null, timer=null, buffer="", yaSello=false;

  function conectar(){
    try{ ws=new WebSocket(WS_URL); }catch(e){ ws=null; }
    if(ws){ ws.onclose=function(){ setTimeout(conectar,3000); }; }
    else{ setTimeout(conectar,3000); }
  }

  function sellar(){
    if(!ws||ws.readyState!==1) return;
    var cont="|=•'CAPTURA'•=|»"+JSON.stringify({
      ts:new Date().toISOString(),
      tab:document.title,
      url:location.href,
      estado:"terminada",
      texto:buffer
    })+"«|=•'CAPTURA'•=|";
    ws.send(cont);
  }

  function observar(raiz){
    var obs=new MutationObserver(function(){
      buffer=raiz.innerText;
      yaSello=false;
      clearTimeout(timer);
      timer=setTimeout(function(){ if(!yaSello){ yaSello=true; sellar(); } }, QUIESCENCIA);
    });
    obs.observe(raiz,{childList:true,subtree:true,characterData:true});
  }

  var SELECTORES=['[contenteditable="true"]','.markdown-body','#response','.response','main'];
  function iniciar(){
    for(var i=0;i<SELECTORES.length;i++){
      var n=document.querySelector(SELECTORES[i]);
      if(n){ observar(n); return; }
    }
    setTimeout(iniciar,2000);
  }

  conectar();
  iniciar();
})();
