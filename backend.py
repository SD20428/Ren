"""진단검사 확률 실험실의 계산 전용 백엔드.

pywebview가 이 클래스의 공개 메서드를 JavaScript Promise API로 노출한다.
HTTP 서버나 소켓을 사용하지 않는다.
"""

from __future__ import annotations

import math


KNCSP = {
    "2020": {"RR": 11.17, "PPV": 2.77, "CDR": 3.10, "ICR": 1.57, "se": 68.93, "sp": 89.09},
    "2009": {"RR": 17.18, "PPV": 0.84, "CDR": 1.45, "ICR": 0.85, "se": 67.30, "sp": 82.93},
}


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


class DiagnosticApi:
    def bayes(self, prevalence: float, sensitivity: float, specificity: float) -> dict:
        n = 1000.0
        diseased = n * prevalence
        tp = diseased * sensitivity
        fn = diseased - tp
        tn = (n - diseased) * specificity
        fp = n - diseased - tn
        ppv = tp / (tp + fp)
        npv = tn / (tn + fn)
        curve = []
        for i in range(181):
            log_p = -4.0 + i * (3.7 / 180.0)
            p = 10**log_p
            value = sensitivity * p / (sensitivity * p + (1 - specificity) * (1 - p))
            curve.append([log_p, value])
        return {
            "N": n, "D": diseased, "TP": tp, "FN": fn, "TN": tn, "FP": fp,
            "ppv": ppv, "npv": npv, "curve": curve,
        }

    def reconstruct(self, year: str) -> dict:
        d = KNCSP[str(year)]
        n = 1000.0
        pos = n * d["RR"] / 100
        neg = n - pos
        tp = d["CDR"]
        fp = pos - tp
        fn = d["ICR"] * neg / 1000
        tn = neg - fn
        return {
            "published": d, "N": n, "pos": pos, "neg": neg, "TP": tp, "FP": fp,
            "FN": fn, "TN": tn, "se": tp / (tp + fn) * 100,
            "sp": tn / (tn + fp) * 100, "ppv": tp / (tp + fp) * 100,
            "prev": (tp + fn) / n * 100,
            "naiveSe": d["CDR"] / (d["CDR"] + d["ICR"]) * 100,
        }

    def roc(self, separation: float, cutoff: float, prevalence: float, fn_weight: float) -> dict:
        sensitivity = 1 - phi(cutoff - separation)
        specificity = phi(cutoff)
        auc = phi(separation / math.sqrt(2))
        cost = 1000 * (prevalence * (1 - sensitivity) * fn_weight + (1 - prevalence) * (1 - specificity))
        best = {"cost": float("inf"), "x": 0.0, "se": 0.0, "sp": 0.0}
        curve = []
        i = 0
        x = -3.0
        while x <= 5.00001:
            se = 1 - phi(x - separation)
            sp = phi(x)
            if i % 4 == 0:
                curve.append([1 - sp, se])
            relative_cost = prevalence * (1 - se) * fn_weight + (1 - prevalence) * (1 - sp)
            if relative_cost < best["cost"]:
                best = {"cost": relative_cost, "x": x, "se": se, "sp": sp}
            x += 0.005
            i += 1
        return {"se": sensitivity, "sp": specificity, "auc": auc, "cost": cost, "best": best, "curve": curve}

    def bias(self, lead: float, slow: float, nonprogressive: float, effect: float) -> dict:
        s5_base = 0.40
        s5_effect = 1 - (1 - s5_base) * (1 - effect)
        decay = -math.log(s5_effect) / 5
        lead_survival = math.exp(-decay * max(5 - lead, 0))

        interval, soj_fast, soj_slow = 2, 0.5, 3.0
        p_fast, p_slow = min(1, soj_fast / interval), min(1, soj_slow / interval)
        detected_slow, detected_fast = slow * p_slow, (1 - slow) * p_fast
        slow_share = detected_slow / max(detected_slow + detected_fast, 1e-9)
        fast_survival = 1 - (1 - 0.30) * (1 - effect)
        slow_survival = 1 - (1 - 0.80) * (1 - effect)
        base_mix = slow * slow_survival + (1 - slow) * fast_survival
        screen_mix = slow_share * slow_survival + (1 - slow_share) * fast_survival

        n = 10000
        progressive = n * (1 - nonprogressive)
        detected_nonprogressive = n * nonprogressive * 0.90
        screen_diagnoses = progressive + detected_nonprogressive
        over_survival = (progressive * s5_effect + detected_nonprogressive) / max(screen_diagnoses, 1)
        return {
            "s5Effect": s5_effect, "leadSurvival": lead_survival,
            "slowShare": slow_share, "baseMix": base_mix, "screenMix": screen_mix,
            "overSurvival": over_survival,
            "baseDeaths": progressive * (1 - s5_base), "deaths": progressive * (1 - s5_effect),
            "pairs": [[s5_effect * 100, lead_survival * 100], [base_mix * 100, screen_mix * 100], [s5_effect * 100, over_survival * 100]],
        }
