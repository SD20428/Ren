const $ = id => document.getElementById(id);
const sampleSize = () => +$('sampleSize').value;
const sampleLabel = () => sampleSize().toLocaleString('ko-KR');

const PRESETS = {
  kncsp20:{se:68.93,sp:89.09,prev:0.44946,n:'KNCSP 2020: RR 11.17%, CDR 3.10/1000 전체 검사, ICR 1.57/1000 음성 검사. 분모를 맞춰 환산한 유효 사전확률 약 0.449%.'},
  kncsp09:{se:67.30,sp:82.93,prev:0.21540,n:'KNCSP 2009: RR 17.18%, CDR 1.45/1000 전체 검사, ICR 0.85/1000 음성 검사. 환산한 유효 사전확률 약 0.215%.'},
  abcs:{se:86.5,sp:81.1,prev:0.309,n:'ABCS-K 2005-2010: 공표값을 같은 방식으로 환산한 유효 사전확률 약 0.309%.'},
  ideal:{se:99,sp:99,prev:0.44946,n:'가상 검사: 민감도와 특이도를 각각 99%로 둔 교육용 예시.'}
};

async function post(path, body){
  const response=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  if(!response.ok) throw new Error(await response.text());
  return response.json();
}
function api(){
  return {
    bayes:(prevalence,sensitivity,specificity)=>post('bayes',{prevalence,sensitivity,specificity}),
    reconstruct:year=>post('reconstruct',{year}),
    roc:(separation,cutoff,prevalence,fn_weight)=>post('roc',{separation,cutoff,prevalence,fn_weight}),
    bias:(lead,slow,nonprogressive,effect)=>post('bias',{lead,slow,nonprogressive,effect})
  };
}
function setLogSlider(id,pct){ $(id).value=Math.log10(pct/100); }
function prepCanvas(cv){
  const d=window.devicePixelRatio||1,w=cv.clientWidth,h=cv.clientHeight;
  cv.width=w*d; cv.height=h*d;
  const c=cv.getContext('2d'); c.setTransform(d,0,0,d,0,0);
  return {c,w,h};
}

async function renderBayes(){
  const prev=Math.pow(10,+$('prev').value),se=+$('se').value/100,sp=+$('sp').value/100;
  $('vPrev').textContent=(prev*100).toFixed(prev<.001?4:3)+'%';
  $('vSe').textContent=(se*100).toFixed(1)+'%'; $('vSp').textContent=(sp*100).toFixed(1)+'%';
  const r=await api().bayes(prev,se,sp), scale=sampleSize()/r.N;
  const {TP,FN,TN,FP,D}=Object.fromEntries(['TP','FN','TN','FP','D'].map(key=>[key,r[key]*scale]));
  $('sampleHeading').textContent=sampleLabel()+'명으로 환산한 결과';
  $('kPPV').textContent=(r.ppv*100).toFixed(2)+'%'; $('kNPV').textContent=(r.npv*100).toFixed(2)+'%';
  $('kPos').textContent=(TP+FP).toFixed(1)+'건'; $('kFP').textContent=FP.toFixed(1)+'건';
  $('icons').innerHTML=[['진짜 양성',TP,'#24946e'],['위음성',FN,'#c95d6c'],['위양성',FP,'#e49a55'],['진짜 음성',TN,'#61777d']].map(([label,n,color])=>'<div class="mini" style="border-left:5px solid '+color+'"><h4>'+label+'</h4><div style="font-size:24px;font-weight:900;color:'+color+'">'+n.toLocaleString('ko-KR',{minimumFractionDigits:2,maximumFractionDigits:2})+'명</div><div class="hint">전체의 '+(n/sampleSize()*100).toFixed(4)+'%</div></div>').join('');
  $('t2x2').innerHTML='<tr><th>'+sampleLabel()+'명 기준</th><th>검사 양성</th><th>검사 음성</th><th>합계</th></tr><tr><td>실제 병 있음</td><td>'+TP.toFixed(2)+'</td><td>'+FN.toFixed(2)+'</td><td>'+D.toFixed(2)+'</td></tr><tr><td>실제 병 없음</td><td>'+FP.toFixed(2)+'</td><td>'+TN.toFixed(2)+'</td><td>'+(sampleSize()-D).toFixed(2)+'</td></tr><tr><td>합계</td><td>'+(TP+FP).toFixed(2)+'</td><td>'+(TN+FN).toFixed(2)+'</td><td>'+sampleLabel()+'</td></tr>';
  $('bayesNote').innerHTML='양성 판정 약 <b>'+(TP+FP).toFixed(1)+'건</b> 가운데 진짜 양성은 <b>'+TP.toFixed(2)+'건</b>입니다. 진짜 양성 1건당 위양성은 약 <b class="big">'+(FP/Math.max(TP,1e-9)).toFixed(1)+'건</b>입니다.';
  drawPPV(r.curve,prev,r.ppv);
  if($('p-retest').style.display!=='none')renderRetest();
}

