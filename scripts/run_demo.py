import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from training_transfer_analytics.core import transfer_index, retention_adjusted, barrier_flags

index=transfer_index(.8,.7,.9,.8)
print(f"Transfer index: {index:.3f}")
print(f"30-day adjusted score: {retention_adjusted(index,30):.3f}")
print('Barrier flags:', barrier_flags(.3,.8,.9))
