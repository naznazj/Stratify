"""
STRATIFY Command-Line Interface (CLI)
Usage:
  python stratify.py "/stratify Healthcare"
  python stratify.py "/stratify Real Estate --location Philippines --depth deep"
  python stratify.py "/stratify compare Healthcare vs Wellness"
  python stratify.py --repl
"""
import sys
import os
import argparse
import json

# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

from stratify_core.orchestrator import StratifyOrchestrator

def print_banner():
    banner = r"""
  ____ _____ ____      _  _____ ___ _______   __
 / ___|_   _|  _ \    / \|_   _|_ _|  ___\ \ / /
 \___ \ | | | |_) |  / _ \ | |  | || |_   \ V / 
  ___) || | |  _ <  / ___ \| |  | ||  _|   | |  
 |____/ |_| |_| \_\/_/   \_\_| |___|_|     |_|  
                                                
 Business Intelligence & Strategic Marketing Engine
 Official Command: /stratify [industry] [--location <loc>] [--depth <quick|standard|deep>]
"""
    print(banner)

def render_cli_report(report: dict):
    if "comparison_id" in report:
        print("\n" + "="*80)
        print("\n" + "="*80)
        print(f"[STRATIFY INDUSTRY COMPARISON] {report['industry_1_name']} vs {report['industry_2_name']}")
        print("="*80)
        print(f"Geographic Scope: {report['location']}")
        print(f"Strategic Winner: {report['winner_summary']}\n")
        
        ind1 = report['industry_1']
        ind2 = report['industry_2']
        print(f"{'Metric':<30} | {ind1['name']:<25} | {ind2['name']:<25}")
        print("-"*85)
        print(f"{'Market TAM':<30} | {ind1['tam']:<25} | {ind2['tam']:<25}")
        print(f"{'Growth CAGR':<30} | {ind1['cagr']:<25} | {ind2['cagr']:<25}")
        print(f"{'Top Opportunity Score':<30} | {ind1['top_opportunity_score']:<25} | {ind2['top_opportunity_score']:<25}")
        print(f"{'Top Opportunity Concept':<30} | {ind1['top_opportunity_name']:<25} | {ind2['top_opportunity_name']:<25}")
        print(f"{'Verified Prospects Found':<30} | {ind1['prospects_count']:<25} | {ind2['prospects_count']:<25}")
        print(f"{'Competitors Analyzed':<30} | {ind1['competitors_count']:<25} | {ind2['competitors_count']:<25}")
        print("="*85 + "\n")
        return

    print("\n" + "="*80)
    print(f"[STRATIFY RESEARCH REPORT] {report['industry'].upper()}")
    print("="*80)
    print(f"Location Market: {report['location']} {'(Default Assumption)' if report['is_default_location'] else ''}")
    print(f"Research Depth: {report['depth'].upper()} | Execution Duration: {report['execution_duration_sec']}s")
    print(f"Top Opportunity Score: {report['top_opportunity_score']}/100")
    
    # Routing & Token metrics
    rm = report['skill_routing']
    tm = report['token_metrics']
    print(f"Skills Activated: {rm['selected_count']}/{rm['total_skills_available']} ({', '.join(s['id'] for s in rm['selected_skills'][:4])}...)")
    print(f"Routing Efficiency: {rm['efficiency_percentage']}% token reduction ({rm['total_token_weight_saved']:,} tokens saved)")
    print(f"Token Consumption: {tm['total_tokens']:,} tokens | Est. API Cost: ${tm['estimated_total_cost_usd']:.5f}")

    # Section A: Market Overview
    print("\n" + "-"*80)
    print("SECTION A: MARKET OVERVIEW & SIZING")
    print("-"*80)
    mkt = report['market_overview']
    print(f"- TAM: {mkt['tam']}")
    print(f"- SAM: {mkt['sam']}")
    print(f"- SOM: {mkt['som']}")
    print(f"- CAGR: {mkt['cagr']}")
    print(f"\n{mkt['market_overview']}\n")
    print("Key Industry Trends:")
    for t in mkt['key_trends']:
        print(f"  * {t}")

    # Section B: Business Opportunities
    print("\n" + "-"*80)
    print("SECTION B: RANKED BUSINESS OPPORTUNITIES")
    print("-"*80)
    for i, opp in enumerate(report['opportunities'][:5], 1):
        print(f"\n[{i}] {opp['name']} (Score: {opp['overall_score']}/100 - {opp['confidence_level']})")
        print(f"    Concept: {opp['concept']}")
        print(f"    Target:  {opp['target_audience']}")
        print(f"    Revenue: {opp['revenue_model']}")
        print(f"    Moat:    {opp['competitive_advantage']}")
        print(f"    Diff:    {opp['execution_difficulty']}")

    # Section C: Customers
    print("\n" + "-"*80)
    print("SECTION C: CUSTOMER INTELLIGENCE & PERSONAS")
    print("-"*80)
    cust = report['customer_intelligence']
    for seg in cust['customer_segments']:
        print(f"- Segment: {seg['name']} ({seg['type']})")
        print(f"  Purchasing Power: {seg['purchasing_power']}")
        print(f"  Primary Motivation: {seg['buying_motivation']}")

    # Section D: High-Value Targets
    print("\n" + "-"*80)
    print("SECTION D: HIGH-VALUE VERIFIED PROSPECTS (Zero Fabrication)")
    print("-"*80)
    for p in report['prospects']:
        print(f"- {p['company_name']} ({p['location']}) - Fit Score: {p['fit_score']}/100")
        print(f"  Domain: {p['website']}")
        print(f"  Signal: {p['public_buying_signals']}")
        print(f"  Outreach: {p['recommended_outreach']}")

    # Section E: Competitors
    print("\n" + "-"*80)
    print("SECTION E: COMPETITOR TEARDOWN & WHITE SPACE")
    print("-"*80)
    for c in report['competitor_intelligence']['competitors']:
        print(f"- {c['name']} ({c['type']}) - {c['website']}")
        print(f"  Pricing: {c['pricing']}")
        print(f"  Gaps:    {c['market_gap']}")

    # Section F: Marketing
    print("\n" + "-"*80)
    print("SECTION F: CUSTOMIZED MARKETING STRATEGY")
    print("-"*80)
    mkt_strat = report['marketing_strategy']
    print(f"Positioning: {mkt_strat['positioning_statement']}\n")
    print("Recommended Channels:")
    for ch in mkt_strat['recommended_channels']:
        print(f"  - {ch['channel']} ({ch['priority']}): {ch['rationale']}")

    # Section G: 90-Day Execution Plan
    print("\n" + "-"*80)
    print("SECTION G: STRATEGIC ACTION ROADMAP")
    print("-"*80)
    plan = report['business_strategy']['strategic_action_plan']
    print("First 7 Days:")
    for step in plan['first_7_days']:
        print(f"  [ ] {step['task']} (KPI: {step['kpi']})")
    print("\nFirst 30 Days:")
    for step in plan['first_30_days']:
        print(f"  [ ] {step['task']} (KPI: {step['kpi']})")

    # Citations
    print("\n" + "-"*80)
    print(f"VERIFIED RESEARCH CITATIONS ({len(report['citations'])} sources)")
    print("-"*80)
    for cit in report['citations'][:4]:
        print(f"  [{cit['classification']}] {cit['source_name']}: {cit['source_url']}")
    print("="*80 + "\n")

def main():
    orchestrator = StratifyOrchestrator()
    print_banner()

    if len(sys.argv) > 1 and sys.argv[1] not in ["--repl", "-i"]:
        raw_cmd = " ".join(sys.argv[1:])
        print(f"Running: {raw_cmd}\n")
        report = orchestrator.execute_command(raw_cmd)
        render_cli_report(report)
        return

    # REPL mode
    print("Interactive REPL active. Type any /stratify command or 'exit' to quit.\n")
    while True:
        try:
            user_input = input("STRATIFY > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting STRATIFY. Goodbye!")
                break
            report = orchestrator.execute_command(user_input)
            render_cli_report(report)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting STRATIFY.")
            break
        except Exception as e:
            print(f"\n[Error] {e}\n")

if __name__ == "__main__":
    main()
