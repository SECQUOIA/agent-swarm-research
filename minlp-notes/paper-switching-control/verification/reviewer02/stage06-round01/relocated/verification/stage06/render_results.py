"""Generate manuscript tables from exact JSON; optionally render PDF figures."""
if not __debug__:
    raise SystemExit('Do not use -O: exact verification requires assertions.')

from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import argparse,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def decimal(x):
    x=F(x)
    with localcontext() as ctx:
        ctx.prec=40
        value=Decimal(x.numerator)/Decimal(x.denominator)
        text=format(value,'f')
        if '.' in text: text=text.rstrip('0').rstrip('.')
    # Only finite decimal public errors are passed; reject truncation.
    assert F(text)==x
    return text

def tables(data, check=False):
    def emit(name, text):
        target=HERE/name
        if check: assert target.read_text()==text, name
        else: target.write_text(text)
    rows={ (x['N'],x['budget']):x for x in data['public']}
    content=[]
    for M in (12,24,48):
        content.append(f'{M} & {decimal(F(12,M))} & '+' & '.join(decimal(rows[M,s]['error']) for s in range(4))+r' \\')
    emit('public-table.tex','\n'.join(content)[:-3]+'\n')
    content=[]
    for M in (12,24,48):
        entries=[]
        for s in (2,3):
            row=rows[M,s]; left='(' if row['lower_strict'] else '['
            entries.append(rf'${left}{decimal(row["general_lower"])},\,{decimal(row["upper"])}]$')
        content.append(f'{M} & '+' & '.join(entries)+r' \\')
    emit('certificate-table.tex','\n'.join(content)[:-3]+'\n')
    content=[]
    for row in data['controlled']:
        fields=[str(row['n']),str(row['N']),str(row['budget']),str(row['cases'])]
        for method in ('subset_dp','word_enumeration'):
            fields.extend(f'{1000*row[method][x]:.2f}' for x in ('cpu_median_s','wall_median_s'))
        content.append(' & '.join(fields)+r' \\')
    emit('controlled-table.tex','\n'.join(content)[:-3]+'\n')
    content=[]
    for row in data['scaling']:
        content.append(f'{row["n"]} & {row["N"]} & {1000*row["cpu_median_s"]:.2f} & {1000*row["wall_median_s"]:.2f}'+r' \\')
    emit('scaling-table.tex','\n'.join(content)[:-3]+'\n')
    fine=data['public_fine']; timing=data['public']
    macros={'FineWall':f'{fine["wall_median_s"]:.3f}','FineCPU':f'{fine["cpu_median_s"]:.3f}'}
    for M in (12,24,48):
        row=rows[M,3]; macros['BudgetThree'+{12:'Twelve',24:'TwentyFour',48:'FortyEight'}[M]]=f'{row["wall_median_s"]:.3f}'
    emit('timing-macros.tex','\n'.join('\\newcommand{\\'+key+'}{'+val+'}' for key,val in macros.items())+'\n')

def figures(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(1,3,figsize=(7.1,2.5),sharey=False)
    for s,ax in enumerate(axes,1):
        modes=list(range(s+2,25));k=s+1
        uniform=[float(1/(F(n)*(F(n,n-1)**k-1))) for n in modes]
        full=[max(1/(s+2),v) for v in uniform]
        ax.plot(modes,uniform,'o--',color='#3666a6',markersize=2,label='geometric one-sided term')
        ax.axhline(1/(s+2),color='#aaa',linewidth=1,label='plateau term')
        ax.plot(modes,full,color='#222',linewidth=1.6,label='exact minimax')
        ax.set_title(f'{s} switch'+('es' if s>1 else ''));ax.set_xlabel('number of modes n')
        ax.set_ylabel('error / T');ax.set_xticks([s+2,12,24]);ax.grid(alpha=.15)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,-.01))
    fig.tight_layout(rect=(0,.10,1,1));fig.savefig(ROOT/'figures/minimax-regimes.pdf',bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(7.1,2.8))
    for M,color in [(12,'#3666a6'),(24,'#d17d22'),(48,'#28855d')]:
        row=sorted((r for r in data['public'] if r['N']==M),key=lambda r:r['budget'])
        axes[0].plot([r['budget'] for r in row],[float(F(r['error'])) for r in row],'o-',label=f'{M} allowed cells',color=color,markersize=3)
    axes[0].set(xlabel='switch budget s',ylabel='exact quantized discrepancy',xticks=[0,1,2,3],title='Public profile, T = 12');axes[0].legend(frameon=False,fontsize=8)
    conv=data['uniform_convergence'];m=[r['N'] for r in conv]
    axes[1].plot(m,[float(F(r['error'])) for r in conv],'o-',label='coarse optimum U',markersize=3)
    axes[1].plot(m,[float(F(r['lower'])) for r in conv],'o--',label='clipped U − 1/M',markersize=3)
    axes[1].axhline(1/6,color='#222',label='continuous optimum 1/6',linewidth=1)
    axes[1].set(xlabel='number of coarse cells M',ylabel='discrepancy',title='Uniform input: n = 3, s = 2, T = 1');axes[1].legend(frameon=False,fontsize=8)
    for ax in axes:ax.grid(alpha=.15)
    fig.tight_layout();fig.savefig(ROOT/'figures/exact-computations.pdf',bbox_inches='tight');plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--figures',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    data=json.loads((HERE/'results.json').read_text());tables(data, args.check)
    if args.figures:figures(data)
