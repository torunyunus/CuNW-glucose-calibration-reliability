"""Run the six dependency-free regression checks without requiring pytest."""
import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parent
count = 0
for path in sorted((root / 'tests').glob('test_*.py')):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in sorted(vars(module)):
        if name.startswith('test_') and callable(getattr(module, name)):
            getattr(module, name)()
            print('PASS', path.name, name)
            count += 1
print(f'{count} regression checks passed.')
