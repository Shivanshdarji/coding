#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
Employee Attrition Prediction — Complete Project Builder
IBM HR Analytics Dataset | Internship Week 2
Author: Shivansh

Run this script ONCE. It will:
  1. Download the IBM HR Analytics dataset
  2. Run all analysis and generate 5 charts (saved to charts/)
  3. Create analysis.ipynb — complete Jupyter Notebook with all 7 tasks
  4. Create summary.docx — non-technical HR Director summary
"""

import os, sys, warnings, urllib.request, json, datetime
warnings.filterwarnings('ignore')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)
CHARTS_DIR  = os.path.join(PROJECT_DIR, 'charts')
DATASET     = 'HR_Attrition.csv'
NOTEBOOK    = 'analysis.ipynb'
SUMMARY     = 'summary.docx'
os.makedirs(CHARTS_DIR, exist_ok=True)

print("=" * 68)
print("  🚀  Employee Attrition Prediction — Project Builder")
print("  Internship Week 2  |  IBM HR Analytics")
print("=" * 68)


# ═══════════════════════════════════════════════════════════════════════
# 1.  DOWNLOAD DATASET
# ═══════════════════════════════════════════════════════════════════════
def download_dataset():
    if os.path.exists(DATASET) and os.path.getsize(DATASET) > 50_000:
        print("\n✓ Dataset already present — skipping download.")
        return True

    print("\n📥 Downloading IBM HR Analytics Dataset...")
    sources = [
        ("GitHub dsrscientist",
         "https://raw.githubusercontent.com/dsrscientist/dataset1/master/"
         "WA_Fn-UseC_-HR-Employee-Attrition.csv"),
        ("GitHub anoubhav",
         "https://raw.githubusercontent.com/anoubhav/Coursera-IBM-Applied-AI/master/"
         "WA_Fn-UseC_-HR-Employee-Attrition.csv"),
        ("GitHub rohitgr7",
         "https://raw.githubusercontent.com/rohitgr7/attrition-prediction/master/"
         "WA_Fn-UseC_-HR-Employee-Attrition.csv"),
    ]

    for name, url in sources:
        try:
            print(f"  Trying {name} ...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            if len(data) > 50_000:
                with open(DATASET, 'wb') as f:
                    f.write(data)
                print(f"  ✓ Downloaded! ({len(data):,} bytes)")
                return True
            print(f"  ✗ File too small ({len(data)} bytes) — skipping")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print("\n⚠  Auto-download failed. Please:")
    print("   1. Visit: https://www.kaggle.com/datasets/pavansubhasht/"
          "ibm-hr-analytics-attrition-dataset")
    print("   2. Download  WA_Fn-UseC_-HR-Employee-Attrition.csv")
    print(f"  3. Rename it to '{DATASET}' and place in this folder")
    print("   4. Re-run this script")
    return False


# ═══════════════════════════════════════════════════════════════════════
# 2.  ANALYSIS + CHART GENERATION  (returns metrics dict)
# ═══════════════════════════════════════════════════════════════════════
def run_analysis():
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.metrics import (
        classification_report, confusion_matrix,
        roc_auc_score, roc_curve, f1_score,
        precision_score, recall_score, accuracy_score
    )

    print("\n" + "─" * 68)
    print("  SECTION 2 — Analysis & Chart Generation")
    print("─" * 68)

    # ── Dark premium palette ──────────────────────────────────────
    BG     = '#0f1117'
    AX_BG  = '#1a1d2e'
    GRID   = '#2a2d3e'
    TEXT   = '#e0e0e0'
    RED    = '#e74c3c'
    BLUE   = '#3498db'
    GREEN  = '#2ecc71'
    GOLD   = '#f1c40f'
    ORANGE = '#e67e22'
    TEAL   = '#1abc9c'
    PURPLE = '#9b59b6'

    plt.rcParams.update({
        'figure.facecolor': BG,   'axes.facecolor': AX_BG,
        'axes.edgecolor': GRID,   'axes.labelcolor': TEXT,
        'xtick.color': '#a0a0a0', 'ytick.color': '#a0a0a0',
        'text.color': TEXT,       'grid.color': GRID, 'grid.alpha': 0.5,
        'font.size': 11,          'axes.titlesize': 14,
        'axes.titleweight': 'bold', 'axes.titlecolor': '#ffffff',
        'legend.facecolor': AX_BG, 'legend.edgecolor': GRID,
    })

    # ── Load ──────────────────────────────────────────────────────
    df = pd.read_csv(DATASET)
    print(f"\n  Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # ── Task 1 metrics ────────────────────────────────────────────
    n_left        = int((df['Attrition'] == 'Yes').sum())
    n_stayed      = int((df['Attrition'] == 'No').sum())
    attrition_rate = n_left / len(df) * 100
    n_numeric     = len(df.select_dtypes(include=[np.number]).columns)
    n_cat         = len(df.select_dtypes(include=['object']).columns)
    null_total    = int(df.isnull().sum().sum())

    print(f"  Attrition: {n_left} left ({attrition_rate:.1f}%), {n_stayed} stayed")

    # ── Task 2: Preprocessing ─────────────────────────────────────
    df_model  = df.copy()
    drop_cols = [c for c in ['EmployeeNumber','Over18','StandardHours','EmployeeCount']
                 if c in df_model.columns]
    df_model.drop(columns=drop_cols, inplace=True)
    df_model['Attrition'] = (df_model['Attrition'] == 'Yes').astype(int)

    cat_cols    = df_model.select_dtypes(include=['object']).columns.tolist()
    df_encoded  = pd.get_dummies(df_model, columns=cat_cols, drop_first=True)

    X           = df_encoded.drop('Attrition', axis=1)
    y           = df_encoded['Attrition']
    feat_names  = X.columns.tolist()

    scaler      = StandardScaler()
    X_sc        = pd.DataFrame(scaler.fit_transform(X), columns=feat_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X_sc, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

    # ── Task 3: EDA metrics ───────────────────────────────────────
    def attr_rate(grp):
        return (grp == 'Yes').sum() / len(grp) * 100

    dept_attr   = df.groupby('Department')['Attrition'].apply(attr_rate).round(1).sort_values(ascending=False)
    role_attr   = df.groupby('JobRole')['Attrition'].apply(attr_rate).round(1).sort_values(ascending=False)
    left_income = df[df['Attrition']=='Yes']['MonthlyIncome'].mean()
    stay_income = df[df['Attrition']=='No']['MonthlyIncome'].mean()
    ot_left     = (df[df['Attrition']=='Yes']['OverTime']=='Yes').mean()*100
    ot_stay     = (df[df['Attrition']=='No']['OverTime']=='Yes').mean()*100
    wlb_left    = df[df['Attrition']=='Yes']['WorkLifeBalance'].mean()
    wlb_stay    = df[df['Attrition']=='No']['WorkLifeBalance'].mean()
    ten_left    = df[df['Attrition']=='Yes']['YearsAtCompany'].mean()
    ten_stay    = df[df['Attrition']=='No']['YearsAtCompany'].mean()

    top_dept    = dept_attr.index[0]
    top_role    = role_attr.index[0]

    print(f"  Top dept: {top_dept} ({dept_attr.iloc[0]:.1f}%)")
    print(f"  Top role: {top_role} ({role_attr.iloc[0]:.1f}%)")

    # ── Task 4: Train models ──────────────────────────────────────
    print("\n  Training models...")
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000, random_state=42, class_weight='balanced', C=1.0),
        'Random Forest': RandomForestClassifier(
            n_estimators=200, random_state=42, class_weight='balanced', n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=200, random_state=42, learning_rate=0.1,
            max_depth=5, subsample=0.8),
    }

    results = {}
    for name, mdl in models.items():
        mdl.fit(X_train, y_train)
        yp   = mdl.predict(X_test)
        yprb = mdl.predict_proba(X_test)[:, 1]
        results[name] = dict(
            model     = mdl,
            y_pred    = yp,
            y_prob    = yprb,
            accuracy  = float(accuracy_score(y_test, yp)),
            precision = float(precision_score(y_test, yp, zero_division=0)),
            recall    = float(recall_score(y_test, yp, zero_division=0)),
            f1        = float(f1_score(y_test, yp, zero_division=0)),
            roc_auc   = float(roc_auc_score(y_test, yprb)),
            cm        = confusion_matrix(y_test, yp),
            report    = classification_report(y_test, yp, target_names=['Stayed','Left']),
        )
        print(f"    ✓ {name}: F1={results[name]['f1']:.3f}  AUC={results[name]['roc_auc']:.3f}")

    best_name = max(results, key=lambda k: results[k]['roc_auc'])
    best      = results[best_name]
    best_mdl  = best['model']
    print(f"\n  Best Model → {best_name} (AUC={best['roc_auc']:.4f})")

    # Feature importance
    if hasattr(best_mdl, 'feature_importances_'):
        fi = pd.Series(best_mdl.feature_importances_, index=feat_names)
    else:
        fi = pd.Series(np.abs(best_mdl.coef_[0]), index=feat_names)
    fi_top10 = fi.sort_values(ascending=False).head(10)
    print(f"  Top features: {', '.join(fi_top10.index[:3])}")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  CHART 1 — Attrition by Department & Job Role           ║
    # ╚══════════════════════════════════════════════════════════╝
    print("\n  Generating charts...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.patch.set_facecolor(BG)

    dept_colors = [RED, ORANGE, BLUE][:len(dept_attr)]
    bars = axes[0].bar(dept_attr.index, dept_attr.values, color=dept_colors,
                       edgecolor='none', width=0.55, zorder=3)
    axes[0].set_facecolor(AX_BG)
    axes[0].set_title('Attrition Rate by Department', pad=15)
    axes[0].set_xlabel('Department', labelpad=8)
    axes[0].set_ylabel('Attrition Rate (%)', labelpad=8)
    axes[0].set_ylim(0, dept_attr.values.max() * 1.45)
    axes[0].grid(axis='y', zorder=0)
    for bar, val in zip(bars, dept_attr.values):
        axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                     f'{val:.1f}%', ha='center', va='bottom',
                     fontweight='bold', color='white', fontsize=14)

    role_srt = role_attr.sort_values(ascending=True)
    n = len(role_srt)
    cmap = plt.cm.RdYlGn_r
    rcols = [cmap(i/(n-1)) for i in range(n)]
    hbars = axes[1].barh(role_srt.index, role_srt.values,
                          color=rcols, edgecolor='none', height=0.65, zorder=3)
    axes[1].set_facecolor(AX_BG)
    axes[1].set_title('Attrition Rate by Job Role', pad=15)
    axes[1].set_xlabel('Attrition Rate (%)', labelpad=8)
    axes[1].grid(axis='x', zorder=0)
    for bar, val in zip(hbars, role_srt.values):
        axes[1].text(val+0.4, bar.get_y()+bar.get_height()/2,
                     f'{val:.1f}%', va='center', fontweight='bold', color='white', fontsize=10)

    fig.suptitle('Employee Attrition: Department & Role Breakdown',
                 fontsize=17, fontweight='bold', color='white', y=1.02)
    plt.tight_layout()
    p1 = os.path.join(CHARTS_DIR, 'chart1_attrition_by_dept_role.png')
    plt.savefig(p1, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"  ✓ Chart 1 → {p1}")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  CHART 2 — Monthly Income Boxplot + Violin              ║
    # ╚══════════════════════════════════════════════════════════╝
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor(BG)

    grp_yes = df[df['Attrition']=='Yes']['MonthlyIncome'].values
    grp_no  = df[df['Attrition']=='No']['MonthlyIncome'].values

    bp = axes[0].boxplot(
        [grp_yes, grp_no], labels=['Left  🔴','Stayed 🟢'],
        patch_artist=True, notch=True,
        medianprops=dict(color=GOLD, linewidth=3),
        whiskerprops=dict(linewidth=1.5, color='#aaa'),
        capprops=dict(linewidth=2, color='#aaa'),
        flierprops=dict(marker='o', markersize=4, alpha=0.5),
    )
    for patch, col in zip(bp['boxes'], [RED, BLUE]):
        patch.set_facecolor(col+'44'); patch.set_edgecolor(col); patch.set_linewidth(2)
    for flier, col in zip(bp['fliers'], [RED, BLUE]):
        flier.set_markerfacecolor(col); flier.set_markeredgecolor(col)
    axes[0].set_facecolor(AX_BG)
    axes[0].set_title('Monthly Income Distribution\n(Box Plot)', pad=10)
    axes[0].set_ylabel('Monthly Income ($)')
    axes[0].grid(axis='y', alpha=0.4)
    for xpos, (g, col) in enumerate(zip(['Yes','No'], [RED, BLUE]), 1):
        mv = df[df['Attrition']==g]['MonthlyIncome'].mean()
        axes[0].text(xpos, mv+220, f'Mean: ${mv:,.0f}',
                     ha='center', color=col, fontsize=9, fontweight='bold')

    vp = axes[1].violinplot([grp_yes, grp_no], positions=[1,2],
                             showmeans=True, showmedians=True)
    for pc, col in zip(vp['bodies'], [RED, BLUE]):
        pc.set_facecolor(col+'55'); pc.set_edgecolor(col); pc.set_linewidth(2)
    vp['cmeans'].set_color(GOLD); vp['cmedians'].set_color('white')
    axes[1].set_xticks([1,2]); axes[1].set_xticklabels(['Left 🔴','Stayed 🟢'])
    axes[1].set_facecolor(AX_BG)
    axes[1].set_title('Monthly Income Density\n(Violin Plot)', pad=10)
    axes[1].set_ylabel('Monthly Income ($)')
    axes[1].grid(axis='y', alpha=0.4)

    fig.suptitle('Monthly Income: Employees Who Left vs Stayed',
                 fontsize=16, fontweight='bold', color='white', y=1.02)
    plt.tight_layout()
    p2 = os.path.join(CHARTS_DIR, 'chart2_income_boxplot.png')
    plt.savefig(p2, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"  ✓ Chart 2 → {p2}")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  CHART 3 — Confusion Matrix + Model Comparison          ║
    # ╚══════════════════════════════════════════════════════════╝
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor(BG)

    cm     = best['cm']
    cm_pct = cm.astype(float) / cm.sum(axis=1)[:,None] * 100
    annot  = np.array([[f'{cm[i,j]}\n({cm_pct[i,j]:.1f}%)' for j in range(2)] for i in range(2)])

    sns.heatmap(cm, annot=annot, fmt='', ax=axes[0],
                cmap='RdBu_r', linewidths=2, linecolor=BG,
                xticklabels=['Stayed','Left'], yticklabels=['Stayed','Left'],
                annot_kws={'size':13,'weight':'bold'},
                cbar_kws={'label':'Count'})
    axes[0].set_title(f'Confusion Matrix\n{best_name}', pad=12)
    axes[0].set_xlabel('Predicted Label', labelpad=8)
    axes[0].set_ylabel('True Label', labelpad=8)

    met_keys   = ['accuracy','precision','recall','f1','roc_auc']
    met_labels = ['Accuracy','Precision','Recall','F1-Score','ROC-AUC']
    x      = np.arange(len(met_labels))
    width  = 0.25
    bcolors = [BLUE, GREEN, ORANGE]
    for i, (mname, bcol) in enumerate(zip(results.keys(), bcolors)):
        vals = [results[mname][k] for k in met_keys]
        axes[1].bar(x+(i-1)*width, vals, width, label=mname,
                    color=bcol, alpha=0.85, edgecolor='none', zorder=3)
    axes[1].set_facecolor(AX_BG)
    axes[1].set_title('Model Performance Comparison', pad=12)
    axes[1].set_xticks(x); axes[1].set_xticklabels(met_labels, fontsize=10)
    axes[1].set_ylim(0, 1.15); axes[1].set_ylabel('Score')
    axes[1].legend(loc='lower right', fontsize=9)
    axes[1].grid(axis='y', alpha=0.4, zorder=0)

    fig.suptitle(f'Model Evaluation — Best: {best_name}',
                 fontsize=16, fontweight='bold', color='white', y=1.02)
    plt.tight_layout()
    p3 = os.path.join(CHARTS_DIR, 'chart3_confusion_matrix.png')
    plt.savefig(p3, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"  ✓ Chart 3 → {p3}")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  CHART 4 — Top 10 Feature Importances                   ║
    # ╚══════════════════════════════════════════════════════════╝
    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(AX_BG)

    fi_asc   = fi_top10.sort_values(ascending=True)
    fi_cols  = [RED,RED,ORANGE,ORANGE,BLUE,BLUE,TEAL,TEAL,PURPLE,GREEN][::-1][:len(fi_asc)]

    bars_fi  = ax.barh(fi_asc.index, fi_asc.values,
                        color=fi_cols[::-1], edgecolor='none', height=0.65, zorder=3)
    ax.set_title(f'Top 10 Feature Importances Driving Attrition\n({best_name})', pad=15)
    ax.set_xlabel('Importance Score', labelpad=8)
    ax.grid(axis='x', zorder=0, alpha=0.4)
    for bar, val in zip(bars_fi, fi_asc.values):
        ax.text(val+fi_top10.max()*0.01, bar.get_y()+bar.get_height()/2,
                f'{val:.5f}', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(0.98, 0.02, f'⭐ Top Predictor: {fi_top10.index[0]}',
            transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
            color=RED, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=AX_BG, edgecolor=RED))
    plt.tight_layout()
    p4 = os.path.join(CHARTS_DIR, 'chart4_feature_importance.png')
    plt.savefig(p4, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"  ✓ Chart 4 → {p4}")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  CHART 5 (Bonus) — ROC Curve All 3 Models               ║
    # ╚══════════════════════════════════════════════════════════╝
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(AX_BG)

    roc_cols  = [BLUE, GREEN, ORANGE]
    roc_stls  = ['-','--','-.']
    for (rname, rr), rcol, rst in zip(results.items(), roc_cols, roc_stls):
        fpr, tpr, _ = roc_curve(y_test, rr['y_prob'])
        ax.plot(fpr, tpr, color=rcol, lw=2.5, linestyle=rst,
                label=f'{rname}  (AUC = {rr["roc_auc"]:.3f})')

    ax.plot([0,1],[0,1],'w--', lw=1.5, alpha=0.4, label='Random Baseline  (AUC = 0.500)')

    best_idx = list(results.keys()).index(best_name)
    bfpr, btpr, _ = roc_curve(y_test, best['y_prob'])
    ax.fill_between(bfpr, btpr, alpha=0.08, color=roc_cols[best_idx])

    ax.set_xlabel('False Positive Rate  (1 − Specificity)', labelpad=8)
    ax.set_ylabel('True Positive Rate  (Sensitivity / Recall)', labelpad=8)
    ax.set_title('ROC Curve — All 3 Models Compared\nHigher AUC = Better Discrimination', pad=15)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(alpha=0.3)
    ax.annotate('Optimal\nZone', xy=(0.1, 0.9), fontsize=10, color=GOLD,
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round', facecolor=AX_BG, edgecolor=GOLD, alpha=0.7))
    plt.tight_layout()
    p5 = os.path.join(CHARTS_DIR, 'chart5_roc_curve.png')
    plt.savefig(p5, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"  ✓ Chart 5 → {p5}")

    # ── Build metrics dict ────────────────────────────────────────
    top3_feats = list(fi_top10.index[:3])
    metrics = dict(
        n_rows        = int(df.shape[0]),
        n_cols        = int(df.shape[1]),
        n_left        = n_left,
        n_stayed      = n_stayed,
        attrition_rate= float(attrition_rate),
        n_numeric     = n_numeric,
        n_cat         = n_cat,
        null_total    = null_total,
        drop_cols     = drop_cols,
        cat_cols      = cat_cols,
        n_encoded_cols= int(df_encoded.shape[1]),
        train_size    = len(X_train),
        test_size     = len(X_test),
        dept_attr     = dept_attr.to_dict(),
        role_attr     = role_attr.to_dict(),
        top_dept      = top_dept,
        top_role      = top_role,
        left_income   = float(left_income),
        stay_income   = float(stay_income),
        ot_left       = float(ot_left),
        ot_stay       = float(ot_stay),
        wlb_left      = float(wlb_left),
        wlb_stay      = float(wlb_stay),
        ten_left      = float(ten_left),
        ten_stay      = float(ten_stay),
        best_model    = best_name,
        results       = {k: dict(
            accuracy  = v['accuracy'],
            precision = v['precision'],
            recall    = v['recall'],
            f1        = v['f1'],
            roc_auc   = v['roc_auc'],
            report    = v['report'],
            cm        = v['cm'].tolist(),
        ) for k, v in results.items()},
        top_features  = fi_top10.to_dict(),
        top3_feats    = top3_feats,
        feat_names    = feat_names,
        ot_ratio      = float(ot_left/ot_stay) if ot_stay else 0,
    )
    return metrics


# ═══════════════════════════════════════════════════════════════════════
# 3.  CREATE JUPYTER NOTEBOOK
# ═══════════════════════════════════════════════════════════════════════
def create_notebook(m):
    import nbformat as nbf

    print("\n" + "─" * 68)
    print("  SECTION 3 — Creating Jupyter Notebook (analysis.ipynb)")
    print("─" * 68)

    nb = nbf.v4.new_notebook()
    nb.metadata = {
        'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'},
        'language_info': {'name':'python','version':'3.x'},
    }

    cells = []
    MD = nbf.v4.new_markdown_cell
    CD = nbf.v4.new_code_cell

    # ── helper to strip leading indent from code strings ─────────
    import textwrap
    def C(src):  return CD(textwrap.dedent(src).strip())
    def M(src):  return MD(src.strip())

    # ════════════════════════════════
    # TITLE
    # ════════════════════════════════
    cells.append(M(f"""
