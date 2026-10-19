
(function(){
  var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var mem=0;
  function getCount(){try{return parseInt(localStorage.getItem('nestling-basket')||'0',10)||0}catch(e){return mem}}
  function setCount(n){mem=n;try{localStorage.setItem('nestling-basket',String(n))}catch(e){}var c=$('#basket-count');if(c)c.textContent=n}
  setCount(getCount());
  var tt;function toast(t){var el=$('#toast');if(!el)return;el.textContent=t;el.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){el.classList.remove('on')},2600)}
  // add to basket
  var add=$('#add');if(add)add.addEventListener('click',function(){setCount(getCount()+1);toast(add.dataset.name+' added. Checkout is switched off: Nestling is a fictional shop.')});
  // filters
  var chips=$$('.chip');
  function applyFilter(k){chips.forEach(function(c){c.setAttribute('aria-pressed',c.dataset.filter===k?'true':'false')});$$('.pcard').forEach(function(p){p.hidden=!(k==='all'||p.dataset.cat===k)})}
  chips.forEach(function(c){c.addEventListener('click',function(){applyFilter(c.dataset.filter)})});
  var h=(location.hash||'').replace('#','');if(chips.length&&h&&chips.some(function(c){return c.dataset.filter===h}))applyFilter(h);
  // "why this message" in the hero
  var wb=$('#why-btn');if(wb)wb.addEventListener('click',function(){var p=$('#why-panel'),o=p.hidden;p.hidden=!o;wb.setAttribute('aria-expanded',String(o))});
  // arrived from a Nest Helper link
  var from=$('#from');if(from){var q=new URLSearchParams(location.search),m=q.get('utm_medium'),s=q.get('utm_source');
    var map={refill:'a refill reminder',sizeup:'a size-up reminder',milestone:'a milestone message',winback:'a welcome-back message',reorder:'your reorder'};
    if(s==='livechat'&&m){from.hidden=false;from.textContent='You came from Nest Helper ('+(map[m]||m)+').'}}
  // only-held toggle
  var oh=$('#only-held');if(oh)oh.addEventListener('change',function(){$$('#tbl tbody tr.sent').forEach(function(r){r.hidden=oh.checked})});
})();