function drawPPV(curve,prev,ppv){
  const {c,w,h}=prepCanvas($('cPPV')),L=52,R=18,T=18,B=38; c.clearRect(0,0,w,h);
  c.strokeStyle='#dce8e6'; c.lineWidth=1;
  for(let y=0;y<=1;y+=.25){const py=T+(1-y)*(h-T-B);c.beginPath();c.moveTo(L,py);c.lineTo(w-R,py);c.stroke();c.fillStyle='#6e8388';c.font='11px system-ui';c.textAlign='right';c.fillText(Math.round(y*100)+'%',L-7,py+4);}
  c.strokeStyle='#2f9d8f';c.lineWidth=2.6;c.beginPath();curve.forEach(([x,y],i)=>{const px=L+(x+4)/3.7*(w-L-R),py=T+(1-y)*(h-T-B);i?c.lineTo(px,py):c.moveTo(px,py);});c.stroke();
  const px=L+(Math.log10(prev)+4)/3.7*(w-L-R),py=T+(1-ppv)*(h-T-B);c.fillStyle='#df7b67';c.beginPath();c.arc(px,py,5,0,Math.PI*2);c.fill();
  c.fillStyle='#5f777c';c.font='11px system-ui';c.textAlign='center';[-4,-3,-2,-1,-.3].forEach(v=>c.fillText((10**v*100).toFixed(v<-2?2:1)+'%',L+(v+4)/3.7*(w-L-R),h-13));c.fillText('질병 비율(로그 눈금)',(L+w-R)/2,h-1);
}

async function renderRecon(){
  const r=await api().reconstruct($('yr').value),d=r.published;
  $('tPub').innerHTML='<tr><th>지표</th><th>공표값</th><th>분모</th></tr><tr><td>재소환율 RR</td><td>'+d.RR.toFixed(2)+'%</td><td>전체 검사</td></tr><tr><td>PPV</td><td>'+d.PPV.toFixed(2)+'%</td><td>양성 검사</td></tr><tr><td>CDR</td><td>'+d.CDR.toFixed(2)+'/1000</td><td>전체 검사</td></tr><tr><td>ICR</td><td>'+d.ICR.toFixed(2)+'/1000</td><td><b>음성 검사</b></td></tr><tr><td>민감도 / 특이도</td><td>'+d.se.toFixed(2)+'% / '+d.sp.toFixed(2)+'%</td><td>질병 유무별</td></tr>';
  $('reconOut').innerHTML='<div class="kpis"><div class="kpi"><b>'+r.prev.toFixed(3)+'%</b><span>분모를 맞춘 유효 사전확률</span></div><div class="kpi"><b>'+r.se.toFixed(2)+'%</b><span>재구성 민감도</span></div><div class="kpi"><b>'+r.sp.toFixed(2)+'%</b><span>재구성 특이도</span></div><div class="kpi"><b>'+r.ppv.toFixed(2)+'%</b><span>재구성 PPV</span></div></div><table><tr><th>1,000건 기준</th><th>검사 양성</th><th>검사 음성</th></tr><tr><td>실제 암</td><td>'+r.TP.toFixed(3)+'</td><td>'+r.FN.toFixed(3)+'</td></tr><tr><td>암 아님</td><td>'+r.FP.toFixed(3)+'</td><td>'+r.TN.toFixed(3)+'</td></tr></table><div class="formula">음성 검사 = 1000 × (1 - RR) = '+r.neg.toFixed(1)+'<br>위음성 FN = ICR × 음성 검사 / 1000 = '+r.FN.toFixed(3)+'<br>민감도 = TP/(TP+FN) = '+r.se.toFixed(2)+'%</div><div class="note"><b>단순히 CDR+ICR을 더하면</b> 민감도는 '+r.naiveSe.toFixed(2)+'%가 되어 공표값 '+d.se.toFixed(2)+'%와 어긋납니다.</div>';
}

