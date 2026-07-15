import argparse
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser(description="Compare metrics between two model versions by their aliases.")
    parser.add_argument("--alias1", type=str, required=True, help="First alias (e.g., 'champion').")
    parser.add_argument("--alias2", type=str, required=True, help="Second alias (e.g., 'candidate').")
    
    args = parser.parse_args()
    registry = RegistryClient()
    
    v1 = registry.get_model_version_by_alias(args.alias1)
    v2 = registry.get_model_version_by_alias(args.alias2)
    
    if not v1 or not v2:
        print("Could not find both aliases.")
        return
        
    print(f"Comparing {args.alias1} (v{v1}) with {args.alias2} (v{v2})...")
    # Fetch run details
    runs = registry.client.search_model_versions(f"name='{registry.model_name}'")
    run1_id = next((r.run_id for r in runs if r.version == v1), None)
    run2_id = next((r.run_id for r in runs if r.version == v2), None)
    
    if not run1_id or not run2_id:
        print("Could not fetch run info.")
        return
        
    run1 = registry.client.get_run(run1_id)
    run2 = registry.client.get_run(run2_id)
    
    metrics1 = run1.data.metrics
    metrics2 = run2.data.metrics
    
    print("\n| Metric |", args.alias1.ljust(15), "|", args.alias2.ljust(15), "| Diff |")
    print("-" * 65)
    
    for metric_name in metrics1.keys():
        val1 = metrics1.get(metric_name, 0.0)
        val2 = metrics2.get(metric_name, 0.0)
        diff = val1 - val2
        diff_str = f"+{diff:.4f}" if diff > 0 else f"{diff:.4f}"
        print(f"| {metric_name.ljust(15)} | {val1:<15.4f} | {val2:<15.4f} | {diff_str:<10} |")

if __name__ == "__main__":
    main()
