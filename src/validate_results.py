"""Validate published aggregates and fail when a core invariant changes."""

import json
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "data" / "results.json"


def main() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    totals = {row["user_type"]: row["trips"] for row in data["totals"]}
    assert data["source"]["publisher"] == "City of Chicago Data Portal"
    assert data["source"]["period"] == "2019"
    assert totals == {"Customer": 880637, "Subscriber": 2937367}
    assert len(data["monthly"]) == 24
    assert len(data["weekday"]) == 14
    assert len(data["hourly"]) == 48
    for section in ("monthly", "weekday", "hourly"):
        for rider_type, expected in totals.items():
            observed = sum(row["trips"] for row in data[section] if row["user_type"] == rider_type)
            assert observed == expected, f"{section} total mismatch for {rider_type}"
    assert all(row["from_station_name"] for row in data["top_stations"])
    print("Results validated: 3,818,004 trips and all aggregate checks passed.")


if __name__ == "__main__":
    main()
