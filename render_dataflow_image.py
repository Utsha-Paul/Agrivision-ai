import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
import numpy as np
from PIL import Image

# Output directory
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "architecture_documentation")
os.makedirs(OUT_DIR, exist_ok=True)

PNG_PATH = os.path.join(OUT_DIR, "core_dataflow_breakdown.png")
JPG_PATH = os.path.join(OUT_DIR, "core_dataflow_breakdown.jpg")

# Canvas setup - High Resolution 4K aspect
fig, ax = plt.subplots(figsize=(22, 12), dpi=300)
fig.patch.set_facecolor('#F8FAFC')
ax.set_facecolor('#F8FAFC')

# Remove axes
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Palette
C_PRIMARY = '#0E3822'      # Deep emerald
C_ACCENT = '#10B981'       # Bright emerald
C_LIGHT_BG = '#ECFDF5'     # Soft mint green
C_BORDER = '#059669'       # Mid green
C_DARK = '#0F172A'         # Slate 900
C_MUTED = '#64748B'        # Slate 500
C_CONTAINER = '#F1F5F9'    # Soft slate bg
C_CARD_BG = '#FFFFFF'      # Pure white
C_AMBER = '#D97706'        # Warm amber
C_RED = '#DC2626'          # Crimson
C_PURPLE = '#7C3AED'       # Royal purple
C_BLUE = '#2563EB'         # Blue

# Title Banner
ax.text(50, 96.5, "AGRIVISION AI — CORE DATAFLOW BREAKDOWN", 
        fontsize=24, fontweight='black', color=C_PRIMARY, ha='center', va='center',
        fontfamily='sans-serif')
ax.text(50, 93.8, "End-to-End Execution Flow: Ingestion, Quality Validation, Deep Neural Inference, Multi-Factor Scoring, and Generative Output", 
        fontsize=12, fontweight='medium', color=C_MUTED, ha='center', va='center',
        fontfamily='sans-serif')

def draw_card(ax, x, y, w, h, title, subtitle="", bg=C_CARD_BG, border=C_BORDER, text_color=C_DARK, icon_color=C_ACCENT, radius=1.5, shadow=True):
    if shadow:
        s_box = FancyBboxPatch((x + 0.3, y - 0.4), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor='#CBD5E1', edgecolor='none', alpha=0.35, zorder=2)
        ax.add_patch(s_box)
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3)
    ax.add_patch(box)
    
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, fontsize=11, fontweight='bold', color=text_color, ha='center', va='center', zorder=4)
        ax.text(x + w/2, y + h*0.35, subtitle, fontsize=8.5, fontweight='medium', color=C_MUTED, ha='center', va='center', zorder=4)
    else:
        ax.text(x + w/2, y + h/2, title, fontsize=11, fontweight='bold', color=text_color, ha='center', va='center', zorder=4)

def draw_pill(ax, x, y, w, h, text, bg=C_LIGHT_BG, border=C_BORDER, text_color=C_PRIMARY):
    pill = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                          facecolor=bg, edgecolor=border, linewidth=1.2, zorder=6)
    ax.add_patch(pill)
    ax.text(x + w/2, y + h/2, text, fontsize=7.5, fontweight='bold', color=text_color, ha='center', va='center', zorder=7)

def draw_arrow(ax, start, end, label="", style="->", color='#059669', lw=2.0, connectionstyle="arc3,rad=0", label_pos=0.5, label_offset=(0, 1.2), dashed=False):
    ls = (0, (4, 3)) if dashed else 'solid'
    arrow = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=16,
                            color=color, linewidth=lw, linestyle=ls,
                            connectionstyle=connectionstyle, zorder=5)
    ax.add_patch(arrow)
    if label:
        lx = start[0] + (end[0] - start[0]) * label_pos + label_offset[0]
        ly = start[1] + (end[1] - start[1]) * label_pos + label_offset[1]
        
        # Draw small background tag for label readability
        ax.text(lx, ly, label, fontsize=8, fontweight='bold', color=color, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec=color, lw=0.8, alpha=0.95), zorder=8)

# ----------------- SUBGRAPH CONTAINERS -----------------
# 1. AI Inference Pipeline Container
box_ai = FancyBboxPatch((41, 38), 24, 48, boxstyle="round,pad=0,rounding_size=2.5",
                        facecolor='#F0FDF4', edgecolor='#A7F3D0', linewidth=1.5, zorder=1)
ax.add_patch(box_ai)
ax.text(53, 83.5, "AI INFERENCE PIPELINE", fontsize=11, fontweight='black', color='#065F46', ha='center', zorder=2)
ax.text(53, 81.8, "Trained Deep CNN, Tabular MLP & Computer Vision", fontsize=8, color='#047857', ha='center', zorder=2)

