const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('frontend.js','utf8');
const html=fs.readFileSync('6. 진단검사 확률 실험실_최종수정본.html','utf8');
const values={sampleSize:'100000',prev2:'-2',dp:'1.73',optD2:'1.73',optFn:'200',optFp:'1',optTest:'.01',optMinSe:'0',optMaxRetest:'100'};
const els={};
let plotted=0;
const canvasContext=new Proxy({},{get:(_,key)=>(...args)=>{if(key==='fillRect'||key==='arc'){assert(args.every(Number.isFinite));plotted++;}},set:()=>true});
function element(id){assert(html.includes('id="'+id+'"'),id);return els[id]??={value:values[id]??'',innerHTML:'',textContent:'',disabled:false,hidden:true,clientWidth:800,getContext:()=>canvasContext,listeners:{},labels:[{textContent:id}],checkValidity:()=>true,addEventListener(type,fn){this.listeners[type]=fn;}};}
const ctx={document:{getElementById:element},window:{devicePixelRatio:2},addEventListener:()=>{},setTimeout:fn=>fn(),Blob,URL};
vm.createContext(ctx);
vm.runInContext('const $=id=>document.getElementById(id);const sampleSize=()=>+$("sampleSize").value;'+source.split('// ROC strategy optimization: pure calculation functions.')[1],ctx);
const q={n:100000,p:.01,d1:1.73,d2:1.73,fnCost:200,fpCost:1,testCost:.01,minSe:0,maxRetest:1},a={se:.9,sp:.9};
for(const [i,cost]of [[0,30900],[1,40098],[2,22702],[3,31900]]){const r=ctx.decisionEvaluate(i,a,a,q,.9,.9);assert(Math.abs(r.cost-cost)<1e-7);assert(Math.abs(r.tp+r.fn-1000)<1e-7);assert(Math.abs(r.tn+r.fp-99000)<1e-7);}
const r=ctx.decisionSearch(q);assert.equal(r.checked,44044);assert(r.winner.cost<=r.best[0].cost);assert(r.best.every(x=>x.feasible));
assert.equal(ctx.decisionSearch({...q,minSe:1,maxRetest:0}).winner,null);
ctx.bindDecisionOptimization();element('optRun').onclick();assert(element('optSummary').innerHTML.includes('최소 손실'));assert(element('optTable').innerHTML.includes('진음성'));assert.equal(element('optExport').disabled,false);
assert.equal(element('optGraph').hidden,false);assert(plotted>44000);assert(element('optLegend').innerHTML.includes('위양성률'));
element('dp').listeners.input();assert.equal(element('optTable').innerHTML,'');assert.equal(element('optExport').disabled,true);
assert.equal(element('optGraph').hidden,true);
element('optFn').value='';element('optRun').onclick();assert(element('optStatus').textContent.includes('입력 범위'));
element('optFn').value='200';element('optMinSe').value='100';element('optMaxRetest').value='0';element('optRun').onclick();assert(element('optSummary').innerHTML.includes('만족하는 조합이 없습니다'));
assert(!fs.existsSync('roc_decision_v2.html'));
console.log('PASS: original-page integration, 90/90 costs, counts, 44,044 combinations, constraints, rendering, invalid input and stale-result clearing.');
