import argparse
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser(description="Rollback an alias to a previous version.")
    parser.add_argument("--alias", type=str, required=True, help="The alias to rollback (e.g., 'champion').")
    parser.add_argument("--target-version", type=str, required=True, help="The version number to rollback to.")
    
    args = parser.parse_args()
    
    registry = RegistryClient()
    print(f"Rolling back '{args.alias}' to version {args.target_version}...")
    registry.assign_alias(args.target_version, args.alias)
    print("Rollback complete.")

if __name__ == "__main__":
    main()
