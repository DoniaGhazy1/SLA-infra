# rules/evaluator.py

import re
import operator

OPS = {
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt
}

def eval_condition(value: float, condition: str) -> bool:
    """
    Parse and apply a simple numeric condition (e.g. "value <= 50").
    
    for sym, fn in OPS.items():
        if sym in condition:
            threshold = float(condition.split(sym)[1])
            return fn(value, threshold)
    raise ValueError(f"Unsupported condition: {condition}")
    """
    m = re.search(r"value\s*(" + "|".join(map(re.escape, OPS.keys())) + r")\s*([0-9\.]+)", condition)
    if not m:
        raise ValueError(f"Unsupported condition format: {condition}")
    op_sym, num = m.group(1), m.group(2)
    threshold = float(num)
    return OPS[op_sym](value, threshold)