# 2. Decision Support & Scoring Container
box_ds = FancyBboxPatch((69, 38), 26, 48, boxstyle="round,pad=0,rounding_size=2.5",
                        facecolor='#FEF3C7', edgecolor='#FDE68A', linewidth=1.5, zorder=1, alpha=0.6)
ax.add_patch(box_ds)
ax.text(82, 83.5, "DECISION SUPPORT & SCORING", fontsize=11, fontweight='black', color='#92400E', ha='center', zorder=2)
ax.text(82, 81.8, "Deterministic Multi-Vector Penalties & Prescriptions", fontsize=8, color='#B45309', ha='center', zorder=2)

# ----------------- ENTITIES & PROCESS BLOCKS -----------------

# Entity: Farmer / Client UI
draw_card(ax, 3, 62, 13, 8, "Farmer / Client UI", "Web Browser / Mobile PWA", bg='#FFFFFF', border='#0F172A', shadow=True)

# Process: FastAPI Gateway
draw_card(ax, 20, 62, 14, 8, "FastAPI Gateway", "api_server.py / Starlette ASGI", bg='#ECFDF5', border=C_BORDER, shadow=True)

# Data Store: Storage
draw_card(ax, 20, 80, 14, 6.5, "Data Store: Uploads", "outputs/web_uploads/ (UUID.jpg)", bg='#F8FAFC', border='#64748B', shadow=True)

# Decision Gate: Validator
diamond = patches.Polygon([[27, 43], [34, 47], [27, 51], [20, 47]], closed=True,
                          fc='#FEF9C3', ec='#CA8A04', lw=1.8, zorder=3)
ax.add_patch(diamond)
ax.text(27, 47.7, "Image Validator", fontsize=9.5, fontweight='bold', color='#713F12', ha='center', va='center', zorder=4)
ax.text(27, 45.8, "Green Ratio >= 1%?", fontsize=7.5, fontweight='bold', color='#854D0E', ha='center', va='center', zorder=4)

# Error Terminus
draw_card(ax, 2, 44, 13, 6, "HTTP 400 Error", "Validation Failure Alert", bg='#FEF2F2', border=C_RED, text_color=C_RED, shadow=True)

# Models in AI Inference Pipeline
draw_card(ax, 43, 68, 20, 7.5, "EfficientNet CNN", "disease_efficientnet.keras (38 Classes)", bg='#FFFFFF', border='#059669', shadow=True)
draw_card(ax, 43, 54, 20, 7.5, "Tabular Yield MLP", "crop_yield_mlp.keras + preprocessor.pkl", bg='#FFFFFF', border='#059669', shadow=True)
draw_card(ax, 43, 40, 20, 7.5, "Optical Stress Visualizer", "visualizer.py (ExG, NDI, Heatmaps)", bg='#FFFFFF', border='#059669', shadow=True)

# Scoring Engines in Decision Support
draw_card(ax, 71, 68, 22, 7.5, "Crop Health Engine", "health_score.py (Multi-Factor 0–100)", bg='#FFFFFF', border=C_AMBER, shadow=True)
draw_card(ax, 71, 54, 22, 7.5, "Composite Risk Engine", "risk_engine.py (Weighted 6-Vector)", bg='#FFFFFF', border=C_AMBER, shadow=True)
draw_card(ax, 71, 40, 22, 7.5, "Advisory Engine", "recommendation_engine.py (Action Matrix)", bg='#FFFFFF', border=C_AMBER, shadow=True)

# Specialized Advanced AI Engines (Bottom Row)
draw_card(ax, 16, 12, 28, 9, "LSTM Recurrent Trend Forecaster", "lstm_trend_engine.py (7/14-Day Trajectory)", bg='#EFF6FF', border=C_BLUE, text_color='#1E3A8A', shadow=True)
draw_card(ax, 56, 12, 28, 9, "Agri-GAN 2.0 Report Synthesizer", "gan_report_engine.py (Latent Timeline & Dossier)", bg='#FAF5FF', border=C_PURPLE, text_color='#581C87', shadow=True)

# ----------------- DIRECTIONAL DATAFLOW ARROWS -----------------

# 1. User -> Gateway
draw_arrow(ax, (16, 66), (20, 66), label="Upload Image & Form Data", color='#047857', lw=2.2, label_pos=0.5, label_offset=(0, 1.3))

# 2. Gateway -> Storage (Persist)
draw_arrow(ax, (27, 70), (27, 80), label="1. Persist Raw Image", color='#475569', lw=1.8, label_pos=0.5, label_offset=(-3.8, 0))

# 3. Gateway -> Validator
draw_arrow(ax, (27, 62), (27, 51), label="2. Validate Quality", color='#047857', lw=1.8, label_pos=0.5, label_offset=(3.5, 0))

