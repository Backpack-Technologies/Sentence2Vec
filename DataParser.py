import json


RAW_DATA_FILE = "data/asin+title.txt"
DATA_FILE = "data/data.txt"


def main():
    loop = 0
    with open(RAW_DATA_FILE, "r") as dp:
        with open(DATA_FILE, "w") as op:
            for line in dp:
                obj = json.loads(line)
                # print(obj["asin"], obj["title"], len(obj["title"]))
                if len(obj["title"]) > 0:
                    op.write(obj["title"])
                    op.write("\n")
                loop += 1

                if loop % 1000 == 0:
                    print(loop)


if __name__ == "__main__":
    main()
