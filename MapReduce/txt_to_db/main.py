from txttodb.turn import TxtToDB

if __name__ == "__main__":
    txt_to_db = TxtToDB()
    txt_to_db.interest_w_top10_to_db("interest_w_top10")
    txt_to_db.user_h_index_to_db("user_h_index")
    txt_to_db.close()