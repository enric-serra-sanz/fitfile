import argparse
import os

from fitfile.data_managers import (
    JsonDataManager,
    CsvDataManager,
    ExcelDataManager,
)
from fitfile.data_rules import (
    AgeBandRule,
    PostCodeTrimToTwoRule,
    PostCodeTrimToThreeRule,
)
import logging


argument_parser = argparse.ArgumentParser(
    prog='Fitfile data manager',
    description='Parses excel, csv or json files, validates and applies rules',
    epilog='For any queries enricserrasanz@gmail.com')

argument_parser.add_argument('--json-file', dest='json_file',
                             help='The location of PatientCohorts.json', required=True)
argument_parser.add_argument('--csv-file', dest='csv_file', help='The location of customer.csv',
                             required=True)
argument_parser.add_argument('--excel-file', dest='excel_file',
                             help='The location of ResearchList.xlsx', required=True)
argument_parser.add_argument('--output-dir', dest='output_dir',
                             help='The output directory to save the outputs', required=True)
argument_parser.add_argument('--log-dir', dest='log_dir', required=False, default=None,
                             help='The output directory to save the outputs')


def main() -> None:
    args = argument_parser.parse_args()
    json_out = os.path.join(args.output_dir, 'PatientCohortsOutput.json')
    csv_out = os.path.join(args.output_dir, 'customerOutput.json')
    excel_out = os.path.join(args.output_dir, 'ResearchListOutput.json')

    if args.log_dir is None:

        process_1 = CsvDataManager(
            input_file_path=args.csv_file,
            output_file_path=csv_out,
            request_id='123',
        )
        p1_r1 = AgeBandRule(fields=['dob'], logger=process_1.logger)
        process_1.set_rules([p1_r1])
        process_1.run()
        process_2 = JsonDataManager(
            input_file_path=args.json_file,
            output_file_path=json_out,
            request_id='7282',
        )
        p2_r1 = AgeBandRule(fields=['age'], logger=process_2.logger)
        p2_r2 = PostCodeTrimToThreeRule(fields=['PostCode'], logger=process_2.logger)
        process_2.set_rules([p2_r1, p2_r2])
        process_2.run()

        process_3 = ExcelDataManager(
            input_file_path=args.excel_file,
            output_file_path=excel_out,
            request_id='92421'
        )
        p3_r1 = PostCodeTrimToThreeRule(fields=['PostCode'], logger=process_3.logger)
        p3_r2 = PostCodeTrimToTwoRule(fields=['PostCode'], logger=process_3.logger)
        process_3.set_rules([p3_r1, p3_r2])
        process_3.run()

    else:
        logging.basicConfig(filename=os.path.join(args.log_dir, 'CsvProcessing_123.log'),
                            filemode='w',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logger = logging.getLogger('CsvDataManager')

        process_1 = CsvDataManager(
            input_file_path=args.csv_file,
            output_file_path=csv_out,
            request_id='123',
            logger=logger,
        )
        p1_r1 = AgeBandRule(fields=['dob'], logger=process_1.logger)
        process_1.set_rules([p1_r1])
        process_1.run()

        logging.basicConfig(filename=os.path.join(args.log_dir, 'JsonProcessing_7282.log'),
                            filemode='w',
                            datefmt='%H:%M:%S',
                            level=logging.INFO,
                            force=True)

        logger = logging.getLogger('JsonDataManager')
        process_2 = JsonDataManager(
            input_file_path=args.json_file,
            output_file_path=json_out,
            request_id='7282',
            logger=logger,
        )
        p2_r1 = AgeBandRule(fields=['age'], logger=process_2.logger)
        p2_r2 = PostCodeTrimToThreeRule(fields=['PostCode'], logger=process_2.logger)
        process_2.set_rules([p2_r1, p2_r2])
        process_2.run()

        logging.basicConfig(filename=os.path.join(args.log_dir, 'ExcelProcessing_92421.log'),
                            filemode='w',
                            datefmt='%H:%M:%S',
                            level=logging.INFO,
                            force=True)

        logger = logging.getLogger('ExcelDataManager')
        process_3 = ExcelDataManager(
            input_file_path=args.excel_file,
            output_file_path=excel_out,
            request_id='92421',
            logger=logger,
        )
        p3_r1 = PostCodeTrimToThreeRule(fields=['PostCode'], logger=process_3.logger)
        p3_r2 = PostCodeTrimToTwoRule(fields=['PostCode'], logger=process_3.logger)
        process_3.set_rules([p3_r1, p3_r2])
        process_3.run()


if __name__ == '__main__':
    main()