async function drawROC(){
  const d=+$('dp').value,cut=+$('cut').value,prev=10**(+$('prev2').value),W=+$('wgt').value;
  $('vD').textContent=d.toFixed(2);$('vCut').textContent=cut.toFixed(2);$('vPrev2').textContent=(prev*100).toFixed(prev<.001?4:3)+'%';$('vW').textContent=W;
  const r=await api().roc(d,cut,prev,W),best=r.best;
  $('rSe').textContent=(r.se*100).toFixed(1)+'%';$('rSp').textContent=(r.sp*100).toFixed(1)+'%';$('rAUC').textContent=r.auc.toFixed(3);$('rCost').textContent=r.cost.toFixed(1);
  const {c,w,h}=prepCanvas($('cROC')),L=48,R=22,T=18,B=38;c.clearRect(0,0,w,h);c.strokeStyle='#dce8e6';
  for(let z=0;z<=1;z+=.25){const x=L+z*(w-L-R),y=T+(1-z)*(h-T-B);c.beginPath();c.moveTo(x,T);c.lineTo(x,h-B);c.stroke();c.beginPath();c.moveTo(L,y);c.lineTo(w-R,y);c.stroke();}
  c.strokeStyle='#b7c9cd';c.setLineDash([5,5]);c.beginPath();c.moveTo(L,h-B);c.lineTo(w-R,T);c.stroke();c.setLineDash([]);c.strokeStyle='#4f8fd8';c.lineWidth=2.6;c.beginPath();r.curve.forEach(([f,s],i)=>{const x=L+f*(w-L-R),y=T+(1-s)*(h-T-B);i?c.lineTo(x,y):c.moveTo(x,y);});c.stroke();
  const dot=(se,sp,col)=>{c.fillStyle=col;c.beginPath();c.arc(L+(1-sp)*(w-L-R),T+(1-se)*(h-T-B),5,0,Math.PI*2);c.fill();};dot(r.se,r.sp,'#df7b67');dot(best.se,best.sp,'#2f9d8f');
  c.fillStyle='#61777d';c.font='11px system-ui';c.textAlign='center';c.fillText('위양성률 (1-특이도)',(L+w-R)/2,h-5);
  $('rocNote').innerHTML='현재 설정에서 비용 최소 기준값은 <b>'+best.x.toFixed(2)+'</b> (민감도 '+(best.se*100).toFixed(1)+'%, 특이도 '+(best.sp*100).toFixed(1)+'%)입니다.';
}

async function runBias(){
  const lead=+$('lead').value,slow=+$('slow').value/100,non=+$('non').value/100,eff=+$('eff').value/100;
  $('vLead').textContent=lead.toFixed(1)+'년';$('vSlow').textContent=(slow*100).toFixed(0)+'%';$('vNon').textContent=(non*100).toFixed(0)+'%';$('vEff').textContent=(eff*100).toFixed(0)+'%';
  const r=await api().bias(lead,slow,non,eff);
  $('leadMetric').innerHTML=(r.s5Effect*100).toFixed(1)+'% <span class="arrow">→</span> '+(r.leadSurvival*100).toFixed(1)+'%';$('leadText').textContent='사망 시점 분포는 그대로 두고 진단 시점만 '+lead.toFixed(1)+'년 앞당긴 모형입니다.';
  $('lengthMetric').innerHTML=(r.baseMix*100).toFixed(1)+'% <span class="arrow">→</span> '+(r.screenMix*100).toFixed(1)+'%';$('lengthText').textContent='느린 종양 비율은 전체 '+(slow*100).toFixed(0)+'% → 검진 발견암 '+(r.slowShare*100).toFixed(1)+'%입니다.';
  $('overMetric').innerHTML=(r.s5Effect*100).toFixed(1)+'% <span class="arrow">→</span> '+(r.overSurvival*100).toFixed(1)+'%';$('overText').textContent='비진행성 병변이 추가 진단되면 분모와 생존자 수가 함께 늘어납니다.';
  drawBias(r.pairs,r.baseDeaths,r.deaths);$('biasNote').innerHTML=(eff===0?'<b>실제 5년 암사망 위험 감소를 0%로 두었습니다.</b> ':'<b>진행암의 5년 사망위험 감소 효과를 반영했습니다.</b> ')+'편향에 따른 생존율 상승과 실제 사망위험 감소를 구분해 해석하세요.';
}

