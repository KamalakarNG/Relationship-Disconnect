# algorithms.py
import math

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def compute_pci(hrv_change, tone_shift, breath_sync, microexpr_pos, microexpr_neg):
    """Compute a simple Pranic Coherence Index (PCI) in [0,1].
    Higher is better (more coherence).
    """
    hrv_score = clamp(0.5 + hrv_change)
    tone_score = clamp(1.0 - tone_shift)
    breath_score = clamp(breath_sync)
    micro_score = clamp(0.5 + microexpr_pos - microexpr_neg)

    w = {'hrv':0.25, 'tone':0.25, 'breath':0.25, 'micro':0.25}
    pci = (hrv_score*w['hrv'] + tone_score*w['tone'] + breath_score*w['breath'] + micro_score*w['micro'])
    return clamp(pci)

def compute_disconnect_score(hrv_drop, tone_shift, breath_desync, microexpr_neg, pci_drop):
    """Compute a DisconnectScore in [0,1]. Higher = more disconnect."""
    w1, w2, w3, w4, w5 = 0.25, 0.25, 0.2, 0.15, 0.15
    score = (w1*clamp(hrv_drop) + w2*clamp(tone_shift) + w3*clamp(breath_desync) + w4*clamp(microexpr_neg) + w5*clamp(pci_drop))
    return clamp(score)

if __name__ == '__main__':
    print(compute_pci(0.05, 0.1, 0.8, 0.1, 0.05))
    print(compute_disconnect_score(0.2, 0.3, 0.1, 0.05, 0.15))
