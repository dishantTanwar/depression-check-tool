import pickle

import pandas as pd

# load saved model
with open('./service/final_knn_model', 'rb') as f:
    model = pickle.load(f)

# load saved encoder
with open('./service/encoder', 'rb') as f:
    enc = pickle.load(f)


def get_prediction(cat_data, binary_data):

    cat_df = pd.DataFrame(
        enc.transform(pd.DataFrame.from_dict(cat_data)).toarray(),
        columns=enc.get_feature_names()
    )
    binary_df = pd.DataFrame.from_dict(binary_data)
    user_df = pd.concat([cat_df, binary_df], axis=1)
    result = model.predict(user_df)

    print("===================== SOL ==================")
    print(str(result))

    return result


def getDepLevel(score):
    if (score < 7):
        return 0
    elif (score < 15):
        return 1
    else:
        return 2