function drawBias(pairs,du,ds){
  const {c,w,h}=prepCanvas($('cBias')),L=48,R=26,T=30,B=54,labs=['선행시간','길이 편향','과잉진단'],cols=['#4f8fd8','#2f9d8f','#df7b67'];c.clearRect(0,0,w,h);
  for(let y=0;y<=100;y+=25){const py=T+(1-y/100)*(h-T-B);c.strokeStyle='#e1ebea';c.beginPath();c.moveTo(L,py);c.lineTo(w-R,py);c.stroke();c.fillStyle='#75878b';c.font='10px system-ui';c.textAlign='right';c.fillText(y+'%',L-6,py+3);}
  const gap=(w-L-R)/3;pairs.forEach((pair,i)=>{const bw=gap*.26,x=L+i*gap+gap*.17;[[pair[0],'#c4d0d3','기준'],[pair[1],cols[i],'편향 후']].forEach((z,j)=>{const xx=x+j*bw*1.35,bh=(h-T-B)*z[0]/100;c.fillStyle=z[1];c.fillRect(xx,h-B-bh,bw,bh);c.fillStyle='#24434a';c.font='10px system-ui';c.textAlign='center';c.fillText(z[0].toFixed(1)+'%',xx+bw/2,h-B-bh-5);c.fillText(z[2],xx+bw/2,h-B+14);});c.fillText(labs[i],L+i*gap+gap/2,h-B+32);});c.textAlign='left';c.fillText('진행암 5년 사망자(10,000 병변 가정): '+Math.round(du)+' → '+Math.round(ds),L,h-6);
}

function bind(){
  document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-pressed',x===b));['bayes','retest','recon','roc','bias'].forEach(t=>$('p-'+t).style.display=t===b.dataset.t?'grid':'none');if(b.dataset.t==='retest')renderRetest();if(b.dataset.t==='roc')drawROC();if(b.dataset.t==='bias')runBias();});
  document.querySelectorAll('[data-p]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-p]').forEach(x=>x.classList.remove('on'));b.classList.add('on');const p=PRESETS[b.dataset.p];$('se').value=p.se;$('sp').value=p.sp;setLogSlider('prev',p.prev);$('srcNote').textContent=p.n;renderBayes();});
  ['prev','se','sp'].forEach(id=>$(id).oninput=renderBayes);$('yr').onchange=renderRecon;['dp','cut','prev2','wgt'].forEach(id=>$(id).oninput=drawROC);['lead','slow','non','eff'].forEach(id=>$(id).oninput=runBias);
  addEventListener('resize',()=>{renderBayes();if($('p-roc').style.display==='grid')drawROC();if($('p-bias').style.display==='grid')runBias();});
  $('sampleSize').onchange=()=>{renderBayes();if(retestData)drawRetest();};
  $('retestTarget').onchange=()=>{retestSelected=0;if(retestData)drawRetest();};
  ['sameTest','se2','sp2'].forEach(id=>$(id).oninput=renderRetest);
  $('srcNote').textContent=PRESETS.kncsp20.n;renderBayes();renderRecon();
}

window.addEventListener('DOMContentLoaded',bind);