# 4. Validator -> Fail (No)
draw_arrow(ax, (20, 47), (15, 47), label="No (Invalid)", color=C_RED, lw=1.8, label_pos=0.5, label_offset=(0, 1.2))

# 5. Validator -> Models (Yes)
draw_arrow(ax, (34, 47), (43, 71.5), label="Yes: Valid Path", color='#059669', lw=2.0, connectionstyle="arc3,rad=-0.15", label_pos=0.45, label_offset=(0, 1.5))
draw_arrow(ax, (34, 47), (43, 57.5), color='#059669', lw=2.0)
draw_arrow(ax, (34, 47), (43, 44), color='#059669', lw=2.0, connectionstyle="arc3,rad=0.15")

# 6. Models -> Decision Support (Fusion)
draw_arrow(ax, (63, 71.5), (71, 71.5), label="Disease & Conf %", color='#047857', lw=1.8, label_pos=0.5, label_offset=(0, 1.2))
draw_arrow(ax, (63, 57.5), (71, 57.5), label="Yield Metric (t/ha)", color='#047857', lw=1.8, label_pos=0.5, label_offset=(0, 1.2))
draw_arrow(ax, (63, 44), (71, 44), label="Stress Score (0-100)", color='#047857', lw=1.8, label_pos=0.5, label_offset=(0, 1.2))

# Inter-Scoring Connections
draw_arrow(ax, (82, 68), (82, 61.5), color='#B45309', lw=1.4)
draw_arrow(ax, (82, 54), (82, 47.5), color='#B45309', lw=1.4)

# 7. Decision Support -> Gateway (Return Loop)
draw_arrow(ax, (82, 75.5), (34, 68), label="Aggregated Diagnostic Results Payload", color='#0F172A', lw=2.0, connectionstyle="arc3,rad=-0.35", label_pos=0.5, label_offset=(0, 2.0))

# 8. Gateway -> User (Live Results)
draw_arrow(ax, (20, 64), (16, 64), label="Live Results & Maps", color='#047857', lw=2.0, label_pos=0.5, label_offset=(0, -1.3))

# 9. Temporal LSTM Flow
draw_arrow(ax, (9.5, 62), (20, 21), label="Temporal Trend Query", color=C_BLUE, lw=1.8, connectionstyle="arc3,rad=0.2", dashed=True, label_pos=0.45, label_offset=(-3.5, 0))
draw_arrow(ax, (30, 21), (12, 62), label="7/14-Day Trajectory Projections", color=C_BLUE, lw=1.8, connectionstyle="arc3,rad=-0.2", dashed=True, label_pos=0.55, label_offset=(4.2, 0))

# 10. GAN Report Flow
draw_arrow(ax, (13, 62), (65, 21), label="Generate GAN Dossier Request", color=C_PURPLE, lw=1.8, connectionstyle="arc3,rad=0.3", dashed=True, label_pos=0.4, label_offset=(-4.5, 0))
draw_arrow(ax, (75, 21), (15, 63), label="Print-Ready Agronomic Field Dossier", color=C_PURPLE, lw=1.8, connectionstyle="arc3,rad=-0.3", dashed=True, label_pos=0.6, label_offset=(5.5, 0))

# Legend at bottom right
leg_x = 85.5
leg_y = 5.0
leg_box = FancyBboxPatch((leg_x, leg_y), 13.5, 7.5, boxstyle="round,pad=0,rounding_size=1",
                         facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.0, zorder=3)
ax.add_patch(leg_box)
ax.text(leg_x + 6.75, leg_y + 6.2, "FLOW LEGEND", fontsize=8, fontweight='black', color=C_DARK, ha='center', zorder=4)

ax.plot([leg_x + 1.2, leg_x + 3.8], [leg_y + 4.2, leg_y + 4.2], color='#059669', lw=2.2, zorder=4)
ax.text(leg_x + 4.5, leg_y + 4.2, "Synchronous REST", fontsize=7, color=C_DARK, va='center', zorder=4)

ax.plot([leg_x + 1.2, leg_x + 3.8], [leg_y + 2.0, leg_y + 2.0], color=C_BLUE, lw=2.0, linestyle=(0, (4, 3)), zorder=4)
ax.text(leg_x + 4.5, leg_y + 2.0, "Async Intelligence Query", fontsize=7, color=C_DARK, va='center', zorder=4)

# Tight layout and save
plt.tight_layout()
fig.savefig(PNG_PATH, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
plt.close(fig)

# Generate JPG from PNG using PIL for best quality
im = Image.open(PNG_PATH)
rgb_im = im.convert('RGB')
rgb_im.save(JPG_PATH, quality=95)

print(f"SUCCESS: Saved {PNG_PATH} ({os.path.getsize(PNG_PATH)} bytes)")
print(f"SUCCESS: Saved {JPG_PATH} ({os.path.getsize(JPG_PATH)} bytes)")

