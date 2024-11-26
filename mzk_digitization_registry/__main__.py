import argparse
from .client import DigitizationRegistryClient


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--barcode", help="Barcode to search for")
    argparser.add_argument(
        "--cnb",
        help="CNB to search for",
    )
    argparser.add_argument(
        "--isxn",
        help="ISXN to search for",
    )
    argparser.add_argument(
        "--year",
        help="Year of the volume to search for",
    )
    argparser.add_argument(
        "--volume",
        help="Volume to search for",
    )
    argparser.add_argument(
        "--bundle",
        help="Bundle to search for",
    )
    argparser.add_argument(
        "--barcodes-file",
        help="File with barcodes to search for",
    )

    args = argparser.parse_args()

    if (
        args.barcode is None
        and args.cnb is None
        and args.isxn is None
        and args.barcodes_file is None
    ):
        print(
            "One of --barcode, --cnb, --isxn "
            "or --barcodes-file must be provided"
        )
        argparser.print_help()
        exit(0)

    client = DigitizationRegistryClient()

    if args.barcodes_file:
        with open(args.barcodes_file) as f:
            barcodes = [line.strip() for line in f]
        for barcode in barcodes:
            record = client.get_record_by_barcode(barcode)
            if record:
                print(f"{barcode},{record.digitization_state.value}")
            else:
                print(f"{barcode},NotFound")

    records = (
        client.get_record_by_barcode(args.barcode) if args.barcode else []
    )

    if not records or (args.cnb or args.isxn):
        records.extend(
            client.get_issue_records(
                cnb=args.cnb,
                isxn=args.isxn,
            )
        )

    if not args.barcode and not args.year and not args.volume:
        output = "\n----------\n1".join(str(record) for record in records)
        print(output)
        exit(0)

    record = client.select_volume_record(
        records, args.barcode, args.year, args.volume, args.bundle
    )

    print(str(record) if record else "Not found")


if __name__ == "__main__":
    main()