let retestData=null, retestSelected=0, retestRequest=0;
const retestPct = v => v===null ? '정의되지 않음' : (v*100).toFixed(4)+'%';
async function renderRetest(){
  const request=++retestRequest;
  const prevalence=10**(+$('prev').value),sensitivity=+$('se').value/100,specificity=+$('sp').value/100;
  const linked=$('sameTest').checked;
  if(linked){$('se2').value=$('se').value;$('sp2').value=$('sp').value;}
  $('se2').disabled=linked;$('sp2').disabled=linked;
  const sensitivity2=linked?sensitivity:+$('se2').value/100,specificity2=linked?specificity:+$('sp2').value/100;
  $('vSe2').textContent=(sensitivity2*100).toFixed(2)+'%';$('vSp2').textContent=(specificity2*100).toFixed(2)+'%';
  $('retestSettings').textContent='검사 전 위암 확률 '+retestPct(prevalence)+' · 1차 민감도 '+(sensitivity*100).toFixed(2)+'% · 특이도 '+(specificity*100).toFixed(2)+'%';
  try{
    const result=await post('retest',{prevalence,sensitivity,specificity,sensitivity2,specificity2});
    if(request!==retestRequest)return;
    retestData=result;$('retestError').textContent='';drawRetest();
  }catch(error){if(request!==retestRequest)return;$('retestError').textContent='계산하지 못했습니다. 설정을 변경하거나 다시 시도해 주세요.';$('retestJourney').innerHTML='';$('retestTable').innerHTML='';$('retestNote').textContent='';}
}
function drawRetest(){
  const target=$('retestTarget').value,raw={...retestData,branches:retestData.branches.map(x=>({...x,count:x.count*sampleSize()/1000,diseased:x.diseased*sampleSize()/1000}))},branches=[];
  let tested=0;
  for(const first of [true,false]){
    const group=raw.branches.filter(x=>x.first===first);
    if(target==='all'||(target==='positive'&&first)||(target==='negative'&&!first)){
      branches.push(...group);tested+=group.reduce((sum,x)=>sum+x.count,0);
    }else{
      const probability=group.reduce((sum,x)=>sum+x.probability,0);
      branches.push({first,second:null,firstPosterior:group[0].firstPosterior,
        posterior:group[0].firstPosterior,probability,count:sampleSize()*probability,
        diseased:group.reduce((sum,x)=>sum+x.diseased,0)});
    }
  }
  const r={...raw,branches};
  if(retestSelected>=branches.length)retestSelected=0;
  const b=r.branches[retestSelected],sign=v=>v?'양성':'음성';
  $('retestPopulation').textContent=sampleLabel()+'명 기준 · 2차 검사 대상 '+tested.toFixed(3)+'명 · 재검사 미실시 '+(sampleSize()-tested).toFixed(3)+'명 · 총 검사 횟수 '+(sampleSize()+tested).toFixed(3)+'회';
  const stages=[['검사 전',r.prevalence],['1차 '+sign(b.first)+' 후',b.firstPosterior],[b.second===null?'2차 미실시 · 1차 확률 유지':'2차 '+sign(b.second)+' 후',b.posterior]];
  $('retestJourney').innerHTML='<div class="split3">'+stages.map(([label,p])=>'<div class="mini"><h4>'+label+'</h4><div style="font-size:22px;font-weight:900">'+retestPct(p)+'</div><div class="hint">위암일 확률</div><div style="height:8px;background:#e5f6f2;border-radius:6px;margin-top:10px"><div style="height:100%;border-radius:6px;background:var(--mint);width:'+(p===null?0:p*100)+'%"></div></div></div>').join('')+'</div>';
  $('retestTable').innerHTML='<tr><th>결과 경로 선택</th><th>경로 발생 확률</th><th>예상 인원 / '+sampleLabel()+'명</th><th>위암 확률</th></tr>'+r.branches.map((x,i)=>'<tr style="background:'+(i===retestSelected?'#e5f6f2':'white')+'"><td><button class="b" data-route="'+i+'" aria-pressed="'+(i===retestSelected)+'">'+sign(x.first)+' → '+(x.second===null?'재검사 미실시':sign(x.second))+'</button></td><td>'+retestPct(x.probability)+'</td><td>'+x.count.toFixed(3)+'명</td><td>'+retestPct(x.posterior)+'</td></tr>').join('');
  $('retestTable').querySelectorAll('[data-route]').forEach(button=>button.onclick=()=>{retestSelected=+button.dataset.route;drawRetest();});
  $('retestNote').textContent=b.posterior===null?'이 결과 조합은 현재 설정에서 발생하지 않으므로 위암 확률을 정의할 수 없습니다.':'전체 '+sampleLabel()+'명 중 이 결과 조합은 약 '+b.count.toFixed(3)+'명, 그중 위암은 약 '+b.diseased.toFixed(3)+'명입니다. 이 조합을 얻은 사람의 위암 확률은 '+retestPct(b.posterior)+'입니다.'+(b.second===null?' 이 사람들은 2차 검사를 받지 않아 1차 결과 후 확률을 유지합니다.':'');
}
