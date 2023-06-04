import argparse
import socket
import dns.resolver
import dns.rdatatype

def perform_forward_lookup(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        if ip_address != "127.0.0.1":
            return ip_address
    except socket.gaierror as e:
        pass

def perform_reverse_lookup(ip_address):
    try:
        result = dns.resolver.resolve_address(ip_address)
        if result:
            return result[0].to_text()
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        pass

def get_dns_record_type(hostname):
    try:
        result = dns.resolver.resolve(hostname)
        if result:
            return result.rdtype
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        pass

def perform_subdomain_enumeration(hostname, subdomains_file):
    try:
        with open(subdomains_file) as file:
            subdomains = file.read().splitlines()

        for subdomain in subdomains:
            parts = hostname.split(".", 1)
            target = subdomain + "." + parts[1]  # Strip the first part of the domain
            ip_address = perform_forward_lookup(target)
            if ip_address:
                reverse_lookup_result = perform_reverse_lookup(ip_address)
                dns_record_type = get_dns_record_type(target)
                dns_record_name = reverse_lookup_result if reverse_lookup_result else "N/A"
                dns_record_type_str = dns.rdatatype.to_text(dns_record_type) if dns_record_type else "N/A"
                print(f"Subdomain: {target} | IP: {ip_address} | DNS Record Name: {dns_record_name} | DNS Record Type: {dns_record_type_str}")

    except FileNotFoundError:
        print(f"Subdomains file '{subdomains_file}' not found.")

def main():
    parser = argparse.ArgumentParser(description="Perform forward lookup and subdomain enumeration for a hostname")
    parser.add_argument("hostname", help="Hostname to perform the forward lookup")
    parser.add_argument("--enumerate", "-e", metavar="subdomains_file", help="Perform subdomain enumeration with the provided subdomains file")
    args = parser.parse_args()

    if args.enumerate:
        print("Performing subdomain enumeration:")
        perform_subdomain_enumeration(args.hostname, args.enumerate)
        print()

    print("Performing forward lookup for the main hostname:")
    ip_address = perform_forward_lookup(args.hostname)
    if ip_address:
        print(f"Hostname: {args.hostname} resolved to IP address: {ip_address}")

if __name__ == "__main__":
    main()

