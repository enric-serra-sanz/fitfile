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
import os


def main() -> None:
    file_dir = os.path.join(os.path.dirname(__file__), '../../20230320_FITFILEPythonTest')

    json_file = os.path.join(file_dir, 'PatientCohorts.json')
    json_out = os.path.join(file_dir, 'PatientCohortsOutput.json')
    csv_file = os.path.join(file_dir, 'customer.csv')
    csv_out = os.path.join(file_dir, 'customerOutput.json')
    excel_file = os.path.join(file_dir, 'ResearchList.xlsx')
    excel_out = os.path.join(file_dir, 'ResearchListOutput.json')

    process_1 = CsvDataManager(
        input_file_path=csv_file,
        output_file_path=csv_out,
        process_id='123',
    )
    p1_r1 = AgeBandRule(fields=['dob'])
    process_1.set_rules([p1_r1])
    process_1.run()
    process_2 = JsonDataManager(
        input_file_path=json_file,
        output_file_path=json_out,
        process_id='7282',
    )
    p2_r1 = AgeBandRule(fields=['age'])
    p2_r2 = PostCodeTrimToThreeRule(fields=['PostCode'])
    process_2.set_rules([p2_r1, p2_r2])
    process_2.run()

    process_3 = ExcelDataManager(
        input_file_path=excel_file,
        output_file_path=excel_out,
        process_id='92421'
    )
    p3_r1 = PostCodeTrimToThreeRule(fields=['PostCode'])
    p3_r2 = PostCodeTrimToTwoRule(fields=['PostCode'])
    process_3.set_rules([p3_r1, p3_r2])
    process_3.run()


if __name__ == '__main__':
    main()
