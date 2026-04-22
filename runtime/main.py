#!/usr/bin/env python3
"""AI_OS v3 Professional — CLEAN ORCHESTRATOR VERSION"""

import argparse
import sys
import re

from dotenv import load_dotenv
load_dotenv()

from core.identity import verify_identity
from core.agent_registry import build_default_registry
from core.conflict_protocol import authorize
from core.logger import log_event
from core.unit_calc import calculate_unit_economics
from core.project_manager import save_run
from core.orchestrator import Orchestrator


MODES = ["meta_agent", "meta_prompt", "marketplace", "research", "visual"]


def extract_number(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    return float(match.group(1))


def run(args):

    # 1. Identity check
    try:
        verify_identity()
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    registry = build_default_registry()
    agent = registry.get(args.mode)

    if not agent:
        print(f"❌ Unknown mode: {args.mode}")
        sys.exit(1)

    skill = args.agent_type if args.mode == "meta_agent" else agent["skill"]
    risk = args.risk_level if args.mode == "meta_agent" else agent["risk"]

    # 2. Conflict check
    try:
        authorize(skill, risk)
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    strict_block = ""
    calc = None

    # 3. STRICT FINANCE BLOCK (оставляем)
    if args.mode == "marketplace" and args.precision == "strict":
        try:
            price = extract_number(r"Цена\s*(\d+)", args.goal)
            cogs = extract_number(r"себестоимость\s*(\d+)", args.goal)
            commission = extract_number(r"комиссия\s*(\d+)", args.goal)
            logistics = extract_number(r"логистика\s*(\d+)", args.goal)
            traffic = extract_number(r"трафик\s*(\d+)", args.goal)
            cvr_raw = extract_number(r"CVR\s*(\d+\.?\d*)", args.goal)
            ad = extract_number(r"реклама\s*(\d+)", args.goal)

            if None in [price, cogs, commission, logistics, traffic, cvr_raw]:
                raise ValueError("Missing required numeric inputs")

            cvr = cvr_raw / 100

            calc = calculate_unit_economics(
                price=price,
                cogs=cogs,
                commission_percent=commission,
                logistics=logistics,
                traffic=traffic,
                cvr=cvr,
                ad_percent=ad
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

    # 4. Формирование input
    if args.mode == "marketplace":
        user_input = f"""
Precision mode: {args.precision}

{strict_block}

Original Input:
{args.goal}
"""
    else:
        user_input = args.goal

    print(f"🚀 Mode: {args.mode}")
    print(f"   Precision: {args.precision}")
    print(f"   Goal: {args.goal}")
    print("   Orchestrator running...\n")

    # =========================
    # 🔥 ЕДИНАЯ ТОЧКА УПРАВЛЕНИЯ
    # =========================
    orch = Orchestrator()

    result = orch.run(
    mode=args.mode,
    goal=user_input,
    model=args.model,          
    temperature=args.temperature
    )    # =========================

    content = result.get("content", "")

    print("=" * 60)
    print(content)
    print("=" * 60)

    # 5. Eval (оставляем)
    eval_score = result.get("eval_score", None)

    print(f"\n📊 Eval: {eval_score}")

    metadata = {
        "model": result.get("model"),
        "latency": result.get("latency"),
        "tokens_prompt": result.get("tokens_prompt"),
        "tokens_completion": result.get("tokens_completion"),
        "eval_score": eval_score,
        "precision": args.precision
    }

    log_event({
        "agent": args.mode,
        **metadata
    })

    # 6. Save project
    if args.project:
        saved_path = save_run(
            project_name=args.project,
            mode=args.mode,
            content=content,
            metadata=metadata
        )
        print(f"\n📁 Saved to project: {saved_path}")

    # 7. Save file
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n💾 Saved: {args.output}")


def main():
    parser = argparse.ArgumentParser(description="AI_OS v3 Professional")

    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--model", default="openai")  # openai | claude | gemini
    parser.add_argument("--goal", required=True)
    parser.add_argument("--precision", choices=["hypothesis", "approx", "strict"], default="hypothesis")
    parser.add_argument("--agent_type", default="analyzer")
    parser.add_argument("--risk_level", default="medium")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--project")
    parser.add_argument("--output", "-o")

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()