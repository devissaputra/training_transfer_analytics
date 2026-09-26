"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from training_transfer_analytics import core
outputs={'final/first follow-up: .6/.8': .6/.8, 'change from baseline: .6-.3': .6-.3, '30-day change: (.6-.8)/60×30': (.6-.8)/60*30}
result={'kind':'illustrative_calculation','note':'Illustrative application-score trajectory; no causal attribution.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
