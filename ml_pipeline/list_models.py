from registry_client import RegistryClient

def main():
    registry = RegistryClient()
    versions = registry.list_all_versions()
    
    print(f"--- Registered Models for '{registry.model_name}' ---")
    if not versions:
        print("No models registered yet.")
        return
        
    for v in versions:
        aliases = v.aliases
        alias_str = f" [{', '.join(aliases)}]" if aliases else ""
        print(f"Version: {v.version} | Status: {v.status}{alias_str} | Run ID: {v.run_id}")

if __name__ == "__main__":
    main()
