# Python-DNS
A set of Python tools that I developed to perform different DNS Recognition

## Zone

**Usage**

```shell
# Perform Zonetransfer
python3 Zone.py -z hostname

# Enumerate subdomain
python3 Zone.py -e /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt hostname

# Both at the same time
python3 Zone.py -z -e ./subdomainlist.txt hostname

# Display Help
python3 Zone.py -h
usage: ZoneSubEnum.py [-h] [--enumerate subdomains_file] [--zonetransfer] hostname

Perform forward lookup, subdomain enumeration, and zone transfer for a
hostname

positional arguments:
  hostname              Hostname to perform the forward lookup

options:
  -h, --help            show this help message and exit
  --enumerate subdomains_file, -e subdomains_file
                        Perform subdomain enumeration with the provided
                        subdomains file
  --zonetransfer, -z    Attempt zone transfer for the domain
```

---

## Subdomain

**Usage**

```shell
# Enum
python3 Subdomain.py -e /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt www.domain.com

# Display Help
usage: Subdomain.py [-h] [--enumerate subdomains_file] hostname

Perform forward lookup and subdomain enumeration for a hostname

positional arguments:
  hostname              Hostname to perform the forward lookup

options:
  -h, --help            show this help message and exit
  --enumerate subdomains_file, -e subdomains_file
                        Perform subdomain enumeration with the provided
                        subdomains file
```

---

## Nameserver-Enum

**Usage**

```shell
# Enum
python3 Nameserver-Enum.py hostname

# Display Help
usage: Nameserver-Enum.py [-h] domain

Get name servers for a domain

positional arguments:
  domain      Domain name

options:
  -h, --help  show this help message and exit
```
