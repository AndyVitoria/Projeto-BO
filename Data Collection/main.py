import pdf2txt
import txt2json


def main():
    pdf_dir = 'PDF'
    lote = 'lote.txt'
    csv_dir = 'CSV'
    json_dir = 'JSON'

#    pdf2txt.pdf2txt(lote, pdf_dir, csv_dir)

    txt2json.txt2json(csv_dir, json_dir, lote)
    return


if __name__ == '__main__':
    main()
