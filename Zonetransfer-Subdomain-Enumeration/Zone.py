import argparse
import socket
import dns.resolver
import dns.rdatatype
import dns.query
import dns.zone
import dns.exception
import warnings
import sys


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
            target = subdomain + "." + hostname
            ip_address = perform_forward_lookup(target)
            if ip_address:
                reverse_lookup_result = perform_reverse_lookup(ip_address)
                dns_record_type = get_dns_record_type(target)
                dns_record_name = reverse_lookup_result if reverse_lookup_result else "N/A"
                dns_record_type_str = dns.rdatatype.to_text(dns_record_type) if dns_record_type else "N/A"
                print(f"Subdomain: {target} | IP: {ip_address} | DNS Record Name: {dns_record_name} | DNS Record Type: {dns_record_type_str}")

    except FileNotFoundError:
        print(f"Subdomains file '{subdomains_file}' not found.")


def dump_zone_file(domain):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            ns_query = dns.resolver.resolve(domain, dns.rdatatype.NS)

        if len(ns_query) == 0:
            print("No NS records found for the domain.")
            return

        for ns in ns_query:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=DeprecationWarning)
                    ns_address = str(dns.resolver.resolve(str(ns), dns.rdatatype.A)[0])

                print(f"\nDumping zone file from {str(ns)} - {ns_address}...")
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_address, domain))
                    for name, node in zone.nodes.items():
                        rdatasets = node.rdatasets
                        for rdataset in rdatasets:
                            for rdata in rdataset:
                                if rdataset.rdtype == dns.rdatatype.A:
                                    print(f"{name} - {rdata.address}\t {name}.{domain}")
                except dns.exception.FormError:
                    print(f"Transfer not allowed for {str(ns)}")
                except dns.exception.SyntaxError:
                    print(f"Malformed data received from {str(ns)}")
                except dns.xfr.TransferError as e:
                    print(f"Zone transfer error from {str(ns)}: {e}")
            except dns.resolver.NoAnswer:
                print(f"No A record found for {str(ns)}")
    except dns.resolver.NXDOMAIN:
        print("Domain not found.")
    except dns.resolver.NoNameservers:
        print("No nameservers found for the domain.")


def main():
    parser = argparse.ArgumentParser(description="Perform forward lookup, subdomain enumeration, and zone transfer for a hostname")
    parser.add_argument("hostname", help="Hostname to perform the forward lookup")
    parser.add_argument("--enumerate", "-e", metavar="subdomains_file", help="Perform subdomain enumeration with the provided subdomains file")
    parser.add_argument("--zonetransfer", "-z", action="store_true", help="Attempt zone transfer for the domain")
    args = parser.parse_args()

    if args.enumerate:
        prefix = args.hostname.split(".", 1)[0]
        if not prefix:
            print("Note: Please provide a plain hostname (e.g. google.com) or with a prefix (e.g., www) for subdomain enumeration.")
            print()
            sys.exit()

        print("Performing subdomain enumeration:")
        perform_subdomain_enumeration(args.hostname, args.enumerate)
        print()

    if args.zonetransfer:
        if args.hostname.startswith("www."):
            print("Note: Zone transfer does not require a prefix (e.g., www) for the hostname.")
            print()
            sys.exit()

        print("Performing zone transfer:")
        dump_zone_file(args.hostname)
        print()

    print("Performing forward lookup for the main hostname:")
    ip_address = perform_forward_lookup(args.hostname)
    if ip_address:
        print(f"Hostname: {args.hostname} resolved to IP address: {ip_address}")


if __name__ == "__main__":
    main()
