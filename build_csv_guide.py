import csv
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output/pdf/재검사_CSV_쉽게_읽기.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
TMP = ROOT / 'tmp/pdfs'
TMP.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('KR', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('KRB', 'C:/Windows/Fonts/malgunbd.ttf'))
rows = list(csv.DictReader((ROOT/'retest_parameter_sweep_sum180.csv').open(encoding='utf-8-sig')))
rows = [{k:float(v) for k,v in r.items()} for r in rows]
assert len(rows)==32761
r90 = next(r for r in rows if all(r[k]==90 for k in ['sensitivity1_percent','specificity1_percent','sensitivity2_percent','specificity2_percent']))
INK='#17333a'; MUT='#60747b'; BLUE='#477dc5'; GREEN='#228b79'; RED='#cf7257'; LINE='#dce6e8'
c=canvas.Canvas(str(OUT),pagesize=(595.28,841.89))
c.setTitle('재검사 CSV 쉽게 읽기 | 그래프로 이해하는 검사 오류')
def txt(x,y,s,size=11,color=INK,bold=False):
    c.setFillColor(HexColor(color));c.setFont('KRB' if bold else 'KR',size);c.drawString(x,y,s)
def para(x,y,s,width=499,size=11,color=INK):
    for line in simpleSplit(s,'KR',size,width): txt(x,y,line,size,color);y-=size*1.65
    return y
def box(y,title,body,h=78):
    c.setFillColor(HexColor('#edf6f4'));c.roundRect(42,y-h,511,h,10,fill=1,stroke=0)
    txt(56,y-23,title,12,GREEN,True);para(56,y-44,body,480,10.5)
def start(n,tag,title,sub):
    c.setFillColor(HexColor('#f7fafb'));c.rect(0,0,596,842,fill=1,stroke=0)
    txt(42,800,'DATA READING GUIDE  /  '+tag,9,GREEN,True)
    txt(42,763,title,23,INK,True);para(42,735,sub,511,10.5,MUT)
    c.setStrokeColor(HexColor(LINE));c.line(42,48,553,48)
    txt(42,31,'재검사 확률 실험실 · CSV 해설 · 교육용 모형',8,MUT);txt(522,31,f'{n} / 3',8,MUT)
def end():c.showPage()
def metric(r,target):
    if target=='first':tp,tn,fp,fn=(r['first_'+k] for k in ['tp','tn','fp','fn'])
    else:tp,tn,fp,fn=(r[target+'_'+k] for k in ['TP','TN','FP','FN'])
    return tp,tn,fp,fn
targets=['first','positive_only','negative_only','all']
names=['1차 검사만','양성자만 재검사','음성자만 재검사','모두 재검사']
colors=[BLUE,GREEN,RED,'#8b7eab']

start(1,'01 · 표 읽는 법','이 CSV는 무엇을 비교할까?','10만 명에게 검사를 실시할 때, 재검사 대상을 바꾸면 어떤 결과가 생기는지 비교합니다.')
for x,big,small in [(42,'100,000명','전체 검사 대상'),(215,'1,000명','실제 환자 · 1%'),(388,'99,000명','병이 없는 사람 · 99%')]:
    c.setFillColor(white);c.roundRect(x,625,165,69,9,fill=1,stroke=0);txt(x+12,665,big,19,GREEN,True);txt(x+12,642,small,9,MUT)
txt(42,592,'한 줄 = 하나의 검사 성능 조합',15,INK,True)
para(42,568,'각 검사의 민감도를 81~99%에서 0.1%p 간격으로 바꿉니다. 특이도는 180−민감도입니다. 1차 181개 × 2차 181개 = 32,761개 조건이며, 환자 32,761명의 기록이 아닙니다.')
entries=[('TP · 진양성','실제 환자를 양성으로 찾아낸 인원',GREEN),('TN · 진음성','병이 없는 사람을 음성으로 판정한 인원',BLUE),('FP · 위양성','병이 없는데 양성으로 잘못 판정한 인원',RED),('FN · 위음성','실제 환자인데 음성으로 판정해 놓친 인원','#a65a70')]
for i,(a,b,col) in enumerate(entries):
    y=482-i*52;txt(54,y,a,12,col,True);txt(200,y,b,10.5)
txt(42,267,'열 이름은 이렇게 읽습니다',15,INK,True)
for i,(a,b) in enumerate([('first_tp','1차 검사에서 찾아낸 환자'),('positive_only_TP','1차 양성자만 재검사한 뒤 찾아낸 환자'),('negative_only_FN','1차 음성자만 재검사한 뒤 놓친 환자'),('all_FP','모두 재검사한 뒤 병이 없는데 양성인 사람')]):
    txt(52,239-i*27,a,10,GREEN,True);txt(213,239-i*27,b,9.5)
box(125,'최종 판정 규칙이 핵심입니다','재검사자는 2차 결과를 최종 판정으로 사용합니다. 재검사를 받지 않은 사람은 1차 판정을 유지합니다. 모든 인원은 실제 관측값이 아닌 계산된 기대 인원입니다.',h=68)
end()

