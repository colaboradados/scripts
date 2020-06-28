import csv
import requests
import http.client

http.client._MAXHEADERS = 1000
tries = 5
last_exception = ""

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    )
}

test_bases = open("status-das-bases.txt", "w")
not_found_bases = open("bases-fora-do-ar.txt", "w")
inconsistent_bases = open("bases-inconsistentes.txt", "w")
exceptions = open("bases-com-excecoes.txt", "w")
no_certification = open("bases-sem-certificados.txt", "w")

with open('all_portals.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Cabeçalho: {} - {}".format(row[0], row[1]))
            line_count += 1
        else:
            for i in range(tries):
                try:
                    if last_exception == "SSLError":
                        base = requests.get(row[0], headers=headers, timeout=60, verify=False)
                        status_code = base.status_code
                    else:
                        base = requests.get(row[0], headers=headers, timeout=60)
                        status_code = base.status_code
                    print("{} - {} - {}".format(row[1], row[0], status_code))
                    last_exception = ""
                except requests.exceptions.RequestException as e:
                    print("Tentativa {}:".format(i+1))
                    print(e)
                    if e.__class__.__name__ == "SSLError":
                        last_exception = e.__class__.__name__
                        no_certification.write("{} - {} - {}\n".format(row[1], row[0], e))
                        continue
                    elif i < tries - 1:
                        continue
                    else:
                        exceptions.write("{} - {} - {}\n".format(row[1], row[0], e))
                break
            test_bases.write("{} - {} - {}\n".format(row[1], row[0], status_code))
            if status_code == 404:
               not_found_bases.write("{} - {} - {}\n".format(row[1], row[0], status_code))
            if status_code != 200 and status_code != 404:
               inconsistent_bases.write("{} - {} - {}\n".format(row[1], row[0], status_code))
print("Finished!")
test_bases.close()
