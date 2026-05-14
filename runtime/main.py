#!/usr/bin/env python3
"""AI_OS v3 Professional"""
from __future__ import annotations
import sys
from pathlib import Path

# Allow `python runtime/main.py` from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))

import argparse
import re
from dotenv import load_dotenv
load_dotenv()

from core.logger import log_event
from core.startup import validate as startup_validate
from core.identity import verify_identity
from core.unit_calc import calculate_unit_economics
from core.project_manager import save_run
from core.orchestrator import Orchestrator

MODES = [
    "meta_agent", "meta_prompt", "marketplace", "research",
    "visual", "code", "review", "decision",
    "legal", "medical", "tables", "writing", "summary",
]


def extract_number(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1)) if match else None


def run(args: argparse.Namespace) -> None:
    # 1. Startup validation
    errors = startup_validate(args.model)
    if errors:
        for e in errors:
            print(f"❌ {e}")
        sys.exit(1)

    # 2. Identity check
    try:
        verify_identity()
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    strict_block = ""

    # 3. Marketplace strict finance block
    if args.mode == "marketplace" and args.precision == "strict":
        try:
            price      = extract_number(r"Цена\s*(\d+)", args.goal)
            cogs       = extract_number(r"себестоимость\s*(\d+)", args.goal)
            commission = extract_number(r"комиссия\s*(\d+)", args.goal)
            logistics  = extract_number(r"логистика\s*(\d+)", args.goal)
            traffic    = extract_number(r"трафик\s*(\d+)", args.goal)
            cvr_raw    = extract_number(r"CVR\s*(\d+\.?\d*)", args.goal)
            ad         = extract_number(r"реклама\s*(\d+)", args.goal)

            missing = [
                name for name, val in [
                    ("цена", price), ("себестоимость", cogs),
                    ("комиссия", commission), ("логистика", logistics),
                    ("трафик", traffic), ("CVR", cvr_raw),
                ] if val is None
            ]
            if missing:
                raise ValueError(f"Не указаны обязательные числа: {', '.join(missing)}")

            assert price is not None
            assert cogs is not None
            assert commission is not None
            assert logistics is not None
            assert traffic is not None
            assert cvr_raw is not None

            if ad is None:
                print("⚠️  Реклама не указана — используется 0")

            calc = calculate_unit_economics(
                price=price, cogs=cogs,
                commission_percent=commission,
                logistics=logistics, traffic=traffic,
                cvr=cvr_raw / 100,
                ad_percent=ad,
            )
            strict_block = f"""
STRICT NUMERIC CALCULATION (Python authoritative)

Sales units: {calc['sales_units']}
Revenue: {calc['revenue']}
Commission per unit: {calc['commission_per_unit']}
Ad cost per unit: {calc['ad_cost_per_unit']}
Unit contribution: {calc['unit_contribution']}
Monthly contribution: {calc['monthly_contribution']}

Revenue MUST NOT be recalculated.
These numbers are final and authoritative.
"""
        except Exception as e:
            strict_block = f"\nSTRICT CALCULATION FAILED: {e}\n"

    user_input = (
        f"Precision mode: {args.precision}\n\n{strict_block}\nOriginal Input:\n{args.goal}"
        if args.mode == "marketplace" else args.goal
    )

    print(f"🚀 Mode: {args.mode} | Model: {args.model}")
    print(f"   Goal: {args.goal}")
    print("   Running...\n")

    orch = Orchestrator()
    result = orch.run(
        mode=args.mode, goal=user_input, model=args.model,
        temperature=args.temperature,
        agent_type=args.agent_type,
        risk_level=args.risk_level,
    )

    content = result.get("content", "")
    print("=" * 60)
    print(content)
    print("=" * 60)

    eval_score = result.get("eval_score", None)
    print(f"\n📊 Eval: {eval_score}")

    metadata = {
        "model":             result.get("model"),
        "latency":           result.get("latency"),
        "tokens_prompt":     result.get("tokens_prompt"),
        "tokens_completion": result.get("tokens_completion"),
        "eval_score":        eval_score,
        "precision":         args.precision,
    }
    log_event({"agent": args.mode, **metadata})

    if args.project:
        saved = save_run(args.project, args.mode, content, metadata)
        print(f"\n📁 Saved to project: {saved}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n💾 Saved: {args.output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI_OS v3 Professional")
    parser.add_argument("--diagnose", action="store_true",
                        help="Print system diagnostics and exit")
    parser.add_argument("--mode",        choices=MODES, default=None)
    parser.add_argument("--model",       default="openai")
    parser.add_argument("--goal",        default=None)
    parser.add_argument("--precision",   choices=["hypothesis", "approx", "strict"], default="hypothesis")
    parser.add_argument("--agent_type",  default=None)
    parser.add_argument("--risk_level",  default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--project")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    if args.diagnose:
        from core.diagnostics import run_diagnostics
        run_diagnostics()
        sys.exit(0)

    if not args.mode or not args.goal:
        parser.error("--mode and --goal are required")

    run(args)


if __name__ == "__main__":
    main()
