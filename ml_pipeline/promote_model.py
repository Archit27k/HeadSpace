import argparse
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser(description="Promote a model version to a specific alias.")
    parser.add_argument("--version", type=str, required=True, help="The version number to promote.")
    parser.add_argument("--alias", type=str, required=True, help="The alias to assign (e.g., 'champion', 'candidate').")
    
    args = parser.parse_args()
    
    registry = RegistryClient()
    registry.assign_alias(args.version, args.alias)

if __name__ == "__main__":
    main()
