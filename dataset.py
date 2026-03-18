import pandas as pd

df=pd.read_csv("data/yoochoose/yoochoose-clicks.dat",
    names=["session_id", "timestamp", "item_id", "category"])
sessions =df.groupby("session_id")["item_id"].apply(list)
sessions=sessions[sessions.apply(len)>=2]
sessions=sessions.reset_index(drop=True)
total=len(sessions)
sessions=sessions.iloc[total-total//64:]
split=int(len(sessions)* 0.8)
train_sessions=sessions.iloc[:split].tolist()
test_sessions=sessions.iloc[split:].tolist()


print("Training sessions:", len(train_sessions))
print("Test sessions:    ", len(test_sessions))
print("Sample train session:", train_sessions[0])
print("Sample test session: ", test_sessions[0])