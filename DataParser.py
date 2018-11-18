import json


RAW_DATA_FILE = "data/asin+title+dimension.txt"
DATA_FILE_TITLE = "data/dataTitle.txt"
DATA_FILE_DIMESIONS = "data/dataDimesions.txt"


def main():
    loop = 0
    with open(RAW_DATA_FILE, "r") as dp:
        with open(DATA_FILE_TITLE, "w") as fTitle:
            with open(DATA_FILE_DIMESIONS, "w") as fDimension:
                for line in dp:
                    obj = json.loads(line)
                    tmp = obj['title'].replace('\n', " ")
                    fTitle.write(tmp)
                    fTitle.write("\n")

                    tmp = str(obj['length']) + " " + str(obj['height']) + " " + str(obj['width']) + " " + \
                          str(obj["weight"]) + "\n"
                    fDimension.write(tmp)

                    loop += 1
                    if loop % 1000 == 0:
                        print(loop)

                    if loop == 1000000:
                        break


if __name__ == "__main__":
    main()
