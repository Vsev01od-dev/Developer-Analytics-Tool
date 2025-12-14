from typing import List, Dict, Any
from collections import defaultdict


def group_by_position(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped = defaultdict(list)
    for developer in data:
        grouped[developer['position']].append(developer)
    return dict(grouped)

def calculate_average_performance(developers: List[Dict[str, Any]]) -> float:
    if not developers:
        return 0.0
    return sum(dev['performance'] for dev in developers) / len(developers)