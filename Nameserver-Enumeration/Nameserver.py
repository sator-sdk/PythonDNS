import argparse
import dns.resolver

def get_name_servers(domain):
    try:
        result = dns.resolver.resolve(domain, dns.rdatatype.NS)
        if result:
            name_servers = [ns.to_text() for ns in result]
            return name_servers
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        pass

def save_name_servers(name_servers, filename):
    with open(filename, 'w') as file:
        for ns in name_servers:
            ns = ns.rstrip('.')  # Remove trailing dot
            file.write(ns + '\n')

def main():
    parser = argparse.ArgumentParser(description="Get name servers for a domain")
    parser.add_argument("domain", help="Domain name")
    args = parser.parse_args()

    filename = args.domain + ".txt"
    name_servers = get_name_servers(args.domain)
    if name_servers:
        save_name_servers(name_servers, filename)
        print(f"Name servers saved successfully in {filename}")
        print("Successful discovery of name servers:")
        for ns in name_servers:
            print(ns.rstrip('.'))  # Remove trailing dot
    else:
        print("No name servers found for the domain.")

if __name__ == "__main__":
    main()