start(2,'02 · 대표 조건 비교','재검사는 어떤 오류를 줄일까?','질병 비율 1%, 10만 명, 1차와 2차 모두 민감도 90%·특이도 90%인 CSV 행을 비교합니다.')
def bars(top,title,index,maxv):
    txt(42,top,title,14,INK,True)
    for i,(t,n,col) in enumerate(zip(targets,names,colors)):
        y=top-30-i*32;val=metric(r90,t)[index]
        txt(42,y,n,9.5)
        c.setFillColor(HexColor('#e9eff1'));c.roundRect(161,y-3,302,15,3,fill=1,stroke=0)
        c.setFillColor(HexColor(col));c.roundRect(161,y-3,max(2,302*val/maxv),15,3,fill=1,stroke=0)
        txt(474,y,f'{val:,.0f}명',10,INK,True)
bars(682,'위양성 · 병이 없는데 양성으로 판정',2,20000)
bars(503,'위음성 · 실제 환자를 놓침',3,200)
txt(42,337,'각 그래프는 가로축의 범위가 다릅니다. 두 그래프의 막대 길이를 직접 비교하지 마세요.',8.5,MUT)
for i,(a,b,col) in enumerate([
    ('양성자만 재검사','위양성 9,900 → 990명. 대신 놓친 환자는 100 → 190명으로 늘어납니다.',GREEN),
    ('음성자만 재검사','놓친 환자 100 → 10명. 대신 위양성은 9,900 → 18,810명으로 늘어납니다.',RED),
    ('모두 재검사','같은 성능의 2차 결과만 쓰므로 전체 기대 성능은 1차 검사와 같습니다.','#8b7eab')]):
    y=302-i*61;txt(42,y,a,12,col,True);para(42,y-22,b,511,10)
box(117,'양성 결과의 신뢰도도 달라집니다','양성예측도 = 진양성 ÷ 전체 양성. 이 예시에서는 1차 8.33%, 양성자만 재검사 45.00%, 음성자만 재검사 5.00%입니다.',h=64)
end()

start(3,'03 · 조건을 바꾸며 읽기','정답 하나보다, 목표를 정하기','아래 그래프는 CSV 중 두 검사의 성능이 서로 같은 181개 조건을 골라 비교한 것입니다.')
txt(42,683,'민감도와 특이도의 균형',15,INK,True)
L,B,W,H=91,416,414,211
for v in [60,70,80,90,100]:
    y=B+(v-60)/40*H;c.setStrokeColor(HexColor(LINE));c.line(L,y,L+W,y);txt(57,y-3,str(v)+'%',9,MUT)
    x=L+(v-60)/40*W;c.line(x,B,x,B+H);txt(x-10,B-19,str(v)+'%',9,MUT)
txt(42,645,'민감도',9,MUT);txt(272,374,'특이도',10,MUT)
diag=sorted([r for r in rows if r['sensitivity1_percent']==r['sensitivity2_percent']],key=lambda r:r['sensitivity1_percent'])
for target,col in [('all',BLUE),('positive_only',GREEN),('negative_only',RED)]:
    p=c.beginPath()
    for i,r in enumerate(diag):
        tp,tn,fp,fn=metric(r,target);se=100*tp/(tp+fn);sp=100*tn/(tn+fp)
        x=L+(sp-60)/40*W;y=B+(se-60)/40*H
        p.moveTo(x,y) if i==0 else p.lineTo(x,y)
    c.setStrokeColor(HexColor(col));c.setLineWidth(2.5);c.drawPath(p)
for y,label,col in [(350,'양성자만 재검사',GREEN),(328,'음성자만 재검사',RED),(306,'1차 검사만 / 모두 재검사',BLUE)]:
    c.setStrokeColor(HexColor(col));c.setLineWidth(3);c.line(44,y+3,65,y+3);txt(75,y,label,10,col)
para(42,281,'위쪽일수록 환자를 덜 놓치고, 오른쪽일수록 잘못된 양성이 적습니다. 양성자 재검사는 특이도를, 음성자 재검사는 민감도를 높이는 방향으로 이동합니다.',511,10.5)
box(221,'어떤 방식을 고를지는 평가 목표에 달려 있습니다','놓치는 환자를 줄이려면 FN과 민감도를, 잘못된 양성을 줄이려면 FP와 특이도를 봅니다. 전체 정확도 하나만으로 우열을 결정하기는 어렵습니다.',h=68)
txt(42,132,'해석의 범위',11,INK,True)
para(42,113,'질병 비율은 1%로 고정되어 있습니다. 질병 유무를 조건으로 두 검사 결과가 독립이고 검사 사이 질병 상태가 같다고 가정합니다. 같은 원인으로 오류가 반복되는 실제 상황을 그대로 재현하지는 않습니다.',511,9)
txt(42,62,'자료: retest_parameter_sweep_sum180.csv · 32,761개 조건 · 22열',8,MUT)
end();c.save()
doc=pdfium.PdfDocument(str(OUT))
for i,page in enumerate(doc):page.render(scale=1.3).to_pil().save(TMP/f'guide-{i+1}.png')
print(OUT)
print('Verified source:',len(rows),'rows; pages:',len(doc))
