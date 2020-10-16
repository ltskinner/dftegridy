
import pandas as pd
import dftegrity


def build_profile():
    original_df = pd.DataFrame({
        'record_id': [1, 2, 3, 4, 5],
        'name': ['Joe', 'John', 'David', 'Brett', 'Richard'],
        'occupation': ['Carpenter', 'Carpenter', 'Surveyor', 'Driver', 'Mechanic'],
    })

    # 1) Configure the Data Units of the columns
    dunit_config = {
        'record_id': dftegrity.dunits.ID_UNIQUE,
        'name': dftegrity.dunits.LABEL,
        'occupation': dftegrity.dunits.CATEGORICAL,
    }

    # 2) Create DFID object, profile the data, and save the profile
    dfid_profile_path = './example_simple_dfid_profile.yaml'
    dfid = dftegrity.DFID(dunit_config=dunit_config)
    profile = dfid.profile(original_df)
    dfid.save_profile(dfid_profile_path)


def verify_df():
    compare_df = pd.DataFrame({
        'record_id': [6, 7],
        'name': ['Paul', 'Jacob'],
        'occupation': ['Driver', 'Technician'],
        'random_new_col': ['something', 'anotherthing'],
    })

    # 1) Load the expected profile of your DF
    dfid_profile_path = './example_simple_dfid_profile.yaml'
    dfid = dftegrity.DFID()
    profile = dfid.load_profile(dfid_profile_path)

    # 2) Verify the new DF and review the report for inconsistencies
    report = dfid.verify(compare_df, skip_unverified=False)  # defaults to True
    print('\n')
    dfid.print_verification_report()


if __name__ == '__main__':
    build_profile()
    verify_df()