# 🎯 Employee Attrition Prediction
## IBM HR Analytics — Machine Learning Project
### Internship Week 2  |  June 2026

---

| | |
|--|--|
| **Author** | Shivansh |
| **Dataset** | IBM HR Analytics  ({m['n_rows']:,} employees · {m['n_cols']} features) |
| **Goal** | Predict which employees are likely to leave and deliver actionable HR insights |
| **Tools** | Python · Pandas · Scikit-learn · Matplotlib · Seaborn · NumPy |

---
"""))

    # ════════════════════════════════
    # IMPORTS
    # ════════════════════════════════
    cells.append(M("## 📦 Setup — Import Libraries"))
    cells.append(C("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import warnings
        import os
        warnings.filterwarnings('ignore')

        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.metrics import (
            classification_report, confusion_matrix,
            roc_auc_score, roc_curve, f1_score,
            precision_score, recall_score, accuracy_score
        )

        os.makedirs('charts', exist_ok=True)

        # ── Dark Premium Colour Palette ──────────────────────────────────────
        BG, AX_BG = '#0f1117', '#1a1d2e'
        RED, BLUE, GREEN   = '#e74c3c', '#3498db', '#2ecc71'
        GOLD, ORANGE, TEAL = '#f1c40f', '#e67e22', '#1abc9c'
        PURPLE = '#9b59b6'

        plt.rcParams.update({
            'figure.facecolor': BG,     'axes.facecolor': AX_BG,
            'axes.edgecolor': '#3d4166','axes.labelcolor': '#e0e0e0',
            'xtick.color': '#a0a0a0',   'ytick.color': '#a0a0a0',
            'text.color': '#e0e0e0',    'grid.color': '#2a2d3e', 'grid.alpha': 0.5,
            'font.size': 11,            'axes.titlesize': 14,
            'axes.titleweight': 'bold', 'axes.titlecolor': '#ffffff',
            'legend.facecolor': '#1a1d2e', 'legend.edgecolor': '#3d4166',
        })

        print("✓ All libraries imported successfully!")
        print(f"  pandas {pd.__version__} | numpy {np.__version__} | sklearn ✓")
    """))

    # ════════════════════════════════
    # TASK 1
    # ════════════════════════════════
    cells.append(M("""
---
## ✅ Task 1 — Data Loading & Exploration

**Objective:** Load the dataset, understand its structure, and characterise the target variable (`Attrition`).
"""))
    cells.append(C("""
        # ── 1.1  Load the Dataset ────────────────────────────────────────────
        df = pd.read_csv('HR_Attrition.csv')

        print("=" * 58)
        print("  IBM HR Analytics — Dataset Overview")
        print("=" * 58)
        print(f"\\n  Shape : {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

        print("\\n📋 First 10 Rows:")
        df.head(10)
    """))
    cells.append(C("""
        # ── 1.2  Column Data Types ───────────────────────────────────────────
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols     = df.select_dtypes(include=['object']).columns.tolist()

        print(f"🔢 Numeric columns   ({len(numeric_cols)}): {numeric_cols}")
        print(f"\\n🔤 Categorical columns ({len(cat_cols)}): {cat_cols}")
    """))
    cells.append(C("""
        # ── 1.3  Target Column — Attrition ──────────────────────────────────
        print("🎯 Target column: 'Attrition'  (Yes = left, No = stayed)")
        print()
        vc = df['Attrition'].value_counts()
        print(vc.to_string())
        print()

        n_left        = (df['Attrition'] == 'Yes').sum()
        n_stayed      = (df['Attrition'] == 'No').sum()
        attrition_rate = n_left / len(df) * 100

        print(f"  Employees who LEFT    : {n_left:,}  ({attrition_rate:.2f}%)")
        print(f"  Employees who STAYED  : {n_stayed:,}  ({100-attrition_rate:.2f}%)")
        print(f"\\n  ✦ Overall Attrition Rate: {attrition_rate:.2f}%")
    """))
    cells.append(C("""
        # ── 1.4  Statistical Summary ─────────────────────────────────────────
        print("📈 Statistical Summary (Numeric Columns):")
        df.describe().round(2)
    """))

    att_r  = m['attrition_rate']
    ratio  = int(m['n_stayed']/m['n_left'])
    cells.append(M(f"""
### 📝 Task 1 — Observation

> **Dataset Size:** {m['n_rows']:,} employees · {m['n_cols']} features · {m['n_numeric']} numeric · {m['n_cat']} categorical.
>
> **Attrition Rate: {att_r:.1f}%** — Only {m['n_left']} employees out of {m['n_rows']:,} left the company.
>
> ⚠️ **The dataset is significantly imbalanced**: there are roughly **{ratio}× more employees who stayed** than those who left. A naive model that always predicts "stayed" would achieve {100-att_r:.1f}% accuracy while being completely useless at finding leavers. We must rely on **Precision, Recall, F1-Score, and ROC-AUC** for fair evaluation, and use `class_weight='balanced'` during training to compensate.
"""))

    # ════════════════════════════════
    # TASK 2
    # ════════════════════════════════
    cells.append(M("""
---
## ✅ Task 2 — Data Cleaning & Preprocessing

**Objective:** Handle nulls, drop irrelevant columns, encode the target, apply One-Hot Encoding, and scale features.
"""))
    cells.append(C("""
        # ── 2.1  Missing Values ──────────────────────────────────────────────
        null_counts = df.isnull().sum()
        print("🔍 Missing Values:")
        if null_counts.sum() == 0:
            print("  ✓ Zero null values — dataset is complete!")
        else:
            print(null_counts[null_counts > 0])
        print(f"\\n  Total nulls: {df.isnull().sum().sum()}")
    """))
    cells.append(C("""
        # ── 2.2  Drop Irrelevant / Constant Columns ─────────────────────────
        # EmployeeNumber  → unique ID, no predictive value
        # Over18          → constant 'Y' for all rows
        # StandardHours   → constant 80 for all rows
        # EmployeeCount   → constant 1 for all rows

        for col in ['Over18','StandardHours','EmployeeCount']:
            if col in df.columns:
                print(f"  {col}: unique values = {df[col].unique()} ← CONSTANT")

        cols_to_drop = [c for c in ['EmployeeNumber','Over18','StandardHours','EmployeeCount']
                        if c in df.columns]
        df_clean = df.drop(columns=cols_to_drop)
        print(f"\\n🗑  Dropped {len(cols_to_drop)} columns: {cols_to_drop}")
        print(f"   Remaining: {df_clean.shape[1]} columns")
    """))
    cells.append(C("""
        # ── 2.3  Encode Target: Attrition → 0 / 1 ──────────────────────────
        df_clean = df_clean.copy()
        df_clean['Attrition'] = (df_clean['Attrition'] == 'Yes').astype(int)
        print("✓ Target encoded:  Yes → 1  (Left)  |  No → 0  (Stayed)")
        print(df_clean['Attrition'].value_counts().rename({1:'Left (1)',0:'Stayed (0)'}).to_string())
    """))
    cells.append(C("""
        # ── 2.4  One-Hot Encoding for Categorical Columns ───────────────────
        cat_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
        print(f"🔤 Categorical columns ({len(cat_cols)}): {cat_cols}\\n")

        df_encoded = pd.get_dummies(df_clean, columns=cat_cols, drop_first=True)
        print(f"✓ After One-Hot Encoding:")
        print(f"   Before : {df_clean.shape[1]} columns")
        print(f"   After  : {df_encoded.shape[1]} columns")
        print(f"   Added  : {df_encoded.shape[1] - df_clean.shape[1]} binary dummy columns")
    """))
    cells.append(C("""
        # ── 2.5  Feature Matrix & Target ────────────────────────────────────
        X = df_encoded.drop('Attrition', axis=1)
        y = df_encoded['Attrition']
        print(f"✓ Feature matrix X : {X.shape}")
        print(f"  Target vector  y : {y.shape}")
        print(f"  Sample features  : {list(X.columns[:6])} ...")
    """))
    cells.append(C("""
        # ── 2.6  StandardScaler ──────────────────────────────────────────────
        scaler   = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        print("✓ StandardScaler applied — all features: mean ≈ 0, std ≈ 1")
        print(f"\\n  Age before scaling : min={X['Age'].min()}, max={X['Age'].max()}")
        print(f"  Age after  scaling : mean={X_scaled['Age'].mean():.4f}, std={X_scaled['Age'].std():.4f}")
        print(f"\\n  Final preprocessed shape: {X_scaled.shape}")
    """))

    # ════════════════════════════════
    # TASK 3
    # ════════════════════════════════
    cells.append(M("""
---
## ✅ Task 3 — Exploratory Data Analysis (EDA)

**Objective:** Discover patterns in attrition across departments, roles, income, work-life balance, and tenure.
"""))
    cells.append(C("""
        # ── 3.1  Attrition Rate by Department ───────────────────────────────
        dept_attr = df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).round(2).sort_values(ascending=False)

        print("📊 Attrition Rate by Department:")
        for dept, rate in dept_attr.items():
            bar = '█' * int(rate / 1.5)
            print(f"  {dept:<35} {rate:5.1f}%  {bar}")
    """))
    cells.append(C("""
        # ── 3.2  Attrition Rate by Job Role ─────────────────────────────────
        role_attr = df.groupby('JobRole')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).round(2).sort_values(ascending=False)

        print("👔 Attrition Rate by Job Role:")
        for role, rate in role_attr.items():
            bar = '█' * int(rate / 1.5)
            print(f"  {role:<35} {rate:5.1f}%  {bar}")
    """))
    cells.append(C("""
        # ── 3.3  Attrition vs Monthly Income ────────────────────────────────
        left_income   = df[df['Attrition']=='Yes']['MonthlyIncome'].mean()
        stayed_income = df[df['Attrition']=='No']['MonthlyIncome'].mean()
        diff          = stayed_income - left_income
        pct           = diff / left_income * 100

        print("💰 Monthly Income Analysis:")
        print(f"  Employees who LEFT   — avg: ${left_income:>9,.2f}")
        print(f"  Employees who STAYED — avg: ${stayed_income:>9,.2f}")
        print(f"  Gap : ${diff:,.2f} ({pct:.1f}% more for stayers)")

        left_med   = df[df['Attrition']=='Yes']['MonthlyIncome'].median()
        stayed_med = df[df['Attrition']=='No']['MonthlyIncome'].median()
        print(f"\\n  Median — LEFT: ${left_med:,.0f}  |  STAYED: ${stayed_med:,.0f}")
    """))
    cells.append(C("""
        # ── 3.4  Attrition vs Work-Life Balance ─────────────────────────────
        print("⚖️  Work-Life Balance Rating (1=Bad … 4=Best):")
        wlb = df.groupby('Attrition')['WorkLifeBalance'].agg(['mean','median','std'])
        print(wlb.rename(index={'Yes':'Left','No':'Stayed'}).round(2).to_string())
        print()
        wlb_cross = pd.crosstab(df['WorkLifeBalance'], df['Attrition'],
                                 normalize='index') * 100
        print("Attrition % per WLB rating:")
        print(wlb_cross['Yes'].round(1).rename('Attrition%').to_string())
    """))
    cells.append(C("""
        # ── 3.5  Attrition vs Years at Company ──────────────────────────────
        print("⏳ Tenure Analysis:")
        tenure = df.groupby('Attrition')['YearsAtCompany'].agg(['mean','median','min','max'])
        print(tenure.rename(index={'Yes':'Left','No':'Stayed'}).round(1).to_string())

        df['TenureBucket'] = pd.cut(
            df['YearsAtCompany'],
            bins=[0,2,5,10,20,40],
            labels=['0-2 yrs','3-5 yrs','6-10 yrs','11-20 yrs','20+ yrs']
        )
        t_attr = df.groupby('TenureBucket', observed=True)['Attrition'].apply(
            lambda x: (x=='Yes').sum()/len(x)*100
        ).round(1)
        print("\\nAttrition % by tenure bucket:")
        for tb, rate in t_attr.items():
            bar = '█' * int(rate/1.5)
            print(f"  {str(tb):<12}  {rate:5.1f}%  {bar}")
    """))
    cells.append(C("""
        # ── 3.6  Overtime & Job Satisfaction ────────────────────────────────
        ot_left   = (df[df['Attrition']=='Yes']['OverTime']=='Yes').mean()*100
        ot_stayed = (df[df['Attrition']=='No']['OverTime']=='Yes').mean()*100
        print(f"⏰ Overtime among Leavers : {ot_left:.1f}%")
        print(f"⏰ Overtime among Stayers: {ot_stayed:.1f}%")
        print(f"   Leavers are {ot_left/ot_stayed:.1f}× more likely to work overtime!\\n")

        js_left   = df[df['Attrition']=='Yes']['JobSatisfaction'].mean()
        js_stayed = df[df['Attrition']=='No']['JobSatisfaction'].mean()
        print(f"😊 Avg Job Satisfaction — Left: {js_left:.2f}  |  Stayed: {js_stayed:.2f}  (scale 1–4)")
    """))

    td = m['top_dept']; td_r = m['dept_attr'][m['top_dept']]
    tr = m['top_role']; tr_r = m['role_attr'][m['top_role']]
    inc_diff = m['stay_income'] - m['left_income']
    inc_pct  = inc_diff / m['left_income'] * 100

    cells.append(M(f"""
### 📝 Task 3 — Business Insights (EDA)

> **Insight 1 — Departmental Hotspot:** The **{td}** department records the highest attrition at **{td_r:.1f}%**, compared to the company average of {m['attrition_rate']:.1f}%. This represents nearly twice the baseline rate and signals systemic issues in this department.
>
> **Insight 2 — Riskiest Job Role:** **{tr}** roles exit at **{tr_r:.1f}%** — the highest of any position. These are typically high-pressure, entry-to-mid-level roles with limited visible career advancement.
>
> **Insight 3 — The Income Gap:** Employees who left earned an average of **${m['left_income']:,.0f}/month** vs **${m['stay_income']:,.0f}** for those who stayed — a gap of **${inc_diff:,.0f} ({inc_pct:.0f}%)**. However, even well-compensated employees leave, indicating pay is necessary but not sufficient.
>
> **Insight 4 — Overtime = Burnout Signal:** {m['ot_left']:.0f}% of employees who left worked overtime, vs only {m['ot_stay']:.0f}% of those who stayed — a **{m['ot_ratio']:.1f}× difference**. Chronic overwork is the clearest leading indicator of attrition in this dataset.
>
> **Insight 5 — New Joiners Are Most Vulnerable:** Employees with 0–2 years tenure show the highest exit rate. Poor onboarding, mismatched expectations, or early-career management failures are likely drivers.
"""))

    # ════════════════════════════════
    # TASK 4
    # ════════════════════════════════
    cells.append(M("""
---
## ✅ Task 4 — Model Building & Comparison

**Objective:** Split data, handle class imbalance, train 3 classifiers, and compare results.
"""))
    cells.append(C("""
        # ── 4.1  Train-Test Split (80/20, stratified) ────────────────────────
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"✓ Split — Train: {len(X_train):,}  |  Test: {len(X_test):,}")
        print(f"  Attrition in train : {y_train.sum()} ({y_train.mean()*100:.1f}%)")
        print(f"  Attrition in test  : {y_test.sum()}  ({y_test.mean()*100:.1f}%)")
        print()
        print("  stratify=y ensures the same attrition ratio in both splits —")
        print("  critical for imbalanced datasets to avoid biased evaluation.")
    """))
    cells.append(C("""
        # ── 4.2  Define Models ────────────────────────────────────────────────
        # class_weight='balanced' → automatically gives higher penalty to
        # minority class (Attrition=Yes), compensating for the 84%/16% split.
        # Gradient Boosting handles imbalance via iterative boosting on errors.

        models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42, class_weight='balanced', C=1.0
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=200, random_state=42, class_weight='balanced', n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=200, random_state=42, learning_rate=0.1,
                max_depth=5, subsample=0.8
            ),
        }

        print("📋 Models to Train:")
        for name in models:
            print(f"  ✦ {name}")
        print()
        print("  Class Imbalance Strategy:")
        print("  → LR & RF : class_weight='balanced'  (explicit re-weighting)")
        print("  → GB      : iterative boosting naturally upweights hard samples")
    """))
    cells.append(C("""
        # ── 4.3  Train & Collect Results ─────────────────────────────────────
        results = {}
        print("🏋️  Training...", flush=True)

        for name, model in models.items():
            print(f"\\n  [{name}]", flush=True)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            results[name] = dict(
                model     = model,
                y_pred    = y_pred,
                y_prob    = y_prob,
                accuracy  = accuracy_score(y_test, y_pred),
                precision = precision_score(y_test, y_pred, zero_division=0),
                recall    = recall_score(y_test, y_pred, zero_division=0),
                f1        = f1_score(y_test, y_pred, zero_division=0),
                roc_auc   = roc_auc_score(y_test, y_prob),
                cm        = confusion_matrix(y_test, y_pred),
                report    = classification_report(y_test, y_pred,
                                target_names=['Stayed','Left']),
            )
            r = results[name]
            print(f"  Precision={r['precision']:.3f}  Recall={r['recall']:.3f}"
                  f"  F1={r['f1']:.3f}  ROC-AUC={r['roc_auc']:.3f}")

        print("\\n✓ All 3 models trained!")
    """))
    cells.append(C("""
        # ── 4.4  Results Comparison Table ────────────────────────────────────
        print("\\n" + "═"*74)
        print(f"  {'Model':<28} {'Accuracy':>9} {'Precision':>10} "
              f"{'Recall':>8} {'F1':>8} {'ROC-AUC':>9}")
        print("═"*74)
        for name, r in results.items():
            print(f"  {name:<28} {r['accuracy']:>9.4f} {r['precision']:>10.4f} "
                  f"{r['recall']:>8.4f} {r['f1']:>8.4f} {r['roc_auc']:>9.4f}")
        print("═"*74)

        best_name = max(results, key=lambda k: results[k]['roc_auc'])
        print(f"\\n  🏆  Best Model: {best_name}  "
              f"(ROC-AUC = {results[best_name]['roc_auc']:.4f})")
    """))

    # ════════════════════════════════
    # TASK 5
    # ════════════════════════════════
    bn = m['best_model']
    br = m['results'][bn]
    cells.append(M(f"""
---
## ✅ Task 5 — Model Evaluation

**Objective:** Deeply evaluate all 3 models, identify the best performer, and extract feature importances.
"""))
    cells.append(C("""
        # ── 5.1  Full Classification Reports ─────────────────────────────────
        for name, r in results.items():
            print("═"*60)
            print(f"  {name}")
            print("─"*60)
            print(r['report'])
    """))
    cells.append(C("""
        # ── 5.2  ROC-AUC Rankings ────────────────────────────────────────────
        print("📈 ROC-AUC Scores:")
        for name, r in results.items():
            mark = "  ← 🏆 BEST" if name == best_name else ""
            bar  = '█' * int(r['roc_auc'] * 28)
            print(f"  {name:<28}: {r['roc_auc']:.4f}  {bar}{mark}")
        print()
        print("  ROC-AUC: 1.0 = perfect  |  0.5 = random  |  > 0.75 = good")
    """))
    cells.append(C(f"""
        # ── 5.3  Best Model Summary ──────────────────────────────────────────
        best = results[best_name]
        cm   = best['cm']

        print(f"🏆 BEST MODEL: {{best_name}}")
        print("─"*52)
        print(f"  Accuracy : {{best['accuracy']:.4f}}")
        print(f"  Precision: {{best['precision']:.4f}}")
        print(f"  Recall   : {{best['recall']:.4f}}")
        print(f"  F1-Score : {{best['f1']:.4f}}")
        print(f"  ROC-AUC  : {{best['roc_auc']:.4f}}")
        print()
        print("  Confusion Matrix:")
        print(f"    True Positives  (correctly caught exits)  : {{cm[1][1]}}")
        print(f"    False Negatives (missed exits — dangerous): {{cm[1][0]}}")
        print(f"    False Positives (false alarms)            : {{cm[0][1]}}")
        print(f"    True Negatives  (correctly predicted stays): {{cm[0][0]}}")
        print()
        print(f"  ✅ Why {{best_name}} wins:")
        print(f"     Highest ROC-AUC → best discrimination between leavers/stayers.")
        print(f"     Strong Recall → catches more actual attrition cases.")
        print(f"     In HR contexts, a missed leaver is more costly than a false alarm.")
    """))
    cells.append(C("""
        # ── 5.4  Feature Importance — Top 10 ────────────────────────────────
        best_model_obj = best['model']

        if hasattr(best_model_obj, 'feature_importances_'):
            fi = pd.Series(best_model_obj.feature_importances_, index=X.columns)
            fi_type = "Gini / Mean Decrease Impurity"
        else:
            fi = pd.Series(np.abs(best_model_obj.coef_[0]), index=X.columns)
            fi_type = "Absolute Coefficient Magnitude"

        fi_top10 = fi.sort_values(ascending=False).head(10)

        print(f"🔑 Top 10 Features  ({fi_type}):\\n")
        for rank, (feat, score) in enumerate(fi_top10.items(), 1):
            bar = '█' * int(score * 250)
            print(f"  #{rank:2d}  {feat:<40} {score:.5f}  {bar[:22]}")
    """))

    cells.append(M(f"""
### 📝 Task 5 — Model Selection Justification

**Best Model: {bn}**

| Metric | Score |
|--------|-------|
| Accuracy | {br['accuracy']:.4f} |
| Precision | {br['precision']:.4f} |
| Recall | {br['recall']:.4f} |
| F1-Score | {br['f1']:.4f} |
| **ROC-AUC** | **{br['roc_auc']:.4f}** |

**Rationale for choosing {bn}:**

1. **Highest ROC-AUC ({br['roc_auc']:.4f})** — best discrimination between leavers and stayers, regardless of classification threshold.
2. **Strong Recall ({br['recall']:.4f})** — catches more actual attrition cases. In HR, a *missed* leaver is far more costly than a false alarm.
3. **Non-linear patterns** — ensemble tree methods capture complex interactions (e.g., *low income AND overtime AND low job level*) that linear models miss.
"""))

    # ════════════════════════════════
    # TASK 6
    # ════════════════════════════════
    cells.append(M("""
---
## ✅ Task 6 — Visualizations

**5 charts** — dark premium theme, all saved to `charts/` as PNG.
"""))
    cells.append(C("""
        # ════════════════════════════════════════════════════════════════
        # CHART 1 — Attrition Rate by Department & Job Role
        # ════════════════════════════════════════════════════════════════
        dept_attr = df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).round(2).sort_values(ascending=False)

        role_attr = df.groupby('JobRole')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).round(2).sort_values(ascending=False)

        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        fig.patch.set_facecolor(BG)

        # Department
        dept_colors = [RED, ORANGE, BLUE][:len(dept_attr)]
        bars = axes[0].bar(dept_attr.index, dept_attr.values,
                            color=dept_colors, edgecolor='none', width=0.55, zorder=3)
        axes[0].set_facecolor(AX_BG)
        axes[0].set_title('Attrition Rate by Department', pad=15)
        axes[0].set_xlabel('Department', labelpad=8)
        axes[0].set_ylabel('Attrition Rate (%)', labelpad=8)
        axes[0].set_ylim(0, dept_attr.values.max() * 1.45)
        axes[0].grid(axis='y', zorder=0)
        for bar, val in zip(bars, dept_attr.values):
            axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                         f'{val:.1f}%', ha='center', va='bottom',
                         fontweight='bold', color='white', fontsize=14)

        # Job Role
        role_srt = role_attr.sort_values(ascending=True)
        n = len(role_srt)
        rcols = [plt.cm.RdYlGn_r(i/(n-1)) for i in range(n)]
        hbars = axes[1].barh(role_srt.index, role_srt.values,
                              color=rcols, edgecolor='none', height=0.65, zorder=3)
        axes[1].set_facecolor(AX_BG)
        axes[1].set_title('Attrition Rate by Job Role', pad=15)
        axes[1].set_xlabel('Attrition Rate (%)', labelpad=8)
        axes[1].grid(axis='x', zorder=0)
        for bar, val in zip(hbars, role_srt.values):
            axes[1].text(val+0.5, bar.get_y()+bar.get_height()/2,
                         f'{val:.1f}%', va='center', fontweight='bold',
                         color='white', fontsize=10)

        fig.suptitle('Employee Attrition: Department & Role Breakdown',
                     fontsize=17, fontweight='bold', color='white', y=1.02)
        plt.tight_layout()
        plt.savefig('charts/chart1_attrition_by_dept_role.png',
                    dpi=150, bbox_inches='tight', facecolor=BG)
        plt.show()
        print("✓ Chart 1 saved → charts/chart1_attrition_by_dept_role.png")
    """))
    cells.append(C("""
        # ════════════════════════════════════════════════════════════════
        # CHART 2 — Monthly Income: Box Plot + Violin Plot
        # ════════════════════════════════════════════════════════════════
        grp_yes = df[df['Attrition']=='Yes']['MonthlyIncome'].values
        grp_no  = df[df['Attrition']=='No']['MonthlyIncome'].values

        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        fig.patch.set_facecolor(BG)

        bp = axes[0].boxplot(
            [grp_yes, grp_no], labels=['Left  🔴', 'Stayed 🟢'],
            patch_artist=True, notch=True,
            medianprops=dict(color=GOLD, linewidth=3),
            whiskerprops=dict(linewidth=1.5, color='#aaa'),
            capprops=dict(linewidth=2, color='#aaa'),
            flierprops=dict(marker='o', markersize=4, alpha=0.5),
        )
        for patch, col in zip(bp['boxes'], [RED, BLUE]):
            patch.set_facecolor(col+'44'); patch.set_edgecolor(col); patch.set_linewidth(2)
        for flier, col in zip(bp['fliers'], [RED, BLUE]):
            flier.set_markerfacecolor(col); flier.set_markeredgecolor(col)
        axes[0].set_facecolor(AX_BG)
        axes[0].set_title('Monthly Income Distribution\\n(Box Plot)', pad=10)
        axes[0].set_ylabel('Monthly Income ($)')
        axes[0].grid(axis='y', alpha=0.4)
        for xpos, (g, col) in enumerate(zip(['Yes','No'], [RED, BLUE]), 1):
            mv = df[df['Attrition']==g]['MonthlyIncome'].mean()
            axes[0].text(xpos, mv+230, f'Mean: ${mv:,.0f}',
                         ha='center', color=col, fontsize=9, fontweight='bold')

        vp = axes[1].violinplot([grp_yes, grp_no], positions=[1,2],
                                 showmeans=True, showmedians=True)
        for pc, col in zip(vp['bodies'], [RED, BLUE]):
            pc.set_facecolor(col+'55'); pc.set_edgecolor(col); pc.set_linewidth(2)
        vp['cmeans'].set_color(GOLD); vp['cmedians'].set_color('white')
        axes[1].set_xticks([1,2]); axes[1].set_xticklabels(['Left 🔴','Stayed 🟢'])
        axes[1].set_facecolor(AX_BG)
        axes[1].set_title('Monthly Income Density\\n(Violin Plot)', pad=10)
        axes[1].set_ylabel('Monthly Income ($)')
        axes[1].grid(axis='y', alpha=0.4)

        fig.suptitle('Monthly Income: Employees Who Left vs Stayed',
                     fontsize=16, fontweight='bold', color='white', y=1.02)
        plt.tight_layout()
        plt.savefig('charts/chart2_income_boxplot.png',
                    dpi=150, bbox_inches='tight', facecolor=BG)
        plt.show()
        print("✓ Chart 2 saved → charts/chart2_income_boxplot.png")
    """))
    cells.append(C("""
        # ════════════════════════════════════════════════════════════════
        # CHART 3 — Confusion Matrix Heatmap + Model Comparison Bars
        # ════════════════════════════════════════════════════════════════
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.patch.set_facecolor(BG)

        cm     = best['cm']
        cm_pct = cm.astype(float) / cm.sum(axis=1)[:,None] * 100
        annot  = np.array([[f'{cm[i,j]}\\n({cm_pct[i,j]:.1f}%)' for j in range(2)]
                            for i in range(2)])
        sns.heatmap(cm, annot=annot, fmt='', ax=axes[0],
                    cmap='RdBu_r', linewidths=2, linecolor=BG,
                    xticklabels=['Stayed','Left'], yticklabels=['Stayed','Left'],
                    annot_kws={'size':13,'weight':'bold'},
                    cbar_kws={'label':'Count'})
        axes[0].set_title(f'Confusion Matrix\\n{best_name}', pad=12)
        axes[0].set_xlabel('Predicted Label', labelpad=8)
        axes[0].set_ylabel('True Label', labelpad=8)

        met_keys   = ['accuracy','precision','recall','f1','roc_auc']
        met_labels = ['Accuracy','Precision','Recall','F1-Score','ROC-AUC']
        x, width   = np.arange(len(met_labels)), 0.25
        bcolors    = [BLUE, GREEN, ORANGE]
        for i, (mname, bcol) in enumerate(zip(results.keys(), bcolors)):
            vals = [results[mname][k] for k in met_keys]
            axes[1].bar(x+(i-1)*width, vals, width, label=mname,
                        color=bcol, alpha=0.85, edgecolor='none', zorder=3)
        axes[1].set_facecolor(AX_BG)
        axes[1].set_title('Model Performance Comparison', pad=12)
        axes[1].set_xticks(x); axes[1].set_xticklabels(met_labels, fontsize=10)
        axes[1].set_ylim(0, 1.15); axes[1].set_ylabel('Score')
        axes[1].legend(loc='lower right', fontsize=9)
        axes[1].grid(axis='y', alpha=0.4, zorder=0)

        fig.suptitle(f'Model Evaluation  —  Best: {best_name}',
                     fontsize=16, fontweight='bold', color='white', y=1.02)
        plt.tight_layout()
        plt.savefig('charts/chart3_confusion_matrix.png',
                    dpi=150, bbox_inches='tight', facecolor=BG)
        plt.show()
        print("✓ Chart 3 saved → charts/chart3_confusion_matrix.png")
    """))
    cells.append(C("""
        # ════════════════════════════════════════════════════════════════
        # CHART 4 — Top 10 Feature Importances (Horizontal Bar)
        # ════════════════════════════════════════════════════════════════
        fi_asc   = fi_top10.sort_values(ascending=True)
        fi_colors = ([TEAL]*4 + [BLUE]*3 + [ORANGE]*1 + [RED]*2)[:len(fi_asc)][::-1]

        fig, ax = plt.subplots(figsize=(13, 7))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(AX_BG)

        bars_fi = ax.barh(fi_asc.index, fi_asc.values,
                           color=fi_colors, edgecolor='none', height=0.65, zorder=3)
        ax.set_title(f'Top 10 Features Driving Employee Attrition\\n({best_name})', pad=15)
        ax.set_xlabel('Importance Score', labelpad=8)
        ax.grid(axis='x', zorder=0, alpha=0.4)
        for bar, val in zip(bars_fi, fi_asc.values):
            ax.text(val + fi_top10.max()*0.01, bar.get_y()+bar.get_height()/2,
                    f'{val:.5f}', va='center', fontsize=9, fontweight='bold', color='white')
        ax.text(0.98, 0.02, f'⭐ Top Predictor: {fi_top10.index[0]}',
                transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
                color=RED, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=AX_BG, edgecolor=RED))

        plt.tight_layout()
        plt.savefig('charts/chart4_feature_importance.png',
                    dpi=150, bbox_inches='tight', facecolor=BG)
        plt.show()
        print("✓ Chart 4 saved → charts/chart4_feature_importance.png")
    """))
    cells.append(C("""
        # ════════════════════════════════════════════════════════════════
        # CHART 5 (Bonus) — ROC Curve — All 3 Models
        # ════════════════════════════════════════════════════════════════
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(AX_BG)

        roc_cols = [BLUE, GREEN, ORANGE]
        roc_stls = ['-','--','-.']
        for (name, r), rcol, rst in zip(results.items(), roc_cols, roc_stls):
            fpr, tpr, _ = roc_curve(y_test, r['y_prob'])
            ax.plot(fpr, tpr, color=rcol, lw=2.5, linestyle=rst,
                    label=f'{name}  (AUC = {r["roc_auc"]:.3f})')

        ax.plot([0,1],[0,1],'w--', lw=1.5, alpha=0.4,
                label='Random Baseline  (AUC = 0.500)')

        best_idx = list(results.keys()).index(best_name)
        bfpr, btpr, _ = roc_curve(y_test, best['y_prob'])
        ax.fill_between(bfpr, btpr, alpha=0.08, color=roc_cols[best_idx])

        ax.set_xlabel('False Positive Rate  (1 − Specificity)', labelpad=8)
        ax.set_ylabel('True Positive Rate  (Sensitivity / Recall)', labelpad=8)
        ax.set_title('ROC Curve — All 3 Models\\nHigher AUC = Better Discrimination', pad=15)
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(alpha=0.3)
        ax.annotate('Optimal\\nZone', xy=(0.1, 0.9), fontsize=10, color=GOLD,
                    fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round', facecolor=AX_BG, edgecolor=GOLD, alpha=0.7))

        plt.tight_layout()
        plt.savefig('charts/chart5_roc_curve.png',
                    dpi=150, bbox_inches='tight', facecolor=BG)
        plt.show()
        print("✓ Chart 5 saved → charts/chart5_roc_curve.png")
        print()
        print("✅ All 5 charts saved to  charts/")
    """))

    # ════════════════════════════════
    # TASK 7
    # ════════════════════════════════
    t3 = m['top3_feats']
    t3_fmt = [f.replace('_Yes','').replace('_','  ') for f in t3]
    cells.append(M("""
---
## ✅ Task 7 — HR Insights & Business Recommendations
"""))
    cells.append(C(f"""
        # ── 7.1  Top Predictors Summary ──────────────────────────────────────
        print("🔑 Top 3 Attrition Predictors (from best model):")
        for i, (feat, score) in enumerate(list(fi_top10.items())[:3], 1):
            print(f"  #{{i}}: {{feat}}  (importance = {{score:.5f}})")
        print()
        top_dept_name = max(dept_attr, key=dept_attr.get)
        top_role_name = max(role_attr, key=role_attr.get)
        print(f"  High-Risk Department : {{top_dept_name}} ({{dept_attr[top_dept_name]:.1f}}% attrition)")
        print(f"  High-Risk Job Role   : {{top_role_name}} ({{role_attr[top_role_name]:.1f}}% attrition)")
    """))

    cells.append(M(f"""
---

### 📊 HR Insights & Business Recommendations

#### 🔍 Which 3 Factors Most Strongly Predict That an Employee Will Leave?

Based on the **{bn}** model:

1. **{t3_fmt[0] if len(t3_fmt)>0 else 'OverTime'}** — The top predictor. Employees in chronic overtime are burning out. This is the earliest, clearest signal HR can act on.
2. **{t3_fmt[1] if len(t3_fmt)>1 else 'Monthly Income'}** — Below-market or stagnant compensation is a core driver, especially for younger employees who can command market salaries.
3. **{t3_fmt[2] if len(t3_fmt)>2 else 'Age / Years at Company'}** — Career stage matters. Early-career employees leave to explore; mid-career employees leave when growth paths stall.

---

#### 🏢 Which Department / Role Should HR Prioritise?

- **Department:** **{td}** at **{td_r:.1f}%** attrition — nearly double the {m['attrition_rate']:.1f}% company average. Targeted retention programmes here will yield the largest ROI.
- **Job Role:** **{tr}** at **{tr_r:.1f}%** — the single riskiest role. High workload + limited advancement = predictable exits.

---

#### 💰 Does Salary Alone Explain Attrition?

**No.** While leavers earned ${m['left_income']:,.0f}/month vs ${m['stay_income']:,.0f} for stayers (a {(m['stay_income']-m['left_income'])/m['left_income']*100:.0f}% gap), the model shows that **overtime, years at company, job level, and work-life balance** are equally or more predictive. High earners also exit. Raising salaries without fixing workload or culture will not solve attrition.

---

### 💼 Concrete HR Recommendations

**Recommendation 1 — Overtime Alert & Burnout Prevention Policy**

Establish a threshold: if any employee works overtime for >3 consecutive weeks, the system automatically triggers a mandatory 1:1 check-in with their manager. During this conversation, managers ask about workload sustainability, career goals, and satisfaction. Offer flexible hours or compensatory leave immediately. This addresses the #1 predictor at near-zero cost.

**Recommendation 2 — Structured Retention Programme for {td} / {tr} Roles**

For the highest-risk segment:
- Within 30 days of joining, every new {tr} receives a written 12-month career roadmap and a mentorship buddy.
- Conduct quarterly *stay interviews* (not performance reviews) — 15-minute informal conversations asking: "What would make you want to stay for another year?"
- Define and communicate a promotion timeline publicly (e.g., "{tr} → Senior in 18 months if X criteria met").

---

### ⚠️ Model Limitations — What HR Must Know Before Using This

1. **Correlation ≠ Causation:** The model finds statistical patterns, not proven causes. An employee flagged as "high-risk" may have entirely personal reasons for leaving that no dataset can capture.
2. **Model Drift:** As company culture, pay bands, and job structures evolve, the model's predictions become less reliable. **Retrain every 12 months** with fresh data.
3. **Individual Privacy & Ethics:** This model should **never** be used to make employment decisions (raises, promotions, PIPs) for individual employees. Use it only to guide group-level HR strategy and resource allocation.
4. **Data Reflects the Past:** The model was trained on historical outcomes. If you improve your culture, the model will temporarily *overestimate* attrition risk — which is actually a good problem to have.

---

## 🎉 Project Summary

| Item | Detail |
|------|--------|
| Dataset | IBM HR Analytics — {m['n_rows']:,} employees |
| Best Model | {bn} |
| ROC-AUC | {br['roc_auc']:.4f} |
| Recall (Attrition) | {br['recall']:.4f} |
| Top Attrition Driver | {t3[0] if t3 else 'OverTime'} |
| Charts Saved | 5 PNG files in `charts/` |

> *Submitted for KK Internship — Week 2  |  Author: Shivansh  |  June 2026*
"""))

    nb.cells = cells
    with open(NOTEBOOK, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    code_cells = sum(1 for c in cells if c.cell_type == 'code')
    md_cells   = sum(1 for c in cells if c.cell_type == 'markdown')
    print(f"  ✓ {NOTEBOOK} created  ({code_cells} code cells, {md_cells} markdown cells)")


# ═══════════════════════════════════════════════════════════════════════
# 4.  CREATE WORD SUMMARY DOCUMENT
# ═══════════════════════════════════════════════════════════════════════
def create_summary(m):
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    print("\n" + "─" * 68)
    print("  SECTION 4 — Creating HR Summary (summary.docx)")
    print("─" * 68)

    doc = Document()
    for sec in doc.sections:
        sec.top_margin    = Inches(0.85)
        sec.bottom_margin = Inches(0.85)
        sec.left_margin   = Inches(1.0)
        sec.right_margin  = Inches(1.0)

    NAVY  = RGBColor(0x1a, 0x1a, 0x6e)
    GREY  = RGBColor(0x55, 0x55, 0x55)
    LGREY = RGBColor(0x88, 0x88, 0x88)

    # Title
    t = doc.add_heading('Employee Attrition: What the Data Tells Us', 0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.runs[0].font.color.rgb = NAVY

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run(f"Confidential Report for HR Leadership  |  {datetime.date.today().strftime('%B %Y')}")
    r.font.size = Pt(11); r.font.italic = True; r.font.color.rgb = GREY

    doc.add_paragraph()

    # Overview
    doc.add_heading('Overview', 1).runs[0].font.color.rgb = NAVY
    p = doc.add_paragraph(
        f"Our analytics team examined the employment records of all {m['n_rows']:,} employees "
        f"in our HR system to understand the patterns behind voluntary departures. Using a machine "
        f"learning model trained on 30+ factors — including salary, working hours, job role, "
        f"tenure, and satisfaction scores — we identified who is most at risk of leaving, "
        f"and why. The findings below are presented for strategic HR decision-making."
    )
    p.runs[0].font.size = Pt(11)

    # Key Findings
    doc.add_heading('Key Findings', 1).runs[0].font.color.rgb = NAVY

    td = m['top_dept']; td_r = m['dept_attr'][m['top_dept']]
    tr = m['top_role']; tr_r = m['role_attr'][m['top_role']]
    inc_diff = m['stay_income'] - m['left_income']

    findings = [
        ("16 in every 100 employees are leaving",
         f"Our current attrition rate is {m['attrition_rate']:.1f}%. Over the past period, "
         f"{m['n_left']} out of {m['n_rows']:,} employees have exited. Each departure costs "
         f"the organisation an estimated 50–200% of that role's annual salary in recruitment, "
         f"onboarding, and productivity loss."),

        ("Overwork is the clearest early warning sign",
         f"Employees who left were {m['ot_ratio']:.1f} times more likely to have worked overtime "
         f"than those who stayed. Among leavers, {m['ot_left']:.0f}% regularly worked overtime — "
         f"compared to only {m['ot_stay']:.0f}% of those who stayed. When people are "
         f"consistently stretched beyond capacity, departure becomes a matter of when, not if."),

        (f"The {td} department needs priority attention",
         f"This department's attrition rate stands at {td_r:.1f}% — "
         f"significantly above the company average of {m['attrition_rate']:.1f}%. "
         f"Within it, {tr} positions are leaving at {tr_r:.1f}%, the highest exit rate "
         f"of any role in the company. These are hard-to-replace positions."),

        ("Pay matters, but it is not the only factor",
         f"Employees who left earned an average of ${m['left_income']:,.0f}/month, versus "
         f"${m['stay_income']:,.0f} for those who stayed — a gap of ${inc_diff:,.0f}. "
         f"However, even well-compensated employees exit when they feel overworked, "
         f"undervalued, or see no growth path. Salary alone will not solve this."),

        ("New employees are the most at risk",
         "Employees in their first one to two years at the company show the highest exit rate. "
         "This points to gaps in our onboarding process, early-career support structures, "
         "or a mismatch between what candidates are told and what they experience on the job."),
    ]

    for title_t, body_t in findings:
        ph = doc.add_paragraph()
        rh = ph.add_run(f"• {title_t}")
        rh.bold = True; rh.font.size = Pt(11.5); rh.font.color.rgb = NAVY
        pb = doc.add_paragraph(f"  {body_t}")
        pb.runs[0].font.size = Pt(10.5)
        pb.paragraph_format.left_indent = Inches(0.2)
        pb.paragraph_format.space_after = Pt(5)

    # Recommendations
    doc.add_heading('What We Recommend', 1).runs[0].font.color.rgb = NAVY

    recs = [
        ("1. Introduce an Overtime Monitoring System",
         "HR should implement a simple rule: any employee working overtime for more than three "
         "consecutive weeks automatically triggers a manager check-in conversation. This is not "
         "a disciplinary meeting — it is a welfare conversation to understand workload, "
         "career satisfaction, and what would make the employee want to stay. This costs "
         "nothing and addresses the single strongest predictor of departure."),
        (f"2. Launch a Targeted Retention Programme for {td} — especially {tr} Roles",
         f"Given the {tr_r:.1f}% exit rate for {tr} positions, HR should: (a) define a clear, "
         f"written career progression path for this role within the first 30 days of joining; "
         f"(b) conduct quarterly 'stay interviews' — informal 15-minute conversations asking what "
         f"would make the employee want to remain; and (c) pair each new joiner with an "
         f"experienced mentor. Early investment in these conversations dramatically reduces "
         f"the chance of a surprise resignation."),
    ]

    for rt, rb in recs:
        pr = doc.add_paragraph()
        rr = pr.add_run(rt)
        rr.bold = True; rr.font.size = Pt(11.5); rr.font.color.rgb = NAVY
        pb2 = doc.add_paragraph(rb)
        pb2.runs[0].font.size = Pt(10.5)
        pb2.paragraph_format.left_indent = Inches(0.2)
        pb2.paragraph_format.space_after = Pt(7)

    # Caveat
    doc.add_heading('Important Note', 1).runs[0].font.color.rgb = NAVY
    pn = doc.add_paragraph(
        "This analysis identifies statistical patterns associated with past attrition. "
        "It cannot predict with certainty who will leave next — no tool can. It is intended "
        "to guide where HR focuses its energy, not to label or penalise individual employees. "
        "Decisions affecting individual employment must never be made based on model scores alone. "
        "The model should be reviewed and updated annually."
    )
    pn.runs[0].font.size = Pt(10.5); pn.runs[0].font.italic = True

    doc.add_paragraph()
    fp = doc.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run(
        f"Prepared by: Shivansh  |  KK Internship Week 2  |"
        f"  {datetime.date.today().strftime('%d %B %Y')}"
    )
    fr.font.size = Pt(9); fr.font.italic = True; fr.font.color.rgb = LGREY

    doc.save(SUMMARY)
    print(f"  ✓ {SUMMARY} created")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    if not download_dataset():
        sys.exit(1)

    metrics = run_analysis()
    create_notebook(metrics)
    create_summary(metrics)

    print("\n" + "=" * 68)
    print("  ✅  PROJECT BUILD COMPLETE!")
    print("=" * 68)
    print()
    print("📁 Output:")
    for fname in [NOTEBOOK, DATASET, SUMMARY]:
        size = os.path.getsize(fname) if os.path.exists(fname) else 0
        print(f"  {fname:<22}  ({size:,} bytes)")
    print(f"  charts/")
    for f in sorted(os.listdir(CHARTS_DIR)):
        size = os.path.getsize(os.path.join(CHARTS_DIR, f))
        print(f"    ├─ {f:<45}  ({size:,} bytes)")
    print()
    print("🚀 Next Steps:")
    print("  1. Open analysis.ipynb in Jupyter Notebook")
    print("  2. Kernel → Restart & Run All  (to generate all inline outputs)")
    print("  3. Review charts/ folder")
    print("  4. Open summary.docx to check the HR Director summary")
    print("  5. ZIP the entire EmployeeAttrition_Shivansh/ folder and submit")
    print()
