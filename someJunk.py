# Get Names from cert.sh and do a reverse DNS lookup.

# import libraries.
import requests
import pandas as pd
import dns.resolver

# Get Initial results and build a list.
def runQuery():
    # Build the query and format it.
    query = input("Enter entity to search: ")
    query = query.replace(" ", "+")

    # Make the request to the webserver.
    request = requests.get(f"https://crt.sh/?q={query}")

    # Check for a 200 OK. If good, we proceed.
    if request.status_code == 200:
        print(f"[+] Pulling Common Names list.")
        dfs = pd.read_html(request.text)
        df = dfs[2]
        common_name = df["Common Name"]
        common_name = common_name.drop_duplicates()
        common_name = common_name.str.replace(r"\*.", "", regex=True)
        common_name.to_csv("common_names", header=False, index=False)
    # If we get anything other than a 200 OK, we print the error code.
    else:
        print(f"Failed with status code: {request.status_code}.")
        exit()


# Create a function to pull our DNS records.
def dns_lookup():
    with open("common_names", "r") as host_list:
        for host in host_list:
            try:
                host_stripped = host.strip()
                request_host = requests.get(f"https://{host_stripped}")
                # print(f"[+] {host_stripped} - {request_host.status_code}") # commented out. Used for a quick test.
                result = dns.resolver.resolve(host_stripped, "A")
                for ipval in result:
                    print(
                        f"[+] {host_stripped} - Request Status Code {request_host.status_code} - ",
                        ipval.to_text(),
                    )

            except:
                print(f"[+] Failed to resolve IP for {host_stripped}.")


# Run the script, function-by-function.
runQuery()
dns_lookup()
